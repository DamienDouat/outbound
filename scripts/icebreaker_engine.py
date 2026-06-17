#!/usr/bin/env python3
"""
Moteur d'icebreaker (tier ICE) — prépare la feuille de rédaction.

L'icebreaker = 1 phrase honnête tirée de la note CRM du contact, glissée en 2e ligne
du template ICE. La GÉNÉRATION est faite par l'agent (lecture de la note, règles : zéro
signal inventé, accord correct, ton sobre). Ce script ne fait que préparer la liste.

Usage :
  python3 icebreaker_engine.py prepare
      -> data/icebreakers_todo.json  (page_id, prénom, société, persona, note)

L'agent rédige 1 phrase par page_id et l'écrit dans le fichier config.icebreaker_files[0]
(objet JSON {page_id: "phrase"} ; omettre les contacts sans signal exploitable).
Ensuite route_all.py route ces contacts vers le tier ICE.
"""
import json
import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import _common as c

ROOT = Path(__file__).resolve().parents[1]
CFG = c.CFG


def note_text(pr):
    n = pr.get(c.col("note"), {}).get("rich_text", [])
    return "".join(t["plain_text"] for t in n).strip()


def li(pr):
    return (pr.get(c.col("linkedin"), {}).get("url") or "").strip()


def existing_icebreakers():
    keys = set()
    for f in CFG.get("icebreaker_files", []):
        p = ROOT / f
        if p.exists():
            keys |= set(json.load(open(p)).keys())
    return keys


def cmd_prepare():
    tok = c.load_token()
    prosp_val = CFG["notion"]["columns"]["prospect_value"]
    validated = CFG["notion"]["columns"]["arc_validated_value"]
    comps = c.query_all(CFG["notion"]["companies_db"], tok)
    prospect, cname = set(), {}
    for co in comps:
        st = co["properties"].get(c.col("company_status"), {}).get("status")
        if st and st.get("name") == prosp_val:
            prospect.add(co["id"])
            cname[co["id"]] = c.title_text(co["properties"].get(c.col("company_title"), {}))
    done = existing_icebreakers()
    rows = c.query_all(CFG["notion"]["contacts_db"], tok)
    todo = []
    for p in rows:
        pr = p["properties"]
        if p["id"] in done:
            continue
        rels = [r["id"] for r in pr.get(c.col("companies_relation"), {}).get("relation", []) if r["id"] in prospect]
        if not rels:
            continue
        if (pr.get(c.col("arc_status"), {}).get("select") or {}).get("name") == validated:
            continue  # tier WARM
        if not li(pr):
            continue  # LinkedIn-only
        note = note_text(pr)
        if len(note) < 40:
            continue  # pas de matière -> reste STD (générique)
        name = c.title_text(pr.get(c.col("contact_title"), {}))
        fam = (pr.get(c.col("famille"), {}).get("select") or {}).get("name") or ""
        todo.append({"page_id": p["id"], "firstName": name.split()[0] if name else "",
                     "lastName": " ".join(name.split()[1:]),
                     "companyName": cname.get(rels[0], ""),
                     "persona": c.famille_to_persona(fam), "note": note})
    out = ROOT / "data" / "icebreakers_todo.json"
    json.dump(todo, open(out, "w"), ensure_ascii=False, indent=1)
    print(f"[prepare] {len(todo)} contacts à icebreaker -> {out}")
    for per, n in Counter(t["persona"] for t in todo).most_common():
        print(f"  {per:10} {n}")
    print(f"\nL'agent rédige 1 phrase honnête par page_id -> {CFG['icebreaker_files'][0]}")


def main():
    if len(sys.argv) < 2 or sys.argv[1] != "prepare":
        sys.exit("usage: icebreaker_engine.py prepare")
    cmd_prepare()


if __name__ == "__main__":
    main()
