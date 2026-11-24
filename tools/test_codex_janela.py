"""Testes simulados do portão de imagens do Codex (tools/codex_janela.py) e do img_codex.py (24/11/2026).

Não chama o Codex nem grava no banco: diretório de estado temporário em $TMPDIR (IMG_CODEX_DIR), relógio fixo
(CODEX_JANELA_AGORA), status dos jobs da fila num json de teste (CODEX_JANELA_SEM_DB) e, no img_codex.py, só os ids
"forçados" (binário inexistente) ou "simulados" (limite fingido); FABRICA_DB inválido para não gravar eventos.
Uso: tools/.venv/bin/python tools/test_codex_janela.py   (sai 0 se tudo passou)
"""
import json
import os
import shutil
import subprocess
import sys
import tempfile
from datetime import date, datetime, timedelta
from pathlib import Path

AQUI = Path(__file__).resolve().parent
TMP = Path(os.environ.get("TMPDIR") or os.path.expanduser("~/cache/tmp"))
if str(TMP).startswith("/tmp"):
    TMP = Path(os.path.expanduser("~/cache/tmp"))
TMP.mkdir(parents=True, exist_ok=True)
BASE = Path(tempfile.mkdtemp(prefix="test-codex-janela-", dir=TMP))
os.environ.update(IMG_CODEX_DIR=str(BASE / "estado"), CODEX_JANELA_SEM_DB="1")
sys.path.insert(0, str(AQUI))
import codex_janela as CJ  # noqa: E402

TEXTO_429 = (':router: error=image generation failed: http 429 Too Many Requests: Some("{\\"error\\":{\\"type\\":'
             '\\"usage_limit_reached\\",\\"message\\":\\"The usage limit has been reached\\",\\"plan_type\\":\\"plus\\",'
             '\\"resets_at\\":%d,\\"eligible_promo\\":null,\\"limit_window_minutes\\":1440,\\"resets_in_seconds\\":6848}}")')
falhas = []


def ok(cond, nome):
    print(("  ok   " if cond else "  FALHOU ") + nome)
    if not cond:
        falhas.append(nome)


def relogio(s):
    os.environ["CODEX_JANELA_AGORA"] = s
    return datetime.fromisoformat(s)


def status_jobs(d):
    (CJ.DIR).mkdir(parents=True, exist_ok=True)
    (CJ.DIR / "test-status.json").write_text(json.dumps(d))


def zerar():
    shutil.rmtree(CJ.DIR, ignore_errors=True)
    CJ.DIR.mkdir(parents=True)


NOITE = date(2026, 11, 28)
VIDS = {"dossie-es": {"video": 901, "e1": "lote-dossie-018-x-e1", "e2": "lote-dossie-018-x-e2", "pasta": "x/dossie", "prazo": "2026-11-29 07:00"},
        "historia-ptbr": {"video": 902, "e1": "lote-historia-018-y-e1", "e2": "lote-historia-018-y-e2", "pasta": "x/historia", "prazo": "2026-11-29 10:00"}}


def noite_dois():
    zerar()
    CJ.gravar_noite(NOITE, ["dossie-es", "historia-ptbr"], {"dossie-es": VIDS["dossie-es"]})
    CJ.gravar_noite(NOITE, ["dossie-es", "historia-ptbr"], {"historia-ptbr": VIDS["historia-ptbr"]})
    status_jobs({})


print("1. noite com 1 canal só: começa direto")
zerar()
relogio("2026-11-28T21:30:00-03:00")
CJ.gravar_noite(NOITE, ["dossie-es"], {"dossie-es": VIDS["dossie-es"]})
ok(CJ.portao(901)[0], "portão aberto para o único vídeo")
ok(CJ.portao_job("lote-dossie-018-x-e2")[0], "fila sobe o e2 do único vídeo")

print("2. dois canais: Dossier primeiro, História espera o aviso")
noite_dois()
ok(CJ.portao(901)[0], "Dossier (1º) aberto")
ok(not CJ.portao(902)[0], "História (2º) fechado antes do aviso")
ok(not CJ.portao_job("lote-historia-018-y-e2")[0], "fila NÃO sobe o e2 do História")
ok(CJ.portao_job("lote-historia-018-y-e1")[0], "fila sobe o e1 do História (etapa 1 em paralelo)")
ok(CJ.portao_job("lote-dossie-018-x-e2")[0], "fila sobe o e2 do Dossier")

