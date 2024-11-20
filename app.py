import os
from dotenv import load_dotenv
from flask import Flask, render_template, request
import mysql.connector

load_dotenv()

# Récupère les variables d'environnement
db_host = os.getenv('DB_HOST')
db_user = os.getenv('DB_USER')
db_password = os.getenv('DB_PASSWORD')
db_name = os.getenv('DB_NAME')

app = Flask(__name__)

# Configuration de la connexion à la base de données
db = mysql.connector.connect(
    host=db_host,
    user=db_user,
    passwd=db_password,
    database=db_name
)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/commande_pizza')
def Commande_pizza():
    cursor = db.cursor()
    cursor.execute("SELECT * FROM croutes")
    croutes = cursor.fetchall()
    cursor.close()

    cursor = db.cursor()
    cursor.execute("SELECT * FROM sauces")
    sauces = cursor.fetchall()
    cursor.close()

    cursor = db.cursor()
    cursor.execute("SELECT * FROM garnitures")
    garnitures = cursor.fetchall()
    cursor.close()

    return render_template('commande_pizza.html', croutes=croutes,sauces=sauces,garnitures=garnitures)


@app.route('/commander_pizza', methods=['GET'])
def commander_pizza():
    
    id_croute = request.args.get('croutes')
    id_sauce = request.args.get('sauces')
    id_garniture1 = request.args.get('garnitures1')
    id_garniture2 = request.args.get('garnitures2')
    id_garniture3 = request.args.get('garnitures3')
    id_garniture4 = request.args.get('garnitures4')
    nom = request.args.get('nom')
    num = request.args.get('num')
    adresse = request.args.get('adresse')

    cursor = db.cursor()
    # Requête d'insertion croutes
    insert_query = """
        INSERT INTO pizzas (id_croute)
        VALUES (%s)
    """
    cursor.execute(insert_query, (id_croute,))
    pizza=cursor.lastrowid
    cursor.close()

    cursor = db.cursor()
    # Requête d'insertion sauce
    insert_query = """
        INSERT INTO sauce_pizzas (id_sauce,id_pizza)
        VALUES (%s, %s)
    """
    cursor.execute(insert_query, (id_sauce, pizza,))
    cursor.close()

    cursor = db.cursor()
    # Requête d'insertion garniture1
    insert_query = """
        INSERT INTO garniture_pizzas (id_garniture,id_pizza)
        VALUES (%s, %s)
    """
    cursor.execute(insert_query, (id_garniture1, pizza,))
    cursor.close()

    cursor = db.cursor()
        # Requête d'insertion garniture2
    insert_query = """
        INSERT INTO garniture_pizzas (id_garniture,id_pizza)
        VALUES (%s, %s)
    """
    cursor.execute(insert_query, (id_garniture2, pizza,))
    cursor.close()

    cursor = db.cursor()
    # Requête d'insertion garniture3
    insert_query = """
        INSERT INTO garniture_pizzas (id_garniture,id_pizza)
        VALUES (%s, %s)
    """
    cursor.execute(insert_query, (id_garniture3, pizza,))
    cursor.close()

    cursor = db.cursor()
        # Requête d'insertion garniture4
    insert_query = """
        INSERT INTO garniture_pizzas (id_garniture,id_pizza)
        VALUES (%s, %s)
    """
    cursor.execute(insert_query, (id_garniture4, pizza,))
    cursor.close()

    cursor = db.cursor()
        # Requête d'insertion clients
    insert_query = """
        INSERT INTO clients (nom,numero_telephone,adresse)
        VALUES (%s, %s,%s)
    """
    cursor.execute(insert_query, (nom, num, adresse,))
    client=cursor.lastrowid
    cursor.close()

    cursor = db.cursor()
        # Requête d'insertion commande
    insert_query = """
        INSERT INTO commandes (id_pizza,id_client)
        VALUES (%s, %s)
    """
    cursor.execute(insert_query, (pizza, client,))
    commande=cursor.lastrowid
    cursor.close()

    cursor = db.cursor()
        # Requête d'insertion liste commande en attente
    insert_query = """
        INSERT INTO liste_commandes_en_attentes (id_commande)
        VALUES (%s)
    """
    cursor.execute(insert_query, (commande,))
    cursor.close()

    
    try:
        db.commit()  # Valider la transaction 
        return render_template('commande_succes.html')
    except Exception as e:
        return render_template('commande_erreure.html')
    
    
@app.route('/liste_commandes')
def liste_commandes():
    cursor = db.cursor()
    cursor.execute("SELECT * FROM liste_commandes_en_attentes")
    data = cursor.fetchall()
    cursor.close()
    return render_template('liste_commandes.html', data=data)


@app.route('/completer_commandes')
def completer_commandes():
    commande = request.args.get('commande')

    if not commande:
        # Si le paramètre 'commande' est manquant, afficher un message d'erreur
        return render_template('completer_commandes.html', message="L'ID de la commande est requis", success=False)

    try:
        # Utiliser la connexion existante à la base de données
        cursor = db.cursor()

        # Suppression de la commande avec l'ID spécifié
        cursor.execute("DELETE FROM liste_commandes_en_attentes WHERE id_commande = ?", (commande,))
        db.commit()  # Validation de la suppression

        cursor.close()

        # Si la suppression a réussi, renvoyer un message de succès
        return render_template('completer_commandes.html', message="Commande supprimée avec succès.", success=True)

    except Exception as e:
        # En cas d'erreur, afficher un message d'erreur
        return render_template('completer_commandes.html', message=f"Erreur lors de la suppression de la commande: {e}", success=False)

if __name__ == '__main__':
    app.run(debug=True)