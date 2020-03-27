import requests
from json import dump
from json import loads
import time
import csv
import datetime
import os


# Variaveis globais:
qtd_dados = 24
qtd_page = 1#if qtd_dados/10 > 0 
qtd_max_buscas = 20

api_url_base = 'https://api.github.com/graphql'

headers = {
    'Content-Type': 'application/json',
    'Authorization': 'bearer 76eda44822120be83dcaa3417e667850f01063dd',
}

query = """
    {
        user(login: "gvanrossum") {
            repositories(first:24,isFork:false) {
                nodes {
                    nameWithOwner
                    url
                    createdAt
                    updatedAt
                    releases {
                        totalCount
                    }
                    primaryLanguage {
                        name
                    }
                    forks {
                        totalCount
                    }
                }
            }
        }
    }
"""
json = {
    "query":query, "variables":{}
}

def request(json, n_consulta = 0):
    time_start = time.time()
    
    print("consulta numero: "+str(n_consulta)+"/"+str(qtd_page))
    response = requests.post(api_url_base, headers=headers, json=json)
    
    qtd_tentativas = 1
    while response.status_code != 200 and qtd_tentativas < qtd_max_buscas:
        print("Erro "+str(response.status_code)+" na busca "+str(qtd_tentativas)+"/"+str(qtd_max_buscas)+", iniciando proxima tentativa ")
        qtd_tentativas = qtd_tentativas+1   
        response = requests.post(api_url_base, headers=headers, json=json)

    time_finish = time.time()
    delta = time_finish-time_start
    print("tempo da consulta: ")
    print(delta)
    return response

def start():
    respo = initialaze()
    # result = search(respo)
    return respo.json()#result

def initialaze():
    
    next_query = query.replace("{AFTER}", "")
    json["query"] = next_query
    response = request(json)
    return response

def search(result):
    if result.status_code == 200 :
        result = result.json()
        have_next_page = result["data"]["search"]["pageInfo"]["hasNextPage"]
        nodes = result['data']['search']['nodes']
        current_page = 1
        while have_next_page and current_page < qtd_page:
            cursor = result["data"]["search"]["pageInfo"]["endCursor"]
            next_query = query.replace("{AFTER}", ", after: \"%s\"" % cursor)
            json["query"] = next_query
            result = request(json, current_page)
            if result.status_code == 200:
                result = result.json()
                nodes += result['data']['search']['nodes']
                have_next_page  = result["data"]["search"]["pageInfo"]["hasNextPage"]
            else:
                print("reiniciando a consulta!")
                return result
            current_page+=1
        result['data']['search']['nodes'] = nodes
    return result

def save_file(json):
    nodes = json['data']['user']['repositories']['nodes']

    file = open("arquivo.csv", 'w')
    fieldnames = ["Nome","url","Data Criacao","Data de Atualizacao","Total de releases","Linguagem","Idade","Tempo de Atualizacao em dias"]
    writer = csv.DictWriter(file, fieldnames=fieldnames)
    writer.writeheader()


    for node in nodes:
        data = node['createdAt']
        data_atual = datetime.datetime.now().date()
        parametros = (data.split('T')[0]).split('-')
        date = datetime.datetime(int(parametros[0]), int(parametros[1]), int(parametros[2])).date()
        idade = int(int(abs((data_atual - date).days))/365)

        data = node['updatedAt']
        parametros_a = (data.split('T')[0]).split('-')
        date = datetime.datetime(int(parametros_a[0]), int(parametros_a[1]), int(parametros_a[2])).date()
        tempo_atualizacao = int(int(abs((data_atual - date).days)))
        
        linguagem = 'Não informado'
        if node['primaryLanguage'] is not None: 
            linguagem = str(node['primaryLanguage']['name'])
        
        if linguagem == "Python":
	        writer.writerow({"Nome": node['nameWithOwner'],
	                         "url":node['url'],
	                         "Data Criacao":date,
	                         "Data de Atualizacao":node['updatedAt'],
	                         "Linguagem":linguagem,
	                         "Total de releases":node['releases']['totalCount'],
	                         "Idade": idade,
	                         "Tempo de Atualizacao em dias": tempo_atualizacao
	                        })
    file.close()



# save_repository()
result = start()
save_file(result)