print("3. aviso: Dossier termina as imagens → História libera na hora")
relogio("2026-11-28T21:31:00-03:00")
CJ.registrar_imagem(901, "dossie-es")
d = CJ._ler(CJ.arq_noite(NOITE))
ok(d["imagens"]["dossie-es"]["estado"] == "gerando", "Dossier marcado como gerando na 1ª imagem")
ok(CJ.janela().get("imagens") == 1, "janela aberta com 1 imagem")
relogio("2026-11-28T22:35:00-03:00")
CJ.marcar_imagens(901, "concluido", "195 cenas")
ok(CJ.portao(902)[0], "História aberto depois do aviso")
ok(CJ.portao_job("lote-historia-018-y-e2")[0], "fila sobe o e2 do História")
ok("concluido" in (CJ._ler(CJ.arq_noite(NOITE)).get("liberado_por") or ""), "liberado_por registra o aviso")

print("4. Dossier falhou (e2 falhou) → libera")
noite_dois()
relogio("2026-11-28T22:00:00-03:00")
status_jobs({"lote-dossie-018-x-e2": "falhou"})
ok(CJ.portao(902)[0], "História liberado pela falha do Dossier")

print("5. Dossier travou (45+ min sem imagem nova) → libera")
noite_dois()
relogio("2026-11-28T21:40:00-03:00")
CJ.registrar_imagem(901, "dossie-es")
relogio("2026-11-28T22:10:00-03:00")
ok(not CJ.portao(902)[0], "30 min sem imagem: ainda espera")
relogio("2026-11-28T22:30:00-03:00")
ok(CJ.portao(902)[0], "50 min sem imagem: libera")

print("6. Dossier nem começou as imagens até 02:00 → libera")
noite_dois()
relogio("2026-11-29T01:59:00-03:00")
ok(not CJ.portao(902)[0], "01:59 ainda espera")
relogio("2026-11-29T02:01:00-03:00")
ok(CJ.portao(902)[0], "02:01 libera")

print("7. 429 do Codex: reset da mensagem, espera, sem retomar depois do prazo")
noite_dois()
t = relogio("2026-11-28T21:30:00-03:00")
for _ in range(3):
    CJ.registrar_imagem(901, "dossie-es")
relogio("2026-11-28T22:30:00-03:00")
reset_epoch = int((t + timedelta(hours=24)).timestamp())
r = CJ.registrar_limite(901, "dossie-es", TEXTO_429 % reset_epoch, {"type": "usageLimitExceeded", "resetsAt": reset_epoch})
ok(r == datetime.fromtimestamp(reset_epoch, CJ.TZ), "reset lido do resetsAt (= 1ª imagem + 24 h)")
j = CJ.janela_bruta()
ok(j["imagens_ate_limite"] == 3 and j["janela_min"] == 1440, "grava imagens até o limite e janela de 1440 min")
ok(CJ.limite_ativo()[0], "limite ativo")
ok(not CJ.portao(901)[0] and not CJ.portao(902)[0], "portão fechado para os dois vídeos")
os.environ["FILA_JOB"] = "lote-historia-018-y-e2"
CJ.marcar_aguarda("limite", "teste", r, 902, "historia-ptbr", 150)
prazo = datetime.fromisoformat("2026-11-29T10:00:00-03:00")
pr = CJ.pode_retomar("lote-historia-018-y-e2", prazo, False)
ok(not pr[0] and pr[2] is None and "prazo" in pr[1], "reset depois do prazo: não retoma sozinho (fila.sh retomar)")
pr = CJ.pode_retomar("lote-historia-018-y-e2", prazo, True)
ok(not pr[0] and pr[2] == r + timedelta(minutes=10), "com CODEX_RETOMA_APOS_PRAZO: retoma em reset + 10 min")
relogio((r + timedelta(minutes=11)).isoformat())
ok(not CJ.limite_ativo()[0], "depois do reset + 10: limite inativo")
ok(CJ.pode_retomar("lote-historia-018-y-e2", None, False)[0], "depois do reset: pode retomar (portão abre pelo reset)")
CJ.registrar_imagem(902, "historia-ptbr")
ok(CJ.janela().get("imagens") == 1 and not CJ.janela().get("limite_em"), "imagem nova abre janela nova")
del os.environ["FILA_JOB"]

print("8. leitura do reset sem resetsAt (só resets_in_seconds / retry-after)")
relogio("2026-11-28T22:00:00-03:00")
r2, fonte, _ = CJ.ler_reset('{"resets_in_seconds": 3600}')
ok(r2 == datetime.fromisoformat("2026-11-28T23:00:00-03:00") and "resets_in" in fonte, "resets_in_seconds")
r3, fonte3, _ = CJ.ler_reset("Retry-After: 120")
ok(r3 == datetime.fromisoformat("2026-11-28T22:02:00-03:00"), "retry-after")

