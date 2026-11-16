# Auditoria de cópia dos vídeos já feitos · 16/11/2026

Só relatório: nada foi refeito. Detector `tools/similaridade_roteiro.py` (limites: atenção ≥ 18, cópia ≥ 30; `CALIBRAGEM.md`). Referências: 5–6 vídeos por tema (canal-modelo + os de mais views em pt/es/en + clones), transcritos por `tools/manada.py` em `refs/<chave>/` (`manada.json` com canal, views e data). Relatório completo de cada um, com os trechos parecidos, em `auditoria/<chave>.md`.

| Vídeo | Status / publicação | Nota | Referência mais parecida | Veredito | Leitura |
|---|---|---|---|---|---|
| historia 005 Brasil | publicado 09/11 | **47** | History in Minutes `Vug2cLY3nxk` (51% dos blocos, 96% na mesma ordem); History Easy Guide `sD0cIJ8JMYw` = 38 | **CÓPIA** | o caso que motivou a regra; Pedro II e o telefone, café com leite, Juscelino "50 em 5", guerra do Paraguai: as mesmas cenas na mesma ordem |
| historia 008 França | publicado 15/11 | **28** | clone pt "História em minutos" `7amJtj96T0w` (31%, ordem 100%) | atenção (alta) | Clóvis católico + bispos de Roma, Natal de 800, Leonor da Aquitânia, "Paris bem vale uma missa": mesmo encadeamento do clone (referência assistida no BRIEF) |
| historia 009 Alemanha | pronto, agendado 16/11 11:30 | 14 | Genius History `wrPmVXTr91s` (16%) | ok | gêmeos isolados de fatos obrigatórios (Armínio, Sacro Império/Voltaire, punhalada pelas costas) |
| **historia 010 Japão** | **pronto, qua 18/11** | **7** | Genius History `ecnCTOzIivE` (8%) | **ok** | ângulo próprio ("copiava, mas ninguém conquistava") funcionou: 1 bloco de consenso em 63 |
| dossie 007 SS | publicado 15/11 | **28** | Archive in Minutes SS `PmpWyltn08s` (33%, ordem 87%); clone The Full Record = 21 | atenção (alta) | fuga de Himmler (bigode, parche, papéis de Hitzinger, cianuro em Lüneburg), Oradour e a Noite dos Longos Punhais com os mesmos detalhes do Archive |
| dossie 008 Inquisición | publicado 16/11 | 3 | Into the Shadows `FQXDIUjr41M` | ok | o Archive não tem o tema; roteiro próprio |
| **dossie 009 Gestapo** | **pronto, qua 18/11** | **24** | clone es "Archivo en Minutos" `OnGBjUOSE4Y` (613 views; 26%); Archive Gestapo `pbIzG1QvoWs` = 11 | **atenção** | os trechos iguais são a parte institucional (Göring cria a Gestapo em 26/04/1933, "Geheime Staatspolizei", RSHA/Departamento IV sob Müller): fatos obrigatórios ditos de modo muito parecido; hook e fio (Barbie/La Paz, Sudamérica) são nossos e não aparecem no Archive |
| **clearance 004 Pearl Harbor** | **pronto, qua 18/11** | **2** | Forgotten Fleet USS Utah `0F3PpD3qBwI` (3%) | **ok** | ângulo e documentos próprios (buracos de bala de Hickam) |
| **em-relevo 005 Enchente 2024** | **pronto, qua 18/11** | **11** | Terra em Choque `sdBxzdQLbaE` (15%) | **ok** | os gêmeos são a geografia obrigatória (5 rios → Guaíba → Lagoa dos Patos); o caminho da água no mapa é ângulo nosso |

## Os de quarta (18/11), para o Rodrigo decidir se publica
- **Japão (7), Pearl Harbor (2), Enchente (11): ok**, ângulo próprio; publicar sem ressalva do ponto de vista de cópia.
- **Gestapo (24): atenção.** Não é cópia do Archive (11), mas 26% dos blocos têm gêmeo no clone espanhol "Archivo en Minutos" (613 views), quase todos na explicação institucional (criação, RSHA, Müller), que é fato obrigatório do tema. O hook e o fio (Barbie preso em La Paz, Sudamérica) são próprios. Recomendação: **publicar** (risco baixo; o clone é minúsculo e o trecho é factual); no próximo do canal, a cota de expedientes próprios (≥ 50%) evita isso.

## Já no ar
- **005 Brasil (47) = cópia** e **008 França / 007 SS (28) = atenção alta**: não refazemos nada (pedido do brief). Se algum dia forem reembalados ou republicados, o roteiro precisa passar pelo crivo de ângulo antes.

## Padrões observados (vão para as bíblias)
- O risco nasce na **referência assistida que vira esqueleto**: 005 (HiM), 008 (clone pt), 007 (Archive). Onde a referência foi só de forma ou o ângulo era nosso (010 Japão, Pearl Harbor, Inquisición, Enchente), a nota ficou ≤ 14.
- Vídeos independentes do mesmo tema dão 0–15: fatos obrigatórios (datas, nomes) não puxam a nota sozinhos.
- **Clones minúsculos no mesmo idioma** (History Easy Guide, Archivo en Minutos, The Full Record) são os mais parecidos conosco, porque todos remodelam o mesmo canal-modelo: a manada inclui os clones sempre.
