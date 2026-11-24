# BLOQUEIO: entrega no Drive (24/11/2026)

O pacote da #1 está pronto em `001/pacote/` e `001/previas/`, mas o rclone não acessa o Drive:
`gdrive: couldn't fetch token: invalid_grant: maybe token expired? - try refreshing with "rclone config reconnect gdrive:"`.

Precisa do Rodrigo (login no navegador): `rclone config reconnect gdrive:` (aproveitar e criar o client_id próprio, pendência antiga).
Depois, para entregar (pôster C no zip por padrão; trocar antes se ele escolher o A: ver `E2-RELATORIO.md`):
```
cd ~/workspace/fabrica-youtube/canais/dossie-es/produtos/hq/001
D="gdrive:Youtube/Dossier en Minutos/produtos/Expedientes-Secretos-1"
rclone copy pacote/Expedientes-Secretos-1.zip "$D/"
rclone copy pacote/Expedientes-Secretos-1.pdf "$D/"
rclone copy previas "$D/previas/"
rclone copy pacote "$D/posteres/" --include "poster-*"
rclone ls "$D"
```
