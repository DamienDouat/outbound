#!/usr/bin/env python3
"""
Socle commun — charge la config et expose les helpers Notion.

Tout le moteur (route_all, icebreaker_engine, build_*) lit `config/outbound.config.json`
via ce module : aucune valeur (DB IDs, colonnes, campagnes, branding) n'est en dur.

Config : config/outbound.config.json (copie de l'example, gitignored).
Secret : variable d'environnement nommée par config.notion.token_env (def. NOTION_TOKEN),
         lue depuis l'environnement ou un fichier .env à la racine du repo.
"""
import json
import os
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CONFIG_PATH = ROOT / "config" / "outbound.config.json"


def load_config():
    if not CONFIG_PATH.exists():
        raise SystemExit(
            f"✗ {CONFIG_PATH} absent. Copie config/outbound.config.example.json "
            f"-> config/outbound.config.json et remplis tes valeurs."
        )
    return json.load(open(CONFIG_PATH))


CFG = load_config()
COLS = CFG["notion"]["columns"]


def col(key):
    """Nom de colonne Notion depuis la config (mapping schéma)."""
    return COLS[key]


def _env_file_value(name):
    env = ROOT / ".env"
    if not env.exists():
        return None
    for line in env.read_text().splitlines():
        if line.startswith(name + "="):
            return line.split("=", 1)[1].strip().strip('"').strip("'")
    return None


def load_token():
    name = CFG["notion"].get("token_env", "NOTION_TOKEN")
    return os.environ.get(name) or _env_file_value(name) or _fail_token(name)


def _fail_token(name):
    raise SystemExit(f"✗ Token Notion absent. Pose ${name} (env) ou dans .env à la racine.")


def notion(method, path, token, body=None):
    """Appel API Notion via curl (zéro dépendance). Retourne le JSON."""
    args = ["curl", "-sS", "-X", method,
            "-H", "Authorization: Bearer " + token,
            "-H", "Notion-Version: 2022-06-28",
            "-H", "Content-Type: application/json",
            "https://api.notion.com" + path]
    if body is not None:
        args[6:6] = ["--data", json.dumps(body)]
    p = subprocess.run(args, capture_output=True, text=True)
    try:
        return json.loads(p.stdout)
    except json.JSONDecodeError:
        return {"error": p.stdout or p.stderr}


def query_all(db, token):
    """Pagine une base Notion entière."""
    out, cur = [], None
    while True:
        b = {"page_size": 100}
        if cur:
            b["start_cursor"] = cur
        d = notion("POST", f"/v1/databases/{db}/query", token, b)
        if d.get("error"):
            raise SystemExit("✗ " + str(d["error"]))
        out += d.get("results", [])
        if d.get("has_more"):
            cur = d["next_cursor"]
        else:
            return out


def title_text(prop):
    return "".join(t["plain_text"] for t in prop.get("title", [])).strip()


def famille_to_persona(fam):
    return CFG.get("famille_to_persona", {}).get(fam or "", "Metier")


def campaign_id(tier, persona):
    return CFG["campaigns"].get(tier, {}).get(persona)
