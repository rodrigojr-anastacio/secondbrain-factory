import json
T = json.load(open("dl/dados/trilhos_caminhos.json"))
W = "Wikipedia pt (coordenadas da página do município)"
def c(nome, lat, lon, tipo, fonte, nota=""): return {"nome": nome, "lat": lat, "lon": lon, "tipo": tipo, "fonte": fonte, "nota": nota}
cidades = [
 c("Fortaleza", -3.7328, -38.5269, "cidade", W, "capital; 1872: 42.458 hab (censo, segundo O Povo; outra fonte, Fortaleza em Fotos, diz 21 mil); picos de 100 a 130 mil na seca"),
 c("Baturité", -4.3289, -38.885, "cidade", W, "serra úmida (brejo de altitude); terminal do ramal da EFB em 02/02/1882"),
 c("Quixadá", -4.9708, -39.015, "cidade", W, "EFB chega em 07/09/1891"),
 c("Açude do Cedro (Barragem Central)", -4.97825, -39.06293, "açude", "OpenStreetMap, way 547305578 'Barragem Central' (Overpass 13/11/2026)", "obra iniciada em 1890 (retomada), concluída em 1906; rio Sitiá, bacia do Banabuiú; ~126 hm3; datas de início variam por fonte (1877 planejamento, 1881, 1884, 1890)"),
 c("Sobral", -3.6861, -40.3497, "cidade", W, "estação da EF de Sobral inaugurada em 31/12/1882"),
 c("Crato", -7.2342, -39.4106, "cidade", "coordenada aproximada de conhecimento geral (Wikipedia pt não traz coordenadas para a página)", "trilhos da EFB chegam ao sul do Ceará só na década de 1920"),
 c("Icó", -6.4008, -38.8619, "cidade", W, "antigo polo do sertão do Jaguaribe"),
 c("Aracati", -4.5619, -37.77, "cidade", W, "porto fluvial/costeiro do Jaguaribe"),
 c("Camocim", -2.9008, -40.8428, "cidade", W, "porto de início da EF de Sobral; primeiros trilhos 26/03/1879"),
 c("Granja", -3.12, -40.8258, "cidade", W, "ponta do 1º trecho da EF de Sobral (24,5 km) aberto em 15/01/1881"),
 c("Mossoró", -5.1878, -37.3439, "cidade", W, "RN"),
 c("Recife", -8.0539, -34.8808, "cidade", W, "PE"),
 c("Belém", -1.4558, -48.5039, "cidade", W, "PA; porta de entrada da Amazônia"),
 c("Manaus", -3.0736, -60.0056, "cidade", W, "AM"),
 c("Rio Branco", -9.9747, -67.81, "cidade", "coordenada aproximada de conhecimento geral (a página da Wikipedia consultada retornou outro ponto, desconsiderado)", "AC; destino de seringueiros nordestinos a partir de ~1877+"),
]
estacoes = [
 c("Estação Central (hoje João Felipe), Fortaleza", -3.7195, -38.5366, "estação", "ponto de trilho OSM mais próximo + Wikipedia 'Estrada de Ferro de Baturité'", "inaugurada 30/11/1873 (outra fonte: 1880 no Campo da Amélia)"),
 c("Parangaba (Arronches)", -3.7766, -38.5658, "estação", "Wikipedia pt Parangaba", "1º trecho Fortaleza–Parangaba (7,2 km): trilhos desde 01/07/1873, tráfego 14/09/1873, inauguração formal 29/11/1873"),
 c("Maracanaú", -3.8767, -38.6256, "estação", "coordenada aproximada", "estações Mondubim e Maracanaú: 14/01/1875"),
 c("Pacatuba", -3.9839, -38.6175, "estação", "Wikipedia pt Pacatuba (Ceará)", "09/01/1876"),
 c("Baturité (estação)", -4.3289, -38.885, "estação", "Wikipedia pt (cidade)", "ramal Canoa–Baturité (9,86 km): obra iniciada 29/04/1881, tráfego 02/02/1882"),
 c("Quixadá (estação)", -4.9717, -39.0148, "estação", "OSM/Wikipedia", "07/09/1891"),
 c("Senador Pompeu (ex-Humaitá)", -5.5878, -39.3719, "estação", "Wikipedia pt (cidade)", "linha já chegava em ~1896-97 (perfil de 1897 em tese da UFC; data exata NÃO confirmada); prolongamento a partir daí iniciado em 1903-04"),
 c("Iguatu", -6.3597, -39.2986, "estação", "coordenada aproximada de conhecimento geral", "estação inaugurada em 05/11/1910 (Diário do Nordeste)"),
]
linhas = {
 "EF Baturité: Fortaleza–Baturité": {"pontos": T["Fortaleza-Baturite"], "fonte": "trilhos OSM (menor caminho), simplificado", "historia": "empresa fundada 05/03/1870; 1873 Fortaleza–Parangaba; 1875 Mondubim/Maracanaú; 1876 Pacatuba; Decreto 6.918 (01/06/1878): governo toma a obra no auge da seca; ramal Canoa–Baturité 02/02/1882", "confianca": "traçado atual (OSM) pode diferir em detalhes do original"},
 "EF Baturité: Fortaleza–Quixadá": {"pontos": T["Fortaleza-Quixada"], "fonte": "trilhos OSM (menor caminho), simplificado", "historia": "tráfego até Quixadá em 07/09/1891", "confianca": "idem"},
 "EF Baturité: Quixadá–Senador Pompeu": {"pontos": T["Quixada-Senador Pompeu"], "fonte": "trilhos OSM, simplificado", "historia": "~1896-97 (inferido)", "confianca": "idem; data não confirmada"},
 "EF Sobral: Camocim–Granja": {"pontos": [[-40.839, -2.901], [-40.838, -2.963], [-40.838, -3.038], [-40.834, -3.112], [-40.826, -3.12]], "fonte": "trilhos OSM abandonados/inativos (trechos), ligados por retas nas falhas", "historia": "1º trecho (24,5 km) aberto em 15/01/1881; obra iniciada 1878, 1os trilhos em Camocim em 26/03/1879", "confianca": "aproximado"},
 "EF Sobral: Granja–Sobral": {"pontos": [[-40.826, -3.12], [-40.62, -3.40], [-40.3497, -3.6861]], "fonte": "ESQUEMÁTICO: reta com 1 ponto intermediário (as estações intermediárias não foram verificadas; o leito foi desativado e não está no OSM)", "historia": "operação até Sobral em 31/12/1882; Ipu em 1894; Crateús em 25/01/1925", "confianca": "esquemático, só para desenho"},
}
rota_maritima = {
 "nome": "Fortaleza → Belém → Manaus → Rio Branco (migração da borracha)",
 "fonte": "traçado esquemático nosso (litoral Maranhão/Pará, calha do Amazonas e do Purus); cidades-pontes por coordenadas aproximadas",
 "trechos": {
  "Fortaleza→Belém (cabotagem)": [[-38.47, -3.70], [-40.9, -2.7], [-43.0, -2.2], [-44.3, -2.4], [-46.0, -1.1], [-47.4, -0.55], [-48.2, -0.8], [-48.5039, -1.4558]],
  "Belém→Manaus (rio Amazonas)": [[-48.5039, -1.4558], [-50.48, -1.68], [-51.64, -1.41], [-53.48, -1.80], [-54.70, -2.44], [-55.5, -1.9], [-56.74, -2.63], [-58.44, -3.14], [-60.0056, -3.0736]],
  "Manaus→Rio Branco (Solimões/Purus)": [[-60.0056, -3.0736], [-61.47, -3.69], [-64.8, -7.26], [-67.38, -8.75], [-67.81, -9.9747]]},
 "contexto": [
  "Wikipedia (en) 'Grande Seca': de ~800 mil habitantes da região afetada, cerca de 120.000 migraram para a Amazônia e 68.000 para outras partes do Brasil",
  "Rodolfo Teófilo (apud USP/Tupi): mais de 300 mil teriam ido povoar a Amazônia nos anos de estiagem (estimativa alta, discutida)",
  "SciELO RBH: 4.963 emigrantes registrados chegando à província do Amazonas entre 01/06/1877 e 20/08/1878 (só essa província)"]}
