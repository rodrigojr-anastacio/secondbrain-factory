#!/usr/bin/env python3
"""Link curto e rastreável da HQ por vídeo (24/11/2026): uma OFERTA da Cakto por vídeo ("YT <NNN-slug>").

Cada oferta tem o próprio link curto https://pay.cakto.com.br/<id> e entra no mesmo checkout personalizado
(o checkout padrão do produto pega as ofertas novas sozinho). O pedido guarda a oferta → sabemos qual vídeo vendeu.

Uso: tools/.venv/bin/python canais/dossie-es/cta/cakto_oferta.py <NNN-slug>   → imprime o link (cria se não existir)
Chave: ~/.segredos/cakto.env (CAKTO_CLIENT_ID/SECRET). Nunca imprime a chave nem o token.
"""
import json
import sys
import urllib.parse
import urllib.request
from pathlib import Path

API = "https://api.cakto.com.br/public_api"
PRODUTO = "a67561b3-0ad2-43f1-b0d0-e2088002363a"   # Expedientes Secretos #1 (US$ 4,99)
PRECO, MOEDA = 4.99, "USD"


def _req(url, data=None, token=None, form=False):
    h = {"User-Agent": "fabrica-dossie/1.0", "Accept": "application/json"}
    if token:
        h["Authorization"] = f"Bearer {token}"
    body = None
    if data is not None:
        if form:
            body = urllib.parse.urlencode(data).encode()
            h["Content-Type"] = "application/x-www-form-urlencoded"
        else:
            body = json.dumps(data).encode()
            h["Content-Type"] = "application/json"
    with urllib.request.urlopen(urllib.request.Request(url, data=body, headers=h), timeout=30) as r:
        return json.load(r)


def token():
    env = {}
    for l in (Path.home() / ".segredos/cakto.env").read_text().splitlines():
        if "=" in l:
            k, v = l.split("=", 1)
            env[k.strip()] = v.strip()
    return _req(f"{API}/token/", {"client_id": env["CAKTO_CLIENT_ID"], "client_secret": env["CAKTO_CLIENT_SECRET"]},
                form=True)["access_token"]


def link(slug, tk=None):
    tk = tk or token()
    nome = f"YT {slug}"
    url = f"{API}/offers/?product={PRODUTO}&limit=200"
    while url:
        d = _req(url, token=tk)
        for o in d.get("results", d if isinstance(d, list) else []):
            if o.get("name") == nome and o.get("status") == "active":
                return f"https://pay.cakto.com.br/{o['id']}"
        url = d.get("next") if isinstance(d, dict) else None
    o = _req(f"{API}/offers/", {"product": PRODUTO, "name": nome, "price": PRECO, "currency": MOEDA, "type": "unique"},
             token=tk)
    return f"https://pay.cakto.com.br/{o['id']}"


if __name__ == "__main__":
    print(link(sys.argv[1]))
