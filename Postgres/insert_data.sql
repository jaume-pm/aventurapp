



INSERT INTO projecte.usuaris (nom_usuari, nom, contrassenya)
VALUES ('john_doe', 'John Doe', 'password123');


INSERT INTO projecte.aventurers (nom_usuari)
VALUES ('john_doe');


INSERT INTO projecte.ocasionals (nom_usuari)
VALUES ('jane_smith');


INSERT INTO projecte.poblacions (nom_poblacio, comarca, altitud, poblacio)
VALUES ('Barcelona', 'Barcelona', 50, 5000000);


INSERT INTO projecte.llistes (titol)
VALUES ('Favorite Places');


INSERT INTO projecte.estatiques (codi_llista)
VALUES (1);


INSERT INTO projecte.personalitzades (codi_llista, nom_usuari)
VALUES (2, 'jane_smith');


INSERT INTO projecte.continguts (codi_llista, nom_poblacio)
VALUES (1, 'Barcelona');


INSERT INTO projecte.subscripcions_aventurers (nom_usuari, codi_llista)
VALUES ('john_doe', 1);


INSERT INTO projecte.subscripcions_ocasionals (nom_usuari, codi_llista)
VALUES ('jane_smith', 2);


INSERT INTO projecte.viatges (nom_usuari, codi_llista)
VALUES ('john_doe', 1);