out = {"meta": {"acesso": "2026-11-13", "proj": "lon/lat WGS84 (converter com a projeção de longo-02/shared/geo.json se preciso)", "aviso": "campo 'fonte' em cada item; coordenadas de estações e rotas são aproximadas, adequadas para desenho de mapa e não para engenharia"},
       "cidades": cidades, "estacoes": estacoes, "linhas_ferroviarias": linhas, "rota_migracao": rota_maritima,
       "marcos": [
        {"data": "1870-03-05", "evento": "Fundada a Companhia da Estrada de Ferro de Baturité", "fonte": "Wikipedia pt EFB"},
        {"data": "1873-09-14", "evento": "Abre ao tráfego Fortaleza–Parangaba (1ª ferrovia do Ceará)", "fonte": "Wikipedia pt EFB; Fortaleza em Fotos"},
        {"data": "1877", "evento": "Início da grande seca; obras da EFB paradas por falta de caixa da companhia", "fonte": "Wikipedia pt EFB; Fortaleza em Fotos e Fatos"},
        {"data": "1878-06-01", "evento": "Decreto 6.918: governo imperial assume a obra e o direito de prolongar até Baturité; vira frente de trabalho de socorro", "fonte": "Wikipedia pt EFB; Fortaleza em Fotos"},
        {"data": "1878-12-10", "evento": "Dia dos Mil Mortos em Fortaleza (1.004 corpos sepultados num dia, varíola + fome)", "fonte": "O Povo, especial 'O Dia dos Mil Mortos'"},
        {"data": "1882-02-02", "evento": "Ramal Canoa–Baturité entregue ao tráfego", "fonte": "Fortaleza em Fotos e Fatos"},
        {"data": "1891-09-07", "evento": "Tráfego da EFB inaugurado até Quixadá", "fonte": "Fortaleza em Fotos e Fatos"},
        {"data": "1906", "evento": "Açude do Cedro concluído (1º grande açude público do Brasil), planejado após a seca", "fonte": "Diário do Nordeste / O Povo 2026"},
        {"data": "1910-11-05", "evento": "Estação de Iguatu inaugurada", "fonte": "Diário do Nordeste"},
        {"data": "1910", "evento": "Fusão EF Baturité + EF Sobral na Rede de Viação Cearense (1909 criação / 1910 fusão: fontes divergem)", "fonte": "Wikipedia pt EFB; UFC"}],
       "retirantes_obras": {"empregados_na_EFB": "estimativas: ~30 mil (pico), ~50 mil em dois anos, >60 mil entre 1878-1880 (fontes divergem)", "fontes": ["UFC tese tapcandido 2014", "Fortaleza em Fotos e Fatos", "repositório UFC 42509"], "retirantes_em_Fortaleza": "até ~115-130 mil (cidade com 20-40 mil antes); Freyre: 160 mil hab em dez/1878, 120 mil retirantes"}}
