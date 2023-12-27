#!/usr/bin/env python3.11
# -*- coding: utf-8 -*-
"""
Created on Sun Jun  4 11:17:21 2023

@author: simon_sensei
"""
#3 lignes de code à rentrer séparément dans le terminal avant de lancer le code python
# se placer dans le repertoire Website dans le terminal avec la commande cd
#export FLASK_APP=main (nom du fichier à la place de main)
#export FLASK_ENV=development
#flask run

from flask import Flask, request
from flask_cors import CORS
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask import render_template



import openai
import os
import csv

#openai.api_key = 'insérer votre clé api ici' 





app = Flask(__name__)
limiter = Limiter(key_func=get_remote_address, app=app)


   # Utilise l'adresse IP de l'utilisateur pour le rate limiting

CORS(app)  # autorise toutes les origines pour simplifier

@app.route('/', methods=['GET', 'POST', 'OPTIONS'])
def home():
    return render_template("dream1.html")

def analyse(text):
	try :
		prompt={f"Joue le rôle d'un expert en interprétation des rêves, j'aimerais une analyse détaillée du rêve suivant : ‘{text}’. Pourrais-tu fournir une explication basée sur des études et faits psychologiques, ainsi qu'une exploration des différents symboles présents dans le rêve ? Enfin, pourrais-tu mentionner une tradition culturelle ou spirituelle qui pourrait avoir un lien avec ce rêve ? Ta réponse ne doit pas dépasser 7 phrases. "}
		response = openai.ChatCompletion.create(
    	model='gpt-3.5-turbo',
    	messages = [{'role':'user', 'content':f'{prompt}'}])
		text_analysed = response.choices[0].message.content
		return text_analysed
	except : 
		return "Erreur"


@app.route('/analyser_reve', methods=['GET', 'POST', 'OPTIONS'])
@limiter.limit("8 per day")  # Vous pouvez ajuster ces limites selon vos besoins

def hello():
	#print("ca fonctionne")
	if request.method == 'POST': #SI LA REQUETE EST BIEN EN POST
		data = request.get_json()  # Récupère les données JSON envoyées avec la requête
		if data is not None: # ET QUE LES DONNEES NE SONT PAS NULLES 
			reve = data.get('reve', '')  # ALORS la fonction récupère le texte du formulaire depuis les données JSON
			print(reve)
			# Ouverture du fichier CSV en mode écriture avec with (dès qu'on sort du with, le fichier se ferme)
			with open('data.csv', 'a', newline='',encoding='utf-8') as csvfile:
				# Création de l'objet écrivain CSV
				writer = csv.writer(csvfile)
				# Écriture des données dans le fichier CSV
				writer.writerow([reve])
			
			reve_analysed=analyse(reve)
		else : 
			reve_analysed = " " #si les données sont nulles, on affiche rien 
	else : 
		reve_analysed = " " # si la requête n'est pas en post on affiche rien 
	return f'{reve_analysed}' #le f après le return permet de mettre une variable dans la chaine de caractère qu'on renvoie






