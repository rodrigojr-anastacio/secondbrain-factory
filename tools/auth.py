"""Login OAuth de um canal (uma vez por canal).

Uso: ~/workspace/fabrica-youtube/tools/.venv/bin/python ~/workspace/fabrica-youtube/tools/auth.py <nome-do-canal>
Rode com o túnel do Mac aberto: ssh -L 8765:localhost:8765 hermes@<vps>
"""
import os
import sys

from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

from _paths import CLIENT, TOKENS

SCOPES = [
    "https://www.googleapis.com/auth/youtube.readonly",
    "https://www.googleapis.com/auth/yt-analytics.readonly",
]


def main():
    if len(sys.argv) != 2:
        sys.exit("uso: auth.py <nome-do-canal>  (ex.: lotr-fr)")
    nome = sys.argv[1]
    flow = InstalledAppFlow.from_client_secrets_file(CLIENT, SCOPES)
    creds = flow.run_local_server(
        host="localhost",
        port=8765,
        open_browser=False,
        authorization_prompt_message="\nAbra este link no navegador do Mac e escolha o canal:\n\n{url}\n",
        success_message="Pronto, pode fechar esta aba.",
    )
    path = os.path.join(TOKENS, f"{nome}.json")
    with open(os.open(path, os.O_WRONLY | os.O_CREAT | os.O_TRUNC, 0o600), "w") as f:
        f.write(creds.to_json())
    yt = build("youtube", "v3", credentials=creds)
    ch = yt.channels().list(part="snippet", mine=True).execute()["items"][0]
    print(f"\nOK: token salvo para o canal '{ch['snippet']['title']}' em {path}")


if __name__ == "__main__":
    main()