json.dump(out, open("dados/historia.json", "w"), ensure_ascii=False, separators=(",", ":"))
# ---- fome global
def r(nome, lat, lon, pais, mortes, fonte, nota=""): return {"regiao": nome, "pais": pais, "lat": lat, "lon": lon, "mortes_estimadas": mortes, "fonte": fonte, "nota": nota}
F = {"meta": {"acesso": "2026-11-13", "periodo": "1876-1879", "total_global": {"valor": "mais de 50 milhões (estimativa citada)", "fonte": "Singh et al. 2018, J. Climate 31(23), 'Climate and the Global Famine of 1876-78' (resumo na NASA NTRS 20180007824)", "aviso": "a cifra global é controversa e muito incerta; use como 'estimativas passam de 50 milhões', não como fato exato. O artigo é de Singh, Seager et al.; o título da pergunta ('The Great Global Drought of 1875-1878') não existe como tal. A seca é 'Great Drought' 1875-78."},
 "causas_singh2018": "Pacífico tropical frio 1870-76, El Niño recorde 1877-78, dipolo do Índico recorde em 1877, Atlântico Norte quente em 1878. Seca na Ásia de monções = a mais intensa em 800 anos e a 2ª mais extensa. Também Brasil, Austrália e norte/sudeste da África.",
 "coordenadas": "centroides aproximados de cada região"},
 "regioes": [
  r("Presidência de Madras", 14.0, 78.5, "Índia", {"valor": None}, "Wikipedia en 'Great Famine of 1876-78' (Madras, Bombaim, Punjab, Mysore, Hyderabad afetados de 1876 por ~2 anos)", "sem divisão por província em fonte verificada"),
  r("Presidência de Bombaim (Decão)", 18.5, 75.0, "Índia", {"valor": None}, "idem"),
  r("Estado de Mysore", 13.0, 76.6, "Índia", {"valor": 874000, "tipo": "queda de população vs censo de 1871 (não só mortes)"}, "Wikipedia en 'Great Famine of 1876-78'"),
  r("Hyderabad (Decão)", 17.4, 78.5, "Índia", {"valor": None}, "idem"),
  r("Índia (total)", 20.0, 78.0, "Índia", {"min": 5600000, "central": 8200000, "max": 9600000, "tipo": "mortes em excesso"}, "Wikipedia en 'Great Famine of 1876-78' (Dyson; 5,6 mi oficial; 8,2 mi Maharatna; 9,6 mi Digby)"),
  r("Shanxi", 37.6, 112.3, "China", {"valor": 5500000}, "Forrest (cônsul britânico em Tianjin) 1879, via Wikipedia en 'Northern Chinese Famine of 1876-1879'", "perda de população por censo: 8,18 mi (48%) incluindo migração"),
  r("Zhili (Hebei)", 39.0, 116.0, "China", {"valor": 2500000}, "idem"),
  r("Henan", 34.0, 113.5, "China", {"valor": 1000000}, "idem", "censo: -7,48 mi (22%)"),
  r("Shandong", 36.3, 118.0, "China", {"valor": 500000}, "idem"),
  r("Shaanxi", 34.3, 108.9, "China", {"valor": None}, "idem", "censo: -2,43 mi (25%)"),
  r("China (total)", 36.0, 113.0, "China", {"min": 9500000, "max": 13000000}, "Edgerton-Tarpley via Wikipedia en 'Northern Chinese Famine of 1876-1879'"),
  r("Ceará", -5.2, -39.3, "Brasil", {"min": 150000, "max": 200000, "tipo": "mortes; ~1/3 da população morreu ou migrou (Wikipedia pt)"}, "Wikipedia pt 'Seca dos três setes'; O Povo", "outra fonte (EBC) fala ~400 mil, provável confusão com o Nordeste"),
  r("Nordeste (total)", -7.5, -38.5, "Brasil", {"min": 150000, "max": 500000, "tipo": "mortes"}, "Cicinato Ferreira Neto 150-300 mil (EBC); Herbert Smith ~500 mil (EBC, Wikipedia pt/en: 400-500 mil)", "a cifra de 500 mil é repetida sem fonte primária clara"),
  r("Egito / Marrocos / África do Sul / Etiópia / Austrália", None, None, "vários", {"valor": None}, "Singh et al. 2018 mencionam apenas 'norte e sudeste da África' e Austrália como impactados (Atlântico/Índico); NÃO foi encontrada fonte verificada de mortes nem de recortes por país (Egito, Marrocos, Etiópia não confirmados)", "não desenhar com mortes; no máximo 'seca registrada'")]}
