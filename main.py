import requests
from bs4 import BeautifulSoup
import mysql.connector
from mysql.connector import Error
from func import getInfos, getIngredients, getSteps, print_recipe
from db import insert_ingredients, insert_recipe, insert_steps

class Receita:
    def __init__(self=None, title=None, portion=None, ingredients=[], time=None, steps=[], hasIParts=None, hasSParts=None, nameIParts=None, nameSParts=None):
        self.title = title
        self.ingredients = ingredients
        self.portion = portion
        self.time = time
        self.steps = steps
        self.hasIParts = hasIParts
        self.nameIParts = nameIParts
        self.hasSParts = hasSParts
        self.nameSParts = nameSParts
    def __str__(self):
        return f"""
        Título: {self.title}
        Porção: {self.portion}
        Tempo: {self.time}
        Tem Partes: {self.hasParts}

        Qtd de listas de ingredientes: {len(self.ingredients)}
        Ingredientes:
        {self.ingredients}
        
        Qtd de listas de preparo: {len(self.steps)}
        Modo de Preparo:
        {self.steps}
        """

    def formatar_lista(self, lista):
        i = 1
        resultado = ""
        for step in lista:
            if len(step) != 0:
                resultado += "===================\n"
                for x in step:
                    resultado += f"{i}: {x}\n"
                    i += 1
        return resultado

class LinkReceita:
    def __init__(self, id, url):
        self.id = id
        self.url = url
                
#Conexão com o MySQL
host="192.168.100.175"
port=3306
database="recipes"
user="italogvss"
password="narutoeb0m"
connection = mysql.connector.connect(database=database, host=host, port=port, user=user, password=password) 
cur = connection.cursor()
cur.execute("SELECT * FROM link LIMIT 30 ")
result = cur.fetchall()

urls = [resultado[1] for resultado in result]

for row in urls:
    URL = row
    print("Acessando: "+URL)
    site = requests.get(URL)
    soup = BeautifulSoup(site.content, 'html.parser')

    receita = Receita()
    
    getInfos(soup, receita)

    getIngredients(soup, receita)

    getSteps(soup, receita)

    #print(receita.ingredients)
    if(receita.hasIParts or receita.hasSParts):
        print_recipe(receita)
    
    insert_recipe(cur, receita)

    insert_ingredients(cur, receita)

    insert_steps(cur, receita)



  