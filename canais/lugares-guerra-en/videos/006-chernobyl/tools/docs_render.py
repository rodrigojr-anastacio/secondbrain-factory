import pymupdf, json, os, sys
V=os.path.expanduser('~/workspace/fabrica-youtube/canais/lugares-guerra-en/videos/006-chernobyl')
OUT=V+'/midia'
H=os.path.expanduser('~/cache/tmp/chdl/')
T=os.path.expanduser('~/cache/tmp/ch67/')
pos={}
def rects(page,phrase):
    return [[round(r.x0,1),round(r.y0,1),round(r.width,1),round(r.height,1)] for r in page.search_for(phrase)]
def union(rs):
    x0=min(r[0] for r in rs); y0=min(r[1] for r in rs)
    x1=max(r[0]+r[2] for r in rs); y1=max(r[1]+r[3] for r in rs)
    return [round(x0,1),round(y0,1),round(x1-x0,1),round(y1-y0,1)]
def row(page,tphrase,nextphrase,x1=None,occ=0):
    a=page.search_for(tphrase)[occ]
    b=[r for r in page.search_for(nextphrase) if r.y0>a.y0+1][0] if nextphrase else None
    xr=x1 or page.rect.width-35
    y1=b.y0-1 if b is not None else a.y1+10
    return [round(a.x0-3,1),round(a.y0-2,1),round(xr-a.x0,1),round(y1-a.y0+2,1)]
def render(src,pg,name,zoom,frases):
    d=pymupdf.open(src); p=d[pg-1]
    pix=p.get_pixmap(matrix=pymupdf.Matrix(zoom,zoom),alpha=False)
    pix.save(f'{OUT}/{name}')
    pos[name]={'pagina_pt':[round(p.rect.width,2),round(p.rect.height,2)],'frases':{k:(v(p) if callable(v) else v) for k,v in frases.items()},'zoom':zoom,'png_px':[pix.width,pix.height],'fonte':os.path.basename(src),'pagina_pdf':pg}
    print(name,pix.width,pix.height)
Z=4.2
render(H+'insag7.pdf',63,'doc_insag7_p63_tabela-I-I-25abr.png',Z,{
 'kievenergo_14h':lambda p:[row(p,'Postponement of testing','15:20')],
 'eccs_14h':lambda p:[row(p,'Disconnection of the ECCS','Postponement')],
 'power_reduction_0106':lambda p:[row(p,'Start of reactor power reduction','03:45')],
 'potencia_30MW':lambda p:rects(p,'reduction in thermal power to 30 MW') or rects(p,'30 MW'),
})
render(H+'insag7.pdf',64,'doc_insag7_p64_tabela-I-I-0122-0123.png',Z,{
 'orm_8_barras':lambda p:rects(p,'ORM proved to be equal to 8 manual')+rects(p,'control rods)'),
 '0122_30':lambda p:rects(p,'01:22:30'),
 '0123_04':lambda p:rects(p,'01:23:04'),
 'oscilloscope_valves':lambda p:rects(p,'closed. The rundown was started'),
})
def p65(p):
    return {}