json.dump(F, open("dados/fome-global-1877.json", "w"), ensure_ascii=False, separators=(",", ":"))
# ---- hoje
H = {"meta": {"acesso": "2026-11-13"},
 "monitor_secas": {"arquivo": "dados/monitor-secas-2026-09.json", "mes": "2026-09", "nota": "mapa mais recente publicado: setembro/2026 (divulgado ~20/10/2026). O de outubro/2026 ainda NÃO existe (s3 da ANA retorna 404 em outubro2026.zip em 13/11/2026; costuma sair ~dia 20 do mês seguinte). Mesmo arquivo do longo-02; categorias SI/S0/S1/S2 (sem S3/S4).",
   "fontes": ["https://ana-monitor-secas-files.s3.sa-east-1.amazonaws.com/uploads/mapas/setembro2026.zip", "Correio da Manhã 23/10/2026: seca em 96% do território do Nordeste; avançou em 14 estados; seca grave se expandiu na BA, PE, PI; SE, AL, PB passaram de moderada a grave", "O Liberal 20/10/2026: seca grave no Nordeste 28% (ago-set, fontes divergem entre agosto e setembro)"],
   "ceara_jan2026": "68 municípios em seca extrema (S3) em jan/2026, pior cenário desde fev/2019; seca excepcional não atinge o CE desde jan/2018 (Diário do Nordeste 23/02/2026). Ceará inteiro com algum nível de seca em jan/2026."},
 "cisternas": {"p1mc_total": "mais de 1,2 milhão de cisternas de consumo humano construídas (ASA, marca celebrada em 2023 nos 20 anos do programa; matéria de fev/2026 repete '>1,2 milhão')", "fontes": ["ASA / Brasil de Fato 2024-04-11", "IHU Unisinos 2023-11-28 '20 anos do programa Cisterna'"], "obs": "não foi achado número oficial de 2026 com data de corte; ritmo médio ~50 mil por ano; 1.262 municípios do semiárido"},
 "previsao": {
  "el_nino": "NOAA/CPC (atualização citada em 10/09/2026): 93% de chance de El Niño 'muito forte' no outono/inverno boreal; 69% de chance de atingir níveis históricos em out-dez, acima dos eventos desde 1950. Nosso cálculo ERSSTv5: Niño 3.4 em out/2026 = +3,06 °C vs 1991-2020 (maior valor de toda a série 1854-2026).",
  "funceme": "Funceme (set/2026): ainda não é possível dizer como será a quadra chuvosa 2027 (fev-mai); El Niño pode trazer 'maior irregularidade de precipitações', veranicos e temperaturas mais altas; Atlântico tropical também decide; atualização 'nos próximos meses' (uma fonte diz janeiro).",
  "inmet": "Boletim Painel El Niño de outubro: nov/2026-jan/2027 com maior chance de chuva abaixo do normal em grande parte do Norte e áreas do Nordeste; impactos no Nordeste concentrados em verão e outono, especialmente no norte da região. Previsão trimestral detalhada de dez-fev para o semiárido não foi verificada no PDF original.",
  "fontes": ["https://diariodonordeste.verdesmares.com.br/ceara/el-nino-tem-93-de-chance-de-vir-muito-forte-e-causar-impactos-na-quadra-chuvosa-alerta-funceme-1.3790630", "https://portal.inmet.gov.br/noticias/painel-el-niño-boletim-de-outubro-é-divulgado", "https://www.cnnbrasil.com.br/nacional/brasil/boletim-aponta-el-nino-muito-forte-e-maior-risco-de-desastres-no-brasil/"]},
 "acudes_ce": {"inicio_outubro_2026": "46% da capacidade armazenada (O Povo 03/10/2026; 3º maior volume da década 2017-2026); bacias Sertões de Crateús, Baixo Jaguaribe, Banabuiú e Médio Jaguaribe abaixo de 30%; 33 açudes < 30% no início de setembro (Diário do Nordeste); Cogerh espera mais evaporação com El Niño. Valor de novembro não achado: ver Portal Hidrológico do Ceará."}}
json.dump(H, open("dados/hoje-2026.json", "w"), ensure_ascii=False, indent=1)
import os
for f in sorted(os.listdir("dados")): print(f, os.path.getsize("dados/"+f)//1024, "KB")
