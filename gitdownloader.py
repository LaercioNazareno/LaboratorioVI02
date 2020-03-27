from git import Git
from csv import DictReader


with open('arquivo.csv') as repositorios:
	reader = DictReader(repositorios)

	for repo in reader:
		print(f"Baixando repositório {repo['Nome']}.")
		Git('repositorios').clone(repo['url'])