render(H+'insag7.pdf',65,'doc_insag7_p65_tabela-I-I-0123-40.png',Z,{
 'eps5_0123_40':lambda p:[row(p,'01:23:40','01:23:43')],
 'eps5_texto':lambda p:rects(p,'EPS-S button was pressed'),
 'teletape_0123_39':lambda p:rects(p,'on teletape)')+rects(p,'(01:23:39'),
 'dba_0123_10':lambda p:[row(p,'01:23:10','01:23:30')],
 'excursion_0123_43':lambda p:[row(p,'01:23:43','01:23:46')],
 'mw_530':lambda p:rects(p,'power exceeded 530 MW(th)'),
 'ultimo_sinal_0123_49':lambda p:[row(p,'01:23:49','From a note')],
 'severe_shocks':lambda p:[union(rects(p,'"01:24: Severe shocks; the RCPS rods stopped moving before they')+rects(p,'reached the lower limit stop switches; power switch of clutch')+rects(p,'mechanisms is off'))],
 'severe_shocks_frase':lambda p:rects(p,'Severe shocks'),
})
render(H+'insag7.pdf',76,'doc_insag7_p76_unable-to-establish-why.png',Z,{
 'unable_to_establish':lambda p:rects(p,'The Commission was unable to establish why the button was pressed.') or rects(p,'unable to establish why'),
 'eps5_0123_40':lambda p:rects(p,'At 01:23:40 the senior reactor control engineer pressed the manual emergency')+rects(p,'stop button (EPS-5).'),
})
render(H+'insag7.pdf',122,'doc_insag7_p122_tabela-II-III-25abr.png',Z,{
 'kievenergo_14h':lambda p:[row(p,'ECCS isolated','15:20')],
})
render(H+'insag7.pdf',123,'doc_insag7_p123_tabela-II-III-margem-reatividade.png',Z,{
 'margem_6_8_barras':lambda p:rects(p,'yielded an ORM value of 6-8 manual')+rects(p,'control rods')[-1:],
 'orm_6_8':lambda p:rects(p,'6-8 manual'),
 'orm_1_9':lambda p:rects(p,'1.9 manual control rods'),
 'dba_button':lambda p:rects(p,'the DBA button was pressed'),
 '0122_30':lambda p:rects(p,'01:22:30'),
})
render(H+'insag7.pdf',124,'doc_insag7_p124_tabela-II-III-0123-40-e-0124.png',Z,{
 'eps5_0123_40':lambda p:[row(p,'01:23:40','01:23:43')],
 'severe_shocks':lambda p:[row(p,'01:24','1 A DBA button')],
 'severe_shocks_frase':lambda p:rects(p,'Severe shocks recorded'),
})
render(H+'insag7.pdf',125,'doc_insag7_p125_fitas-de-telefone-II-2-3-4.png',Z,{
 'tape_recordings_telephone':lambda p:rects(p,'tape recordings of')+rects(p,'telephone calls made by personnel'),
})
render(H+'insag7.pdf',126,'doc_insag7_p126_duas-explosoes-testemunhas.png',Z,{
 'two_explosions':lambda p:rects(p,'there had been two explosions') or rects(p,'two explosions') or rects(p,'majority of people reported'),
 'minimo_15_barras':lambda p:rects(p,'minimum permissible level'),
 'accounts_inaccurate':lambda p:rects(p,'highly inaccurate'),
})
# Politburo NSArchive (letter 612x792)
Zp=3.1
render(H+'polit.pdf',1,'doc_politburo-28abr_p1_dolgikh-0130.png',Zp,{
 'dolgikh_1_30am':lambda p:rects(p,'On April 26, at 1:30 a.m. there was an explosion at the')+rects(p,'1:30 a.m.'),
 'populacao_45000':lambda p:rects(p,'Out of the 45,000 residents')+rects(p,'only 5,000 who service the'),
})
render(H+'polit.pdf',3,'doc_politburo-28abr_p3_gorbachev-statement.png',Zp,{
 'gorbachev_statement_quickly':lambda p:rects(p,'We should issue a statement quickly, we must not')+rects(p,'delay.'),
 'gorbachev_issue_statement':lambda p:rects(p,'We should issue a statement quickly'),
 'gromyko_panic':lambda p:rects(p,'does not cause excessive anxiety or panic.')+rects(p,'The statement should be written in such a way that it'),
 'dobrynin_americans':lambda p:rects(p,'The Americans will notice the fact of the explosion and')+rects(p,'the spread of the radioactive cloud anyway.'),
})
render(T+'gorby.pdf',3,'doc_politburo-28abr_ru_gorbachev-soobshchenie.png',3.2,{
 'gorbachev_bystree_soobshchenie':lambda p:rects(p,'Надо быстрее дать сообщение'),
})
# Wilson scans
Zs=4.9
render(T+'scan208406.pdf',1,'doc_wilson208406_p1_ministerstvo-avtotransporta-2000.png',Zs,{
 'sinal_2000_26abr':[[78,205,305,28]],
 'ordem_masik':[[95,177,295,25]],
 'secreto':[[302,96,37,16]],
 'numero_data_382s':[[99,102,112,11]],
 'coluna_2325':[[103,385,272,18]],
 'ministerstvo_cabecalho':[[80,30,300,40]],
})
render(T+'scan208406.pdf',2,'doc_wilson208406_p2_lista-de-onibus.png',Zs,{})
render(T+'scan208406.pdf',3,'doc_wilson208406_p3_1125-onibus-250-caminhoes.png',Zs,{
 '1330_evacuacao':[[74,147,285,19]],
 '1125_onibus':lambda p:rects(p,'1125'),
 '250_caminhoes':lambda p:rects(p,'250'),
})
render(T+'scan208405.pdf',1,'doc_wilson208405_bryukhanov-0125.png',Zs,{
 'explosao_0125':[[60,188,270,10]],
 'incendio_0450_0600':[[47,243,290,20]],
 'pripyat_normal':[[47,431,265,20]],
 'secreto_ex3':[[257,37,37,12]],
})
Zw=3.1
render(T+'frus.pdf',1,'doc_frus-v05-d220_cia-29abr.png',Zw,{
 'possibly_occurred_last_friday':lambda p:rects(p,'possibly occurred last Friday'),
 'cabecalho_cia':lambda p:rects(p,'Central Intelligence Agency')+rects(p,'SPOT COMMENTARY'),
})
render(T+'upi.pdf',1,'doc_upi-28abr1986_p1_titulo-dateline.png',Zw,{
 'titulo':lambda p:rects(p,'Soviets say reactor damaged in Ukraine nuclear accident'),
 'dateline_28abr':lambda p:rects(p,'April 28, 1986'),
})
render(T+'upi.pdf',2,'doc_upi-28abr1986_p2_tass-announcement.png',Zw,{
 'aid_is_being_given':lambda p:rects(p,'Aid is being given'),
 'tass_announcement':lambda p:rects(p,'Tass announcement'),
})
render(T+'upi.pdf',4,'doc_upi-28abr1986_p4_forsmark.png',Zw,{
 'forsmark_alarm':lambda p:rects(p,'Forsmark'),
 '600_employees':lambda p:rects(p,'600 employees'),
})
json.dump(pos,open(V+'/tools/docs_pos.json','w'),indent=1,ensure_ascii=False)
