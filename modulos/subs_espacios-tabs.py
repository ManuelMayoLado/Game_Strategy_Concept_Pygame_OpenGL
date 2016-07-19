# -*- coding: utf-8 -*-

import sys

if len(sys.argv) > 1:
	nome_arquivo = sys.argv[1]
else:
	nome_arquivo = raw_input(">>> Introduce o nome do arquivo: ")
	
texto_arquivo = open(nome_arquivo,"r").read()
	
print(u"Substituir:")
opcion = raw_input(u"[1] - Espacios por Tabs\n[2] - Tabs por Espacios\n>>> ")

if opcion == "1":
	num_espacios = raw_input(u">>> Numero de espacios a subtituir por cada Tabulacion: ")
else:
	num_espacios = raw_input(u">>> Numero de espacios a introducir por cada Tabulacion: ")
	
def substituir(text,opc,num_esp):
	if opc == "1":
		texto_salida = text.replace(" "*int(num_esp),"\t")
	elif opc == "2":
		texto_salida = text.replace("\t"," "*int(num_esp))
	return texto_salida
	
arquivo_a_crear = open(nome_arquivo,"w")
arquivo_a_crear.write(substituir(texto_arquivo,opcion,num_espacios))
arquivo_a_crear.close()