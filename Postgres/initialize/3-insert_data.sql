


--- Indiana Jone's information ---

INSERT INTO projecte.usuaris (nom_usuari, nom, contrassenya)
VALUES ('Indiana22', 'Indiana Jones', 'Skull1234');

INSERT INTO projecte.aventurers (nom_usuari)
VALUES ('Indiana22');

INSERT INTO projecte.llistes (titol)
VALUES ('Towns with hidden treasures!');

INSERT INTO projecte.personalitzades (codi_llista, nom_usuari)
VALUES (1, 'Indiana22');

INSERT INTO projecte.continguts (codi_llista, nom_poblacio)
VALUES (1, 'Sant Jaume de Frontanyà');

INSERT INTO projecte.continguts (codi_llista, nom_poblacio)
VALUES (1, 'Savallà del Comtat');

INSERT INTO projecte.continguts (codi_llista, nom_poblacio)
VALUES (1, 'Capafonts');

INSERT INTO projecte.continguts (codi_llista, nom_poblacio)
VALUES (1, 'Gaià');

INSERT INTO projecte.continguts (codi_llista, nom_poblacio)
VALUES (1, 'Molló');


INSERT INTO projecte.llistes (titol)
VALUES ('Towns with mysterious churches');

INSERT INTO projecte.personalitzades (codi_llista, nom_usuari)
VALUES (2, 'Indiana22');

INSERT INTO projecte.continguts (codi_llista, nom_poblacio)
VALUES (2, 'Viladamat');

INSERT INTO projecte.continguts (codi_llista, nom_poblacio)
VALUES (2, 'Sant Ramon');

INSERT INTO projecte.continguts (codi_llista, nom_poblacio)
VALUES (2, 'Capafonts');

INSERT INTO projecte.continguts (codi_llista, nom_poblacio)
VALUES (2, 'Cabacés');

INSERT INTO projecte.continguts (codi_llista, nom_poblacio)
VALUES (2, 'Massoteres');

INSERT INTO projecte.continguts (codi_llista, nom_poblacio)
VALUES (2, 'Prades');

INSERT INTO projecte.continguts (codi_llista, nom_poblacio)
VALUES (2, 'Meranges');



--- Mike's information ---

INSERT INTO projecte.usuaris (nom_usuari, nom, contrassenya)
VALUES ('Mike1', 'Mike McMiller', 'MikeIsTheBest!');

INSERT INTO projecte.aventurers (nom_usuari)
VALUES ('Mike1');

INSERT INTO projecte.llistes (titol)
VALUES ('Most beautiful cities!');

INSERT INTO projecte.personalitzades (codi_llista, nom_usuari)
VALUES (3, 'Mike1');

INSERT INTO projecte.continguts (codi_llista, nom_poblacio)
VALUES (3, 'Vic');

INSERT INTO projecte.continguts (codi_llista, nom_poblacio)
VALUES (3, 'Figueres');

INSERT INTO projecte.continguts (codi_llista, nom_poblacio)
VALUES (3, 'Mataró');

INSERT INTO projecte.continguts (codi_llista, nom_poblacio)
VALUES (3, 'Castelldefels');

--- Sarah's information ---

INSERT INTO projecte.usuaris (nom_usuari, nom, contrassenya)
VALUES ('Sarah21', 'Sarah Williams', '??Ruffus82938??');

INSERT INTO projecte.aventurers (nom_usuari)
VALUES ('Sarah21');

INSERT INTO projecte.llistes (titol)
VALUES ('Astonishing coastal towns!');

INSERT INTO projecte.personalitzades (codi_llista, nom_usuari)
VALUES (4, 'Sarah21');

INSERT INTO projecte.continguts (codi_llista, nom_poblacio)
VALUES (4, 'Sitges');

INSERT INTO projecte.continguts (codi_llista, nom_poblacio)
VALUES (4, 'Llançà');

INSERT INTO projecte.continguts (codi_llista, nom_poblacio)
VALUES (4, 'Roses');

INSERT INTO projecte.continguts (codi_llista, nom_poblacio)
VALUES (4, 'Calella');


-- Estatiques information --

INSERT INTO projecte.llistes (titol)
VALUES ('Favorite Places');

INSERT INTO projecte.estatiques (codi_llista)
VALUES (5);



-- John Doe's information --

INSERT INTO projecte.usuaris (nom_usuari, nom, contrassenya)
VALUES ('John271', 'John Doe', 'WhyIsMyNameEverywhere?8775');
INSERT INTO projecte.ocasionals (nom_usuari)
VALUES ('John271');


-- Mile's information --

INSERT INTO projecte.usuaris (nom_usuari, nom, contrassenya)
VALUES ('Miles52', 'Miles Morales', 'IAmSpiderman33!');
INSERT INTO projecte.ocasionals (nom_usuari)
VALUES ('Miles52');



-- INSERT INTO projecte.llistes (titol)
-- VALUES ('Favorite Places');

-- INSERT INTO projecte.estatiques (codi_llista)
-- VALUES (1);


-- INSERT INTO projecte.subscripcions_aventurers (nom_usuari, codi_llista)
-- VALUES ('john_doe', 1);


-- INSERT INTO projecte.subscripcions_ocasionals (nom_usuari, codi_llista)
-- VALUES ('jane_smith', 2);


-- INSERT INTO projecte.viatges (nom_usuari, codi_llista)
-- VALUES ('john_doe', 1);