import os
from glob import glob
from csv import writer
from csv import reader


root_path = os.getcwd()

# trecho adaptado da internet
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
				


repos_path =  os.getcwd() + "/repositorios/*"

diretorios = glob(repos_path)

vetor_lines = []

for repo_diretorio in diretorios:
    contador_linhas_repo = (countlines(repo_diretorio))
    vetor_lines.append(contador_linhas_repo)

addToCsv(vetor_lines)
