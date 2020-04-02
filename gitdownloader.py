from git import Git
from csv import DictReader
from csv import DictWriter
from csv import writer
from csv import reader

import time
import os
import signal, time, random

class MyTimeout(Exception):
    pass

def handler(signum, frame):
    print('Timeout', signum)
    raise MyTimeout

def downloadRepo():
	numero = 136
	with open('arquivo.csv') as repositorios:
		file = open('arquivo_loc.csv','w')
		fieldnames = ["Nome","url","Data Criacao","Data de Atualizacao","Total de releases","Linguagem","Idade","Tempo de Atualizacao em dias","Loc"]
		csv_writer = DictWriter(file, fieldnames=fieldnames)

		reader = DictReader(repositorios)
		repoF = []
		for repo in reader:
			status = 'ok'
			linhas = 0

			try:
				signal.signal(signal.SIGALRM, handler)
				signal.alarm(600)
				print("Baixando repositorio "+ repo['Nome']+""+ str(numero))
				Git('repositorios').clone(repo['url'])
				# Analise
				path = getPath(repo['Nome'])
				print('analisando o repositorio: '+ repo['Nome'])
				linhas = int(countlines(path))
				
			except MyTimeout:
				status = 'falha'
				print('falha')
				continue
			except TimeoutError as exc:
				repoF.append(repo['url'])
				status = 'falha'
				print('falha')
				continue
			except Exception as e:
				repoF.append(repo['url'])
				status = 'falha'
				print('falha')
				continue
			finally:
				numero += 1
				csv_writer.writerow({"Nome": repo['Nome'],
	                         "url": repo['url'],
	                         "Data Criacao":repo['Data Criacao'],
	                         "Data de Atualizacao":repo['Data de Atualizacao'],
	                         "Linguagem":repo['Linguagem'],
	                         "Total de releases":repo['Total de releases'],
	                         "Idade": repo['Idade'],
	                         "Tempo de Atualizacao em dias": repo['Tempo de Atualizacao em dias'],
							 "Loc":linhas
	                        })
				print("download do repositorio: "+ repo['Nome']+" status:" +status )

def getPath(nome):
	parent = os.getcwd() + "/repositorios/"
	directory = nome.split('/')[1]
	path = os.path.join(parent, directory)
	return path

def addToCsv(lines):
	# Open the input_file in read mode and output_file in write mode
	with open('arquivo.csv', 'r') as read_obj, \
        open('arquivo_loc.csv', 'w', newline='') as write_obj:
	# Create a csv.reader object from the input file object
		csv_reader = reader(read_obj)
		# Create a csv.writer object from the output file object
		csv_writer = writer(write_obj)
		isHeader = True
		index = 0
		fieldnames = ["Nome","url","Data Criacao","Data de Atualizacao","Total de releases","Linguagem","Idade","Tempo de Atualizacao em dias","Loc"]
		    # Read each row of the input csv file as list
		for row in csv_reader:
			if isHeader is True:
				csv_writer.writerow(fieldnames)
				isHeader = False
			else:
				# Append the default text in the row / list
				row.append(lines[index])
				index+=1
				# Add the updated row / list to the output file
				csv_writer.writerow(row)		

def countlines(start, lines=0, header=True, begin_start=None):
    try:
        for thing in os.listdir(start):
            thing = os.path.join(start, thing)
            if os.path.isfile(thing):
                if thing.endswith('.py'):
                    with open(thing, 'r') as f:
                        newlines = f.readlines()
                        newlines = len(newlines)
                        lines += newlines

                        if begin_start is not None:
                            reldir_of_thing = '.' + thing.replace(begin_start, '')
                        else:
                            reldir_of_thing = '.' + thing.replace(start, '')

        for thing in os.listdir(start):
            thing = os.path.join(start, thing)
            if os.path.isdir(thing):
                lines = countlines(thing, lines, header=False, begin_start=start)
    except:
        pass

    return lines

downloadRepo()