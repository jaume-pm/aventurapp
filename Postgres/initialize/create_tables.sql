CREATE SCHEMA IF NOT EXISTS projecte;

CREATE TABLE IF NOT EXISTS projecte.usuaris (
    nom_usuari VARCHAR(100) PRIMARY KEY,
    nom VARCHAR(100) NOT NULL,
    contrassenya VARCHAR(100) NOT NULL
);

 CREATE TABLE IF NOT EXISTS projecte.aventurers (
            nom_usuari VARCHAR(100) PRIMARY KEY,
            FOREIGN KEY (nom_usuari) REFERENCES projecte.usuaris (nom_usuari)
            ON DELETE CASCADE ON UPDATE CASCADE
);

 CREATE TABLE IF NOT EXISTS projecte.ocasionals (
            nom_usuari VARCHAR(100) PRIMARY KEY,
            FOREIGN KEY (nom_usuari) REFERENCES projecte.usuaris (nom_usuari)
            ON DELETE CASCADE ON UPDATE CASCADE
);

CREATE TABLE IF NOT EXISTS projecte.poblacions (
    nom_poblacio VARCHAR(100) PRIMARY KEY,
    comarca VARCHAR(100),
    altitud integer,
    poblacio integer
);

CREATE TABLE IF NOT EXISTS projecte.llistes (
    codi_llista SERIAL PRIMARY KEY,
    titol VARCHAR(100) NOT NULL
);

CREATE TABLE IF NOT EXISTS projecte.estatiques (
    codi_llista SERIAL PRIMARY KEY,
    FOREIGN KEY (codi_llista) REFERENCES projecte.llistes(codi_llista)
    ON DELETE CASCADE ON UPDATE CASCADE
);

CREATE TABLE IF NOT EXISTS projecte.personalitzades (
    codi_llista SERIAL PRIMARY KEY,
    nom_usuari VARCHAR(100) NOT NULL,
    FOREIGN KEY (codi_llista) REFERENCES projecte.llistes(codi_llista)
    ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (nom_usuari) REFERENCES projecte.usuaris(nom_usuari)
    ON DELETE RESTRICT ON UPDATE CASCADE
);

CREATE TABLE IF NOT EXISTS projecte.continguts (
    codi_llista SERIAL,
    nom_poblacio VARCHAR(100) NOT NULL,
    FOREIGN KEY (codi_llista) REFERENCES projecte.llistes(codi_llista)
    ON DELETE RESTRICT ON UPDATE CASCADE,
    FOREIGN KEY (nom_poblacio) REFERENCES projecte.poblacions(nom_poblacio)
    ON DELETE RESTRICT ON UPDATE CASCADE,
    PRIMARY KEY (codi_llista, nom_poblacio)
);

CREATE TABLE IF NOT EXISTS projecte.subscripcions_aventurers (
    nom_usuari VARCHAR(100) NOT NULL,
    codi_llista SERIAL NOT NULL,
    PRIMARY KEY (nom_usuari, codi_llista),
    FOREIGN KEY (nom_usuari) REFERENCES projecte.usuaris(nom_usuari)
    ON DELETE RESTRICT ON UPDATE CASCADE,
    FOREIGN KEY (codi_llista) REFERENCES projecte.llistes(codi_llista)
    ON DELETE RESTRICT ON UPDATE CASCADE
);

CREATE TABLE IF NOT EXISTS projecte.subscripcions_ocasionals (
    nom_usuari VARCHAR(100) NOT NULL,
    codi_llista SERIAL NOT NULL,
    PRIMARY KEY (nom_usuari, codi_llista),
    FOREIGN KEY (nom_usuari) REFERENCES projecte.usuaris(nom_usuari)
    ON DELETE RESTRICT ON UPDATE CASCADE,
    FOREIGN KEY (codi_llista) REFERENCES projecte.llistes(codi_llista)
    ON DELETE RESTRICT ON UPDATE CASCADE
);

CREATE TABLE IF NOT EXISTS projecte.viatges (
    codi_viatge SERIAL PRIMARY KEY,
    nom_usuari VARCHAR(100) NOT NULL,
    codi_llista SERIAL NOT NULL,
    FOREIGN KEY (nom_usuari) REFERENCES projecte.usuaris(nom_usuari)
    ON DELETE RESTRICT ON UPDATE CASCADE,
    FOREIGN KEY (codi_llista) REFERENCES projecte.llistes(codi_llista)
    ON DELETE RESTRICT ON UPDATE CASCADE
);
