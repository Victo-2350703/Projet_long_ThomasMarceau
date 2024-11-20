DROP DATABASE IF EXISTS pizzeria;
CREATE DATABASE IF NOT EXISTS pizzeria;
USE pizzeria;

CREATE TABLE croutes(
id 	INT PRIMARY KEY AUTO_INCREMENT,
nom VARCHAR(255) NOT NULL
);

CREATE TABLE garnitures(
id 	INT PRIMARY KEY AUTO_INCREMENT,
nom VARCHAR(255)NOT NULL
);

CREATE TABLE sauces(
id 	INT PRIMARY KEY AUTO_INCREMENT,
nom VARCHAR(255) NOT NULL
);

CREATE TABLE pizzas (
id 	INT PRIMARY KEY AUTO_INCREMENT,
id_croute INT NOT NULL,
FOREIGN KEY (id_croute) REFERENCES croutes (id)
);

CREATE TABLE garniture_pizzas(
id_pizza INT,
id_garniture INT,
FOREIGN KEY (id_pizza) REFERENCES pizzas (id),
FOREIGN KEY (id_garniture) REFERENCES garnitures (id)
);

CREATE TABLE sauce_pizzas(
id_pizza INT,
id_sauce INT,
FOREIGN KEY (id_pizza) REFERENCES pizzas (id),
FOREIGN KEY (id_sauce) REFERENCES sauces (id)
);

CREATE TABLE clients(
id 	INT PRIMARY KEY AUTO_INCREMENT,
nom VARCHAR(255),
numero_telephone INT,
adresse VARCHAR(255)
);

CREATE TABLE commandes(
id 	INT PRIMARY KEY AUTO_INCREMENT,
id_pizza INT,
id_client INT,
FOREIGN KEY (id_pizza) REFERENCES pizzas (id),
FOREIGN KEY (id_client) REFERENCES clients (id)
);

CREATE TABLE liste_commandes_en_attentes(
id_commande INT,
FOREIGN KEY (id_commande) REFERENCES commandes (id)
);