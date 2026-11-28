#!/usr/bin/env python3
"""Amostra v3 (historia-ptbr): Rio, 1808 — o P.R. na sua porta. Fonte única do roteiro (só texto).

Gera SCRIPT.md e blocos.json nesta pasta. Rodar: python3 roteiro.py
Bloco = (id, passo, ideia, texto). Passos = esqueleto v3 da bíblia (1 Arremesso … 8 Veredito).
"""
import json, re
from pathlib import Path

AQUI = Path(__file__).resolve().parent
PPM = 128  # voz do canal (bíblia, tabela Tamanho)

TOPO = """# SCRIPT — amostra v3 001: Rio, 1808 (o P.R. na sua porta)

**Promessa:** você vive, na pele de um carioca comum, o despejo da corte em 1808: o oficial escreve P.R. a giz na sua porta, você tem 24 horas para sair, e o vídeo mostra quanto tempo você aguenta até ter a casa de volta (13 anos).
**Títulos:** T1 Rio, 1808: Escreveram "P.R." na Sua Porta e Você Tinha 24 Horas Para Sair / T2 Você Foi Despejado Pela Corte em 1808: 13 Anos Sem a Sua Casa / T3 O Dia em que a Corte Chegou e Ficou com a Sua Casa (Rio, 1808)
**Pergunta-gancho:** quanto tempo você aguenta depois que a corte escreve P.R. na sua porta?
**Fio condutor:** a sua casa (perdida no 0:20, cobrada no clímax, devolvida no veredito); cada bloco é consequência do despejo (rua → degrau → aluguel → emprego → quarto → febre → briga pela casa).
**Loop 1:** a promessa do conde, "Pago o aluguel estipulado" (N010, ~2:40) → paga em N041–N043 (~10:50: dez anos sem pagar, caso real do Conde de Belmonte) e no veredito (a chave volta, a cama não).
**Loop 2:** Marrocos, o freguês ranzinza que "não pretende ficar" (N025–N026, ~6:30) → reaparece na doença (N038) e paga em N049 (~13:00: fica no Rio até o fim da vida, 1838).
**Rebobinas:** N009 (cadeia → entrega sorrindo), N037 (bexiga → febre comum), N045 (sobrado → casa térrea).
**Dispositivos:** Despachante do Tempo, Turista de chinelo, cronômetro "VOCÊ DUROU", "Cronômetro valendo.", "Rebobina."
"""

