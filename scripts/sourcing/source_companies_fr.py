#!/usr/bin/env python3
"""
Adaptateur sourcing — FRANCE (INSEE via recherche-entreprises.api.gouv.fr).

Gratuit, sans clé, France uniquement. Cherche des sociétés par code(s) NAF + département(s) +
tranche(s) d'effectif (depuis config.sourcing), dédoublonne par SIREN, et :
  - par défaut (dry) : écrit les candidats dans data/companies_candidates.json + récap.
  - avec --push     : crée les Companies manquantes dans Notion (titre + statut Prospect), gaté.

C'est un ADAPTATEUR : le reste du moteur (route_all, campagnes) est provider-agnostique.
Pour un autre pays/source, écris un nouvel adaptateur qui produit le même
data/companies_candidates.json (champs : siren, name, naf, tranche, dept). Voir docs/sourcing.md.

Usage :
  python3 scripts/sourcing/source_companies_fr.py [--push]
"""
import json
import subprocess
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import _common as c

ROOT = Path(__file__).resolve().parents[2]
API = "https://recherche-entreprises.api.gouv.fr/search"
SRC = c.CFG.get("sourcing", {})


def _tranche_range():
    lo = int(SRC.get("employee_tranches_min", "21"))
    hi = int(SRC.get("employee_tranches_max", "42"))
    return ",".join(str(t) for t in range(lo, hi + 1))


def fetch(naf, dept, page):
    q = [f"activite_principale={naf}", f"page={page}", "per_page=25"]
    tr = _tranche_range()
    if tr:
        q.append("tranche_effectif_salarie=" + tr)
    if dept:
        q.append("departement=" + dept)
    url = API + "?" + "&".join(q)
    p = subprocess.run(["curl", "-sS", url], capture_output=True, text=True)
    try:
        return json.loads(p.stdout)
    except json.JSONDecodeError:
        return {"results": []}


def harvest():
    seen, out = set(), []
    depts = SRC.get("departments") or [None]
    for naf in SRC.get("naf_codes", []):
        for dept in depts:
            for page in range(1, int(SRC.get("page_limit", 5)) + 1):
                r = fetch(naf, dept, page)
                res = r.get("results", [])
                if not res:
                    break
                for e in res:
                    siren = e.get("siren")
                    if not siren or siren in seen:
                        continue
                    seen.add(siren)
                    out.append({
                        "siren": siren,
                        "name": (e.get("nom_complet") or e.get("nom_raison_sociale") or "").strip(),
                        "naf": (e.get("siege", {}) or {}).get("activite_principale") or e.get("activite_principale"),
                        "tranche": e.get("tranche_effectif_salarie"),
                        "dept": (e.get("siege", {}) or {}).get("departement"),
                    })
                time.sleep(0.2)
    return out


def push_notion(cands):
    tok = c.load_token()
    db = c.CFG["notion"]["companies_db"]
    existing = {c.title_text(p["properties"].get(c.col("company_title"), {})).lower()
                for p in c.query_all(db, tok)}
    created = skipped = 0
    for x in cands:
        if not x["name"] or x["name"].lower() in existing:
            skipped += 1
            continue
        body = {"parent": {"database_id": db}, "properties": {
            c.col("company_title"): {"title": [{"text": {"content": x["name"][:195]}}]},
            c.col("company_status"): {"status": {"name": c.CFG["notion"]["columns"]["prospect_value"]}},
        }}
        r = c.notion("POST", "/v1/pages", tok, body)
        if r.get("error"):
            print("  ✗", x["name"], r["error"])
        else:
            created += 1
            existing.add(x["name"].lower())
        time.sleep(0.34)
    print(f"[push] créées {created} | déjà présentes/skip {skipped}")


def main():
    if not SRC.get("naf_codes"):
        sys.exit("✗ config.sourcing.naf_codes vide. Renseigne tes activités cibles.")
    cands = harvest()
    out = ROOT / "data" / "companies_candidates.json"
    json.dump(cands, open(out, "w"), ensure_ascii=False, indent=1)
    print(f"[france_insee] {len(cands)} sociétés -> {out}")
    if "--push" in sys.argv:
        push_notion(cands)
    else:
        print("  (dry-run) relance avec --push pour écrire dans Notion (statut Prospect).")


if __name__ == "__main__":
    main()
