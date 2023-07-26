COPY projecte.poblacions(nom_poblacio, comarca, altitud, poblacio)
FROM '/docker-entrypoint-initdb.d/poblacions.csv'
DELIMITER ';'
CSV HEADER;