BLOCOS = [
    # 1 · Arremesso (0:00–0:40)
    ("N001", 1, True, "Você está no sofá, pagando o aluguel pelo celular. Surge o Despachante do Tempo e carimba a sua testa: Senha mil oitocentos e oito!"),
    ("N002", 1, False, "Rio de Janeiro, março de mil oitocentos e oito. Você acorda de chinelo na sua casa da Rua Direita. Batem na porta. Um oficial de justiça escreve nela, a giz, duas letras: P. R. E você tem vinte e quatro horas para sair."),
    ("N003", 1, False, "Você está sem celular, sem advogado, sem caminhão de mudança. Quanto tempo você aguenta? Cronômetro valendo."),
    # 2 · Chegada (0:40–2:30)
    ("N004", 2, True, "A fofoca você pega na esquina. Napoleão invadiu Portugal no fim de mil oitocentos e sete, e o príncipe regente, Dom João, fugiu de navio com o governo inteiro. Parou em Salvador em janeiro e chegou aqui no dia sete de março."),
    ("N005", 2, False, "Os cronistas falam em dez a quinze mil pessoas nos navios, mas é estimativa: tem historiador que conta uns quinhentos nobres. Pouca ou muita, essa gente precisa dormir. E a cama que eles querem é a sua."),
    ("N006", 2, False, "P. R. quer dizer Príncipe Regente. Você ouve o vizinho ler de outro jeito: Ponha-se na Rua. E a vizinha, na versão azeda: Propriedade Roubada."),
    ("N007", 2, True, "Você quer reclamar? Então você precisa entender o processo. O cronista Joaquim Manuel de Macedo contou em cinco tempos. Um: o fidalgo gosta da sua casa e avisa o juiz aposentador. Dois: o juiz manda o oficial. Três: o oficial escreve P. R. a giz."),
    ("N008", 2, False, "Quatro: você sai em vinte e quatro horas. Cinco: o fidalgo entra e fica, diz o cronista, muito à vontade. Você acabou de ver o único processo do Brasil que anda em um dia."),
    ("N009", 2, False, "Você protesta. Mas quem despeja você é o mesmo governo que julga o seu protesto. Versão provável: você dorme na cadeia e perde a casa do mesmo jeito. Rebobina. Versão com sorte: você entrega a chave sorrindo, como muito comerciante rico fez, de olho num título de nobreza."),
    ("N010", 2, False, "A casa vai mobiliada, com a sua cama, a sua mesa e a sua moringa. Quem entra é um conde de peruca. Ele aprova a sala, olha para você e promete: Pago o aluguel estipulado. Você anota essa frase. Ela volta."),
    # 3 · Seu degrau (2:30–4:30)
    ("N011", 3, False, "E se você está gostando, se inscreve no canal antes que o Despachante chame a sua senha."),
    ("N012", 3, True, "Agora você está na calçada, com uma trouxa. Hora de você ver em que degrau caiu. Lá em cima, você vê a família real e umas mil pessoas da corte, que escolhem casa como você escolhe pão na padaria."),
    ("N013", 3, False, "Logo abaixo, os grandes negociantes. Pelas contas do inglês John Luccock, que morou aqui, eram só quarenta. Esses trocam casa por medalha e ainda agradecem. Você não tem medalha. Você tem uma trouxa."),
    ("N014", 3, False, "No meio, você: livre, sem título e sem casa. Luccock contou umas quatro mil casas para sessenta mil moradores. Dá quinze pessoas por casa. E você reclamando do colega de apartamento."),
    ("N015", 3, True, "Abaixo de você está o degrau que não tem graça nenhuma. Na conta de Luccock, doze mil moradores da cidade eram escravizados, e o censo de mil oitocentos e vinte e um conta quase metade dos moradores nessa condição."),
    ("N016", 3, False, "Eram eles que carregavam a água, a carga do porto e a sujeira das casas, sem salário e sem direito a nada. E, com a corte, o porto do Rio passou a receber, em média, mais de vinte mil africanos escravizados por ano."),
    ("N017", 3, True, "Você precisa de um teto. Plano A: a segunda casa do seu primo. Não dá. Uma das primeiras ordens do príncipe proíbe ter duas casas na cidade. A segunda casa do seu primo já é a primeira de um desembargador."),
    ("N018", 3, False, "Plano B: você aluga um quarto. E o aluguel dispara, porque uma cidade de uns sessenta mil moradores recebe milhares de recém-chegados de uma vez. Quarto caro pede salário. Você precisa de emprego."),
    # 4 · Um dia de trabalho (4:30–6:45)
    ("N019", 4, True, "Você vira caixeiro numa loja de tecidos. E você não está sozinho: Luccock contou quatro mil caixeiros e aprendizes. O seu expediente começa antes do sol e termina quando o patrão cansa."),
    ("N020", 4, False, "E a sua loja ferve, porque Dom João abriu os portos às nações amigas. Luccock viu uns cinquenta navios mercantes na baía. Você está trabalhando na primeira grande liquidação inglesa do Brasil."),
    ("N021", 4, False, "Seis da manhã: você abre a caixa que veio de Londres. Espartilhos. Você abre a próxima: patins de gelo. O viajante John Mawe jura: mandaram patins para quem nunca viu água virar gelo."),
    ("N022", 4, False, "Oito horas: você abre mais caixas. Fogão de ferro, para o verão carioca. Lustre de cristal, para uma cidade de lamparina. E enfeite de luxo para caixão, num lugar onde, segundo Mawe, ninguém usava caixão."),
    ("N023", 4, False, "Regra de ouro: você não abre caixa na frente do freguês. E se um fidalgo perguntar dos patins, você segura assim, lâmina para baixo, e jura que é faca de cozinha."),
    ("N024", 4, False, "Duas da tarde: um nobre escolhe três peças e manda pôr na conta. Você pergunta: que conta? Ele aponta para o próprio peito. Você anota: conta do peito."),
    ("N025", 4, True, "Três anos depois, em mil oitocentos e onze, o seu freguês mais ranzinza é um bibliotecário recém-chegado de Lisboa: Luís Joaquim dos Santos Marrocos. Ele veio cuidar dos livros do rei."),
    ("N026", 4, False, "Nas cartas para o pai, ele reclama da vida na cidade. Você olha a cara dele e tem certeza: esse aí não fica. Guarda esse nome: Marrocos."),
    # 5 · O corpo (6:45–8:45)
    ("N027", 5, True, "Você aluga um quarto nos fundos de um sobrado. Primeira missão: água. Você procura um cano em casa. Não tem. Você pega um pote e vai para a fila do chafariz."),
    ("N028", 5, False, "No chafariz do Largo do Paço, você vê a água cair sobre uma cúpula e escorrer devagar, evaporando no sol. Luccock achou difícil inventar coisa pior e concluiu: no Rio não há filósofos nem economistas."),
    ("N029", 5, False, "Na fonte da Rua das Marrecas, pelo menos, você senta num banco de pedra para esperar a vez. É a avó da fila do posto de saúde."),
    ("N030", 5, True, "Você almoça carne de boi. Com a cidade lotada, tem boi que vem andando de setecentas milhas, mais de mil quilômetros. Ele espera dias no curral do único matadouro da cidade, como você na fila. O bife chega mais cansado que você."),
    ("N031", 5, False, "Se você não tem dinheiro, você come carne-seca. Prato do dia: farinha. Acompanha: mais farinha."),
    ("N032", 5, True, "Esgoto? Você procura e não existe. Cada casa junta a sujeira num barril, esvaziado todo dia ou toda semana. E quando cai uma chuva forte, o barril vai para o meio da rua, para a enxurrada levar. Você aprende rápido: no Rio de mil oitocentos e oito, chuva não é romântica."),
    ("N033", 5, False, "Em mil oitocentos e nove, o intendente de polícia, Paulo Fernandes Viana, manda arrancar as rótulas, as treliças de madeira das janelas. Era a sua sombra e a sua cortina. Como você não tem vidro, a sua janela vira vitrine, e a rua inteira vê você de ceroula."),
    ("N034", 5, False, "De noite, o seu quarto úmido é um zoológico: mosquito, barata, formiga, até escorpião. O conselho de Luccock para as picadas é ficar quieto e passar suco de limão. Você passa o limão. Você espirra."),
    # 6 · Doença e "médico" (8:45–10:45)
    ("N035", 6, True, "Placa na sua tela: FEBRE. Luccock diz que as picadas davam inchaço e febre. E o socorro que você tem é curto: para sessenta mil moradores, ele contou duzentos médicos e cirurgiões. Um para cada trezentas pessoas, e ninguém sabe ainda que o mosquito transmite doença. Só você sabe, e ninguém acredita em você."),
    ("N036", 6, False, "E tem a bexiga, como o povo chamava a varíola. Má notícia do século vinte e um: a varíola foi declarada erradicada em mil novecentos e oitenta. Se você nasceu depois disso, você provavelmente nunca tomou essa vacina. A sua vacina também foi aposentada."),
    ("N037", 6, False, "Versão provável: você pega bexiga. O cronômetro para. Apagão. Placa: TENTE DE NOVO. Rebobina. Versão com sorte: você tem só uma febre comum. E o seu tratamento é o que um conde recebeu na Bahia em mil oitocentos e nove: muito láudano, emplastro que faz bolha de propósito e dieta de água morna com caramelo."),
    ("N038", 6, False, "O seu freguês Marrocos foi além de você. Nas cartas, ele conta que tentou sanguessuga, banho de mar e choque elétrico no ouvido. Não é piada. Você paga aluguel e ainda leva choque no ouvido."),
    ("N039", 6, False, "A boa notícia para você: em mil oitocentos e onze, a corte cria a Junta da Vacina, e a vacina contra a varíola chega à cidade. Você entra na fila. De novo."),
    ("N040", 6, False, "Você sobrevive. E o seu cronômetro dá um salto, de dias para anos. Porque a sua briga agora não é com a febre. É com o conde."),
    # 7 · Clímax (10:45–13:00)
    ("N041", 7, True, "Lembra da promessa? Pago o aluguel estipulado. Passa um ano. Você cobra, educado. O conde diz que não achou outra casa boa e que paga mês que vem. Passam dois anos. Você cobra de novo. Mês que vem."),
    ("N042", 7, False, "Você acha que é exagero de roteiro? O cronista Mello Moraes conta que o Conde de Belmonte morou dez anos na casa nova de um morador sem pagar aluguel, enquanto o dono se apertava com a família numa casinha ao lado."),
    ("N043", 7, False, "E a duquesa de Cadaval ficou uns dez anos na chácara de um coronel. Quando ele pediu a casa de volta, ela não saiu e ofereceu seiscentos mil réis de aluguel. O coronel recusou."),
    ("N044", 7, True, "Então você tem uma ideia: construir outra casa. Versão provável: você ergue um sobrado bonito, de dois andares. Na semana seguinte, você vê o oficial chegando com o giz na mão. Você conhece esse giz."),
    ("N045", 7, False, "Rebobina. Versão com sorte: você faz o que muita gente fez e levanta uma casa térrea, baixinha, que nenhum fidalgo quer. Você ganha, e a coroa reage: em mil oitocentos e onze, dá até vinte anos sem imposto a quem fizer sobrado nos terrenos de pântano."),
    ("N046", 7, False, "Resumo: para ter casa, você precisa morar no brejo. E o brejo, você já sabe, é a capital do mosquito."),
    ("N047", 7, True, "Até que, em mil oitocentos e dezoito, você vê Dom João ser aclamado rei aqui no Rio. E, de presente, dá aos moradores da cidade o privilégio de não ter a casa tomada. Precisou o príncipe virar rei para a sua porta ficar em paz."),
    ("N048", 7, False, "Em mil oitocentos e vinte e um, as Cortes de Lisboa abolem as aposentadorias de vez, e o rei volta para Portugal. O seu conde vai junto. Você recebe a chave, abre a porta e procura a sua cama. A cama, essa, foi com o conde."),
    ("N049", 7, False, "E o Marrocos, o ranzinza que você jurou que não ficava? Ficou. Quando a corte vai embora, ele continua no Rio cuidando dos livros, até o fim da vida, em mil oitocentos e trinta e oito. Virou carioca de teimoso."),
    # 8 · Veredito + gancho (13:00–13:45)
    ("N050", 8, True, "Placar final. VOCÊ DUROU: treze anos fora da sua casa. O recorde da série é seu, porque esta foi a primeira senha. E você voltou para casa, ainda que sem cama."),
    ("N051", 8, False, "Hoje, a antiga Rua Direita, onde você morava, se chama Primeiro de Março, e o governo bate na sua porta por aplicativo. Mas o apelido do povo durou mais de duzentos anos: você aí, sinceramente, lê P. R. como Príncipe Regente?"),
    ("N052", 8, False, "O Despachante do Tempo olha a prancheta. Próxima senha!"),
]


def palavras(t):
    return len(re.sub(r"\[[^]]*\]", "", t).split())


def main():
    out = [{"id": i, "texto": t, "ideia": ideia, "passo": p} for i, p, ideia, t in BLOCOS]
    (AQUI / "blocos.json").write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8")
    nomes = {1: "Arremesso", 2: "Chegada: onde você caiu", 3: "Seu degrau", 4: "Um dia de trabalho",
             5: "O corpo: comida, água, sujeira", 6: "Doença e \"médico\"", 7: "Clímax", 8: "Veredito + gancho"}
    linhas, acum, atual = [TOPO], 0, None
    for i, p, ideia, t in BLOCOS:
        if p != atual:
            atual = p
            ini = acum / PPM * 60
            linhas.append(f"\n## {p}. {nomes[p]} (início estimado {int(ini // 60)}:{int(ini % 60):02d})\n")
        acum += palavras(t)
        linhas.append(f"**{i}**{' · IDEIA' if ideia else ''} — {t}\n")
    tot = sum(palavras(t) for *_, t in BLOCOS)
    linhas.append(f"\n---\nTotal: {tot} palavras · {len(BLOCOS)} blocos · ~{tot / PPM:.1f} min a {PPM} ppm\n")
    (AQUI / "SCRIPT.md").write_text("\n".join(linhas), encoding="utf-8")
    print(tot, "palavras", f"{tot / PPM:.2f} min")


if __name__ == "__main__":
    main()
