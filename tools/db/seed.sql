SET search_path=youtube;
INSERT INTO canais(slug,nome,idioma,nicho,status) VALUES
 ('lotr-fr','Le Gardien de Valinor','fr','lore de Tolkien','ativo'),
 ('historia-ptbr','(canal antigo do Rodrigo)','pt-BR','história mundial','preparacao')
ON CONFLICT (slug) DO NOTHING;
INSERT INTO videos(canal_slug,numero,titulo,status,pasta,youtube_id,publicado_em,duracao_s) VALUES
 ('lotr-fr',0,'Sam e a viagem ao Oeste (piloto)','arquivado','canais/lotr-fr/videos/000-piloto-sam',NULL,NULL,61),
 ('lotr-fr',1,'Quelles étaient les plus grandes villes de la Terre du Milieu ?','publicado','canais/lotr-fr/videos/001-maiores-cidades','87BdomKxa-M','2026-11-02',499)
ON CONFLICT (canal_slug,numero) DO NOTHING;
