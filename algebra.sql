-- 1. Liste o título de todas as músicas e suas durações.
SELECT título, duração FROM música;

--2. Encontre o nome de todos os artistas que têm mais de 5 músicas em seu repertório.
SELECT a.nome_artista
FROM artista a
JOIN música_artista ma ON a.id_artista = ma.id_artista
GROUP BY a.nome_artista
HAVING COUNT(ma.id_música) > 5;
--*TESTAR COM ">2"*

--3. Quais são os títulos dos discos lançados após 2020?
SELECT título
FROM disco
WHERE disco.lançamento_ano > '2019';

--4. Liste os títulos das músicas e os nomes dos artistas que as interpretam, ordenados pelo título da música.
SELECT título, nome_artista
FROM música
JOIN música_artista ON música.id_música = música_artista.id_música
JOIN artista ON música_artista.id_artista = artista.id_artista
ORDER BY música.título;

--5. Encontre os títulos das playlists que contêm a música com o título 'Imagine'.
SELECT p.título
FROM playlist p
JOIN playlist_música pm ON p.id_playlist = pm.id_playlist
JOIN música m ON pm.id_música = m.id_música
WHERE m.título = 'Imagine';
--*TESTAR COM ALGUMA MÚSICA QUE EXISTA NUMA PLAYLIST QUALQUER*

--6. Liste os usuários que criaram playlists que contêm músicas do disco 'Abbey Road'.
SELECT DISTINCT u.nome_usuário
FROM usuário u
JOIN playlist p ON u.id_usuário = p.id_usuário
JOIN playlist_música pm ON p.id_playlist = pm.id_playlist
JOIN música m ON pm.id_música = m.id_música
JOIN disco d ON m.id_disco = d.id_disco
WHERE d.título = 'Abbey Road';

--7. Qual é a duração média das músicas de um artista específico?
SELECT AVG(m.duração) AS duracao_media
FROM música m
JOIN música_artista ma ON m.id_música = ma.id_música
WHERE ma.id_artista = 1;
--*TROCAR <id_artista> POR UM NÚMERO DE 1 A 30

--8. Encontre todos os artistas que não têm músicas.
SELECT a.nome_artista
FROM artista a
LEFT JOIN música_artista ma ON a.id_artista = ma.id_artista
WHERE ma.id_artista IS NULL;

--9. Liste todos os discos que contêm mais de 10 músicas.
SELECT d.título, COUNT(m.id_música) AS total_musicas
FROM disco d
JOIN música m ON d.id_disco = m.id_disco
GROUP BY d.id_disco, d.título
HAVING COUNT(m.id_música) > 10;

--10. Quais são os nomes dos artistas que têm discos lançados antes de 2010 e que têm músicas na playlist 'Top 50'?
SELECT DISTINCT a.nome_artista
FROM artista a
JOIN disco d ON a.id_artista = d.id_artista
JOIN música m ON d.id_disco = m.id_disco
JOIN playlist_música pm ON m.id_música = pm.id_música
JOIN playlist p ON pm.id_playlist = p.id_playlist
WHERE d.lançamento_ano < '2010' AND p.título = 'Top 50';

--11. Quais músicas são interpretadas por mais de um artista?
SELECT m.título, COUNT(ma.id_artista) AS total_artistas
FROM música m
JOIN música_artista ma ON m.id_música = ma.id_música
GROUP BY m.id_música, m.título
HAVING COUNT(ma.id_artista) > 1;

--12. Liste os títulos das músicas que aparecem em mais de uma playlist.
SELECT m.título, COUNT(pm.id_playlist) AS total_playlists
FROM música m
JOIN playlist_música pm ON m.id_música = pm.id_música
GROUP BY m.id_música, m.título
HAVING COUNT(pm.id_playlist) > 1

--13. Encontre os nomes dos usuários que têm playlists que incluem a música 'Bohemian Rhapsody'.
SELECT DISTINCT u.nome_usuário
FROM usuário u
JOIN playlist p ON u.id_usuário = p.id_usuário
JOIN playlist_música pm ON p.id_playlist = pm.id_playlist
JOIN música m ON pm.id_música = m.id_música
WHERE m.título = 'Bohemian Rhapsody';

--14. Qual é o título da música mais longa do disco 'Dark Side of the Moon'?
SELECT m.título
FROM música m
JOIN disco d ON m.id_disco = d.id_disco
WHERE d.título = 'Dark Side of the Moon'
ORDER BY m.duração DESC
LIMIT 1;

--15. Liste todos os discos lançados por um artista específico em um determinado ano.
SELECT d.título, d.lançamento_ano
FROM disco d
JOIN artista a ON d.id_artista = a.id_artista
WHERE a.id_artista = 2 AND d.lançamento_ano = '2020';

--16. Quais são os nomes dos artistas que têm músicas em playlists criadas por um usuário específico?
SELECT DISTINCT nome_usuário
FROM usuário u
JOIN playlist p ON u.id_usuário = p.id_usuário
JOIN playlist_música pm ON p.id_playlist = pm.id_playlist
JOIN música m ON pm.id_música = m.id_música
JOIN música_artista ma ON m.id_música = ma.id_música
JOIN artista a ON ma.id_artista = a.id_artista
WHERE u.id_usuário = 1;
--*TROCAR <id_artista> POR UM NÚMERO DE 1 A 30

--17. Encontre a lista de músicas que não estão em nenhuma playlist.
SELECT m.título
FROM música m
LEFT JOIN playlist_música pm ON m.id_música = pm.id_música
WHERE pm.id_playlist IS NULL;

--18. Liste os títulos das músicas e os nomes dos artistas que têm mais de 3 músicas em uma mesma playlist.
SELECT m.título, a.nome_artista
FROM música m
JOIN música_artista ma ON m.id_música = ma.id_música
JOIN artista a ON ma.id_artista = a.id_artista
JOIN playlist_música pm ON m.id_música = pm.id_música
JOIN playlist p ON pm.id_playlist = p.id_playlist
WHERE p.id_playlist IN (
    SELECT pm.id_playlist
    FROM playlist_música pm
    GROUP BY pm.id_playlist
    HAVING COUNT(pm.id_música) > 3
);

--19. Quais são os discos que contêm músicas de artistas que têm pelo menos 2 discos lançados?
SELECT DISTINCT d.título
FROM disco d
JOIN artista a ON d.id_artista = a.id_artista
JOIN música m ON d.id_disco = m.id_disco
WHERE a.id_artista IN (
    SELECT id_artista
    FROM disco
    GROUP BY id_artista
    HAVING COUNT(id_disco) >= 2
);

--20. Liste todos os usuários e suas playlists, mas apenas para playlists que contêm pelo menos 5 músicas
SELECT u.nome_usuário, p.título
FROM usuário u
JOIN playlist p ON u.id_usuário = p.id_usuário
WHERE p.id_playlist IN (
    SELECT pm.id_playlist
    FROM playlist_música pm
    GROUP BY pm.id_playlist
    HAVING COUNT(pm.id_música) >= 5
);
