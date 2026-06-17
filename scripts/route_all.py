#!/usr/bin/env python3
"""
Routeur unifié 3 tiers × N personas — remplit les campagnes.

Pour chaque Contact lié à une Company `Prospect`, avec un canal LinkedIn :
  - tier : arc validé (dataset) -> WARM ; sinon icebreaker dispo -> ICE ; sinon -> STD
  - persona (depuis la Famille via config.famille_to_persona) -> campagne (config.campaigns)

Règles dures (config-driven) :
  - 1 seule entrée par enseigne (Company) : meilleur contact
    (priorité tier = config.tiers ; à tier égal, persona = config.persona_priority).
  - Déjà en séquence exclu (enseigne ayant >=1 contact `Canal status = <in_sequence>`).
  - LinkedIn-only.

Sortie : data/route/<tier>_<persona>.json (leads + page_id + variables). NE PUSHE RIEN.
Affiche le PLAN. Le push (add_leads_to_campaign) + la MAJ Canal status sont des actes gatés.
"""
import json
import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import _common as c

ROOT = Path(__file__).resolve().parents[1]
CFG = c.CFG
TIER_RANK = {t: i for i, t in enumerate(CFG["tiers"])}
PERSONA_RANK = {p: i for i, p in enumerate(CFG["persona_priority"])}


def li(pr):
    return (pr.get(c.col("linkedin"), {}).get("url") or "").strip()


def load_arcs():
    p = ROOT / CFG.get("arc_dataset", "")
    if not p.exists():
        return {}
    return {x["page_id"]: x for x in json.load(open(p)) if x.get("t1_body")}


def load_ice():
    ice = {}
    for f in CFG.get("icebreaker_files", []):
        p = ROOT / f
        if p.exists():
            ice.update(json.load(open(p)))
    return ice


def main():
    tok = c.load_token()
    arcs, ice = load_arcs(), load_ice()
    in_seq = CFG["notion"]["columns"]["canal_in_sequence_value"]
    prosp_val = CFG["notion"]["columns"]["prospect_value"]
    validated = CFG["notion"]["columns"]["arc_validated_value"]

    comps = c.query_all(CFG["notion"]["companies_db"], tok)
    prospect, cname = set(), {}
    for co in comps:
        st = co["properties"].get(c.col("company_status"), {}).get("status")
        if st and st.get("name") == prosp_val:
            prospect.add(co["id"])
            cname[co["id"]] = c.title_text(co["properties"].get(c.col("company_title"), {}))

    rows = c.query_all(CFG["notion"]["contacts_db"], tok)

    taken = set()
    for p in rows:
        canal = (p["properties"].get(c.col("canal_status"), {}).get("select") or {}).get("name")
        if canal == in_seq:
            for r in p["properties"].get(c.col("companies_relation"), {}).get("relation", []):
                taken.add(r["id"])

    best = {}
    stats = {"no_prospect": 0, "no_linkedin": 0, "already_taken": 0, "candidates": 0}
    for p in rows:
        pr = p["properties"]
        rels = [r["id"] for r in pr.get(c.col("companies_relation"), {}).get("relation", []) if r["id"] in prospect]
        if not rels:
            stats["no_prospect"] += 1
            continue
        cid = rels[0]
        if cid in taken:
            stats["already_taken"] += 1
            continue
        liurl = li(pr)
        if not liurl:
            stats["no_linkedin"] += 1
            continue
        pid = p["id"]
        fam = (pr.get(c.col("famille"), {}).get("select") or {}).get("name") or ""
        arc_ok = ((pr.get(c.col("arc_status"), {}).get("select") or {}).get("name") == validated) and pid in arcs
        tier = "warm" if arc_ok else ("ice" if pid in ice else "std")
        per = c.famille_to_persona(fam)
        if per not in PERSONA_RANK:
            per = CFG["persona_priority"][-1]
        name = c.title_text(pr.get(c.col("contact_title"), {}))
        first = name.split()[0] if name else ""
        last = " ".join(name.split()[1:]) if len(name.split()) > 1 else ""
        lead = {"page_id": pid, "firstName": first, "lastName": last,
                "companyName": cname.get(cid, ""), "linkedinUrl": liurl,
                "tier": tier, "persona": per,
                "rank": (TIER_RANK[tier], PERSONA_RANK.get(per, 99))}
        if tier == "warm":
            a = arcs[pid]
            t1 = a.get("t1_body", "")
            lead["variables"] = {
                "noteInvite": a.get("t1_invite_note", ""), "t1Subject": a.get("t1_subject", ""),
                "t1BodyLi": t1, "t1BodyMail": t1.replace("\n", "<br>"),
                "t2BodyMail": a.get("t2_body", "").replace("\n", "<br>"),
            }
        elif tier == "ice":
            lead["variables"] = {"icebreaker": ice[pid]}
        else:
            lead["variables"] = {}
        cur = best.get(cid)
        if cur is None or lead["rank"] < cur["rank"]:
            best[cid] = lead
        stats["candidates"] += 1

    out = {}
    for lead in best.values():
        out.setdefault((lead["tier"], lead["persona"]), []).append(lead)

    rdir = ROOT / "data" / "route"
    os.makedirs(rdir, exist_ok=True)
    print("[PLAN — 1 entrée/enseigne, LinkedIn-only, déjà-en-séquence exclus]\n")
    print(f"{'tier':8}{'persona':10}{'campagne':22}{'leads':6}")
    total = 0
    for (tier, per), leads in sorted(out.items(), key=lambda kv: (TIER_RANK[kv[0][0]], PERSONA_RANK.get(kv[0][1], 99))):
        cam = c.campaign_id(tier, per) or "(non configurée)"
        json.dump(leads, open(rdir / f"{tier}_{per}.json", "w"), ensure_ascii=False)
        print(f"{tier:8}{per:10}{cam:22}{len(leads):<6}")
        total += len(leads)
    print(f"\n  total à pousser : {total}")
    print(f"  skip : {stats}")
    print(f"  fichiers : {rdir}/<tier>_<persona>.json")


if __name__ == "__main__":
    main()