print("9. img_codex.py simulado (sem chamar o Codex, sem banco)")
zerar()
relogio("2026-11-28T22:00:00-03:00")
CJ.gravar_noite(NOITE, ["dossie-es", "historia-ptbr"], {"dossie-es": VIDS["dossie-es"], "historia-ptbr": VIDS["historia-ptbr"]})
cenas = BASE / "cenas.json"
cenas.write_text(json.dumps([{"id": "I001", "prompt": "teste"}, {"id": "I002", "prompt": "teste"}]))
env = dict(os.environ, FABRICA_DB="dbname=nao_existe_teste host=/nonexistent", FILA_JOB="job-teste-hist",
           IMG_CODEX_SALDO_TESTE="0.5", IMG_CODEX_BIN="/nonexistent/codex-teste", IMG_CODEX_TESTE="1")
PY = str(AQUI / ".venv/bin/python")


def rodar(args, extra=None):
    e = dict(env, **(extra or {}))
    return subprocess.run([PY, str(AQUI / "img_codex.py"), "historia-ptbr", str(cenas), str(BASE / "saida"), *args],
                          capture_output=True, text=True, env=e, cwd=str(AQUI.parent), timeout=120)


p = rodar(["--video", "902", "--prazo-min", "1"])
ok(p.returncode == 4 and "CODEX_AGUARDAR" in p.stdout, "2º vídeo com portão fechado: sai 4 sem chamar o Codex")
m = CJ.ler_aguarda("job-teste-hist")
ok(bool(m) and m["tipo"] == "portao", "marcador aguarda/<job>.json (tipo portao) para a fila")
CJ.limpar_aguarda("job-teste-hist")
reset_epoch = int(datetime.fromisoformat("2026-11-29T21:30:00-03:00").timestamp())
p = rodar(["--video", "901", "--prazo-min", "1", "--paralelo", "1"],
          {"IMG_CODEX_SIMULAR_LIMITE": "I001,I002", "IMG_CODEX_SIMULAR_TEXTO": TEXTO_429 % reset_epoch, "FILA_JOB": "job-teste-dossie"})
ok(p.returncode == 4 and "CODEX_AGUARDAR" in p.stdout, "429 simulado no 1º vídeo: sai 4 (espera o reset)")
ok("fallback gemini NÃO chamado" in p.stdout and ".gemini-fallback" not in p.stdout, "sem fallback pago no limite")
m = CJ.ler_aguarda("job-teste-dossie")
ok(bool(m) and m["tipo"] == "limite" and m["reset_em"].startswith("2026-11-29T21:30"), "marcador com o reset da mensagem")
ok(not list((BASE / "saida").glob("*.jpg")), "nenhuma imagem/placeholder criada")
p = rodar(["--video", "901", "--prazo-min", "1"])
ok(p.returncode == 4 and "sem cota" in p.stdout, "com limite ativo, nova chamada nem tenta o Codex")
# falha pontual (não-limite) sem saldo para o fallback: fica faltando (sai 1), sem gastar (IMG_CODEX_TESTE: nunca chama a tool paga)
zerar()
p = rodar(["--video", "901", "--prazo-min", "1", "--paralelo", "1", "--so", "I001"], {"IMG_CODEX_FORCAR_FALHA": "I001"})
ok(p.returncode == 1 and "sem saldo para o fallback" in p.stdout, "falha pontual + Gemini abaixo da folga: não paga, sai 1")
# aviso: todas as cenas do cenas.json do vídeo existem → marca concluido e libera o 2º
zerar()
CJ.gravar_noite(NOITE, ["dossie-es", "historia-ptbr"], {"dossie-es": dict(VIDS["dossie-es"], pasta=str(BASE / "vid")),
                                                        "historia-ptbr": VIDS["historia-ptbr"]})
(BASE / "vid").mkdir(exist_ok=True)
shutil.copy(cenas, BASE / "vid" / "cenas.json")
(BASE / "saida").mkdir(exist_ok=True)
from PIL import Image  # noqa: E402
for i in ("I001", "I002"):
    Image.new("RGB", (64, 36), (120, 80, 40)).save(BASE / "saida" / f"{i}.jpg")
p = rodar(["--video", "901", "--prazo-min", "1"])
d = CJ._ler(CJ.arq_noite(NOITE))
ok(p.returncode == 0 and d["imagens"]["dossie-es"]["estado"] == "concluido" and d.get("liberado_em"),
   "tudo pronto no 1º → aviso 'pode seguir' (liberado)")

shutil.rmtree(BASE, ignore_errors=True)
print(f"\n{'TUDO OK' if not falhas else str(len(falhas)) + ' FALHA(S): ' + '; '.join(falhas)}")
sys.exit(1 if falhas else 0)
