import os
from To_copy.to_copy import copy_text_files

comp_name = input("Insira o nome da imobiliária: ").strip().replace(" ","_")
acron_name = input("Insira a sigla: ")[:2].upper()
url = input("Insira o url para coleta dos links dos anúncios: ")

path_dir = "C:/Users/joaov/OneDrive/Área de Trabalho/Backup Pendrive/Data/Web Scraping"
path = os.path.join(path_dir, comp_name)

os.mkdir(path)

files_text = copy_text_files(comp_name, acron_name, url)

for index, title in enumerate(["find", "main"]):
    with open(f"{path_dir+"/"+comp_name+"/"+title}.py", "a") as file:
        file.write(files_text[index])