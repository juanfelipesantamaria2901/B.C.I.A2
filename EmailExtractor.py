#Autor: Juan Felipe Santamaria Guerrero
from googlesearch import search
from socket import timeout
import http
from bs4 import BeautifulSoup
import urllib.request
from urllib.request import URLError, HTTPError
import random
import os
import time
import sqlite3
from sqlite3 import Error
import sys
import re
from fake_useragent import UserAgent
from socket import timeout
from urllib.error import HTTPError, URLError

import googlesearch

imageExt = ["jpeg", "exif", "tiff", "gif", "bmp", "png", "ppm", "pgm", "pbm", "pnm", "webp", "hdr", "heif", "bat", "bpg", "cgm", "svg"]
ua = UserAgent()

count_email_in_phrase = 0

# Menú Principal
def menu():
    	
	global count_email_in_phrase
	count_email_in_phrase = 0

	try:
		clear()
		print('		 /                                     \ ')
		print('		 |            Prospectos Correros      |')
		print('		 \_____________________________________/')
		print('')
		print(' ------------------------------------------------------------------')
		print("|                        ESPAÑOL                                    | ")
		print(" ------------------------------------------------------------------")
		print("1 - Buscar solo en la URL ingresada")
		print("2 - Buscar en una URL(Dos Niveles)")
		print("3 - Buscar frase en Google")
		print("4 - En desarrollo")
		print("5 - Listar correos")
		print("6 - Guardar correos en archivo .txt")
		print("7 - Eliminar correos de la Base de datos")
		print("8 - Salir")
		print("")

		opcion = input("Enter option - Ingrese Opcion: ")
		if (opcion == "1"):
			print("")
			print ("Example URL: http://www.pythondiario.com")
			url = str(input("Enter URL - Ingrese URL: "))
			extractOnlyUrl(url)
			input("Pulsa enter para continuar")
			menu()

		if (opcion == "2"):
			print("")
			print ("Example URL: http://www.pythondiario.com")
			url = str(input("Enter URL - Ingrese URL: "))
			extractUrl(url)
			input("Pulsa enter para continuar")
			menu()

		elif (opcion == "3"):
			print("")
			frase = str(input("Ingresa una frase a buscar: "))
			print ("*** Advertencia: La cantidad de resultados elejidos impacta el tiempo de ejecucion")
			cantRes = int(input("Cantiad de resultados en Google: ")) 
			print ("")
			googlesearch.search (frase, cantRes, lang="es,en")
			input("Pulsa enter para continuar")
			menu()

		elif (opcion == "4"):
			#extractKeywordsList("KeywordsList.txt")
			print("Desarollando...")
			input("Pulsa enter para continuar")
			menu()
		
		elif (opcion == "5"):
			print ("")
			print ("1 - Seleccionar una frase")
			print ("2 - Insert una URL")
			print ("3 - Todos los correos")
			opcListar = input(" Ingrese Opcion: ")
			
			if (opcListar == "1"):
				listarPorFrase("Emails.db")

			elif (opcListar == "2"):
				listarPorUrl("Emails.db")

			elif (opcListar == "3"):
				listarTodo("Emails.db")

			else:
				print("Opcion incorrecta, retornando al menu...")
				time.sleep(2)
				menu()

		elif (opcion == "6"):
			print("")
			print("1 - Guardar correos de una frase")
			print("2 - Guardar correos de una URL")
			print("3 - Guardar todos los correos")
			opcGuardar = input("Ingrese Opcion: ")
			
			if(opcGuardar == "1"):
				frase = str(input("Enter phrase: "))
				guardarFrase("Emails.db", frase)
				
			elif(opcGuardar == "2"):
				print("Example URL: http://www.pythondiario.com")
				url = str(input("Insert URL: "))
				guardarUrl("Emails.db", url)
				
			elif(opcGuardar == "3"):
				guardarAll("Emails.db")
				
			else:
				print("Opcion incorrecta, retornando al menu..")
				time.sleep(2)
				menu()

		elif (opcion == "7"):
			print("")
			print("1 - Elimina correo con URL especifica")
			print("2 - Elimina correo con frace especifica")
			print("3 - Elimina todos los correos")
			op = input("Ingresa opcion: ")

			if(op == "1"):
				print("Example URL: http://www.pythondiario.com")
				url = str(input("Insert URL: "))
				deleteUrl("Emails.db", url.strip())
			
			elif(op == "2"):
				phrase = str(input("Inserta frase: "))
				deletePhrase("Emails.db", phrase.strip())

			elif(op == "3"):
				deleteAll("Emails.db")

			else:
				print("Opcion incorrecta, retornando al menu...")
				time.sleep(2)
				menu()
		
		elif (opcion == "8"):
			sys.exit(0)

		else:			
			print("")
			print (" Seleccione un opcion correcta")
			time.sleep(3)
			clear()
			menu()
	
	except KeyboardInterrupt:
		input("Pulsa enter para continuar")
		menu()

	except Exception as e:
		print (e)
		input("Pulsa enter para continuar")
		menu()

# Insertar correo, frase y Url en base de datos
def insertEmail(db_file, email, frase, url):
	try:
		conn = sqlite3.connect(db_file)
		c = conn.cursor()
		c.execute("INSERT INTO emails (phrase, email, url) VALUES (?,?,?)", (frase, email, url))
		conn.commit()
		conn.close()

	except Error as e:
		print(e)
		input("Pulsa enter para continuar")
		menu()

	finally:
		conn.close()

# Buscar correo en la base de datos
def searchEmail(db_file, email, frase):
	try:
		conn = sqlite3.connect(db_file)
		c = conn.cursor()
		sql = 'SELECT COUNT(*) FROM emails where email LIKE "%' + str(email) + '%" AND phrase LIKE "%' + str(frase) + '%"'
		result = c.execute(sql).fetchone()
		conn.close()

		return (result[0])

	except Error as e:
		print(e)
		input("Pulsa enter para continuar")
		menu()

	finally:
		conn.close()

# Crea tabla principal		
def crearTabla(db_file, delete = False):
	try:
		conn = sqlite3.connect(db_file)
		c = conn.cursor()
		
		if(delete == True):
			c.execute('drop table if exists emails')			

		sql = '''create table if not exists emails 
				(ID INTEGER PRIMARY KEY AUTOINCREMENT,
				 phrase varchar(500) NOT NULL,
				 email varchar(200) NOT NULL,
				 url varchar(500) NOT NULL)'''

		c.execute(sql)
		conn.close()

	except Error as e:
		print(e)
		input("Pulsa enter para continuar")
		menu()

	finally:
		conn.close()

# Guardar por URL en un archivo .txt
def guardarUrl(db_file, url):
	try:
		conn = sqlite3.connect(db_file)
		c = conn.cursor()
		sql = 'SELECT COUNT(*) FROM emails WHERE url = "' + url.strip() + '"'
		result = c.execute(sql).fetchone()

		if(result[0] == 0):
			print("There are no emails to erase")
			input("Pulsa enter para continuar")
			menu()
			
		else:
			nameFile = str(input("Nombre del archivo:  "))
			print("")
			print("Archivo guardado... por favor espera")
			
			f = open(nameFile.strip() + ".txt", "w")
		
			c.execute('SELECT * FROM emails WHERE url = "' + url.strip() + '"')
			
			count = 0
			
			for i in c:
				count += 1
				f.write("")
				f.write("Number: " + str(count) + '\n')
				f.write("Phrase: " + str(i[1]) + '\n')
				f.write("Email: " + str(i[2]) + '\n')
				f.write("Url: " + str(i[3]) + '\n')
				f.write("-------------------------------------------------------------------------------" + '\n')
				
			f.close()
			
		conn.close()
		input("Pulsa enter para continuar")
		menu()
		
	except Error as e:
		print(e)
		input("Pulsa enter para continuar")
		menu()
		
	except Exception as o:
		print(o)
		input("Pulsa enter para continuar")
		menu()
		
	finally:
		conn.close()

# Guardar por frase en un archivo .txt
def guardarFrase(db_file, frase):
	try:
		conn = sqlite3.connect(db_file)
		c = conn.cursor()
		sql = 'SELECT COUNT(*) FROM emails WHERE phrase = "' + frase.strip() + '"'
		result = c.execute(sql).fetchone()

		if(result[0] == 0):
			print("There are no emails to erase")
			input("Pulsa enter para continuar")
			menu()
			
		else:
			nameFile = str(input("Nombre del archivo:  "))
			print("")
			print("Archivo guardado... por favor espera")
			
			f = open(nameFile.strip() + ".txt", "w")
		
			c.execute('SELECT * FROM emails WHERE phrase = "' + frase.strip() + '"')
			
			count = 0
			
			for i in c:
				count += 1
				f.write("")
				f.write("Number: " + str(count) + '\n')
				f.write("Phrase: " + str(i[1]) + '\n')
				f.write("Email: " + str(i[2]) + '\n')
				f.write("Url: " + str(i[3]) + '\n')
				f.write("-------------------------------------------------------------------------------" + '\n')
				
			f.close()
			
		conn.close()
		input("Pulsa enter para continuar")
		menu()
			
	except Error as e:
		print(e)
		input("Pulsa enter para continuar")
		menu()
		
	except Exception as o:
		print(o)
		input("Pulsa enter para continuar")
		menu()
		
	finally:
		conn.close()

# Guardar todos los correos en un archivo .txt
def guardarAll(db_file):
	try:
		conn = sqlite3.connect(db_file)
		c = conn.cursor()
		sql = 'SELECT COUNT(*) FROM emails'
		result = c.execute(sql).fetchone()

		if(result[0] == 0):
			print("No hay correos electrónicos para borrar")
			input("Pulsa enter para continuar")
			menu()
			
		else:
			nameFile = str(input("Nombre del archivo: "))
			print("")
			print("Archivo guardado... por favor espera")
			
			f = open(nameFile + ".txt", "w")
		
			c.execute('SELECT * FROM emails')
			
			count = 0
			
			for i in c:
				count += 1
				f.write("")
				f.write("Number: " + str(count) + '\n')
				f.write("Phrase: " + str(i[1]) + '\n')
				f.write("Email: " + str(i[2]) + '\n')
				f.write("Url: " + str(i[3]) + '\n')
				f.write("-------------------------------------------------------------------------------" + '\n')
				
			f.close()
			
		conn.close()
		
		input("Pulsa enter para continuar")
		menu()
		
	except Error as e:
		print(e)
		input("Pulsa enter para continuar")
		menu()
		
	except Exception as o:
		print(o)
		input("Pulsa enter para continuar")
		menu()
		
	finally:
		conn.close()

# Borra todos los correos de una URL específica
def deleteUrl(db_file, url):
	try:
		conn = sqlite3.connect(db_file)
		c = conn.cursor()
		sql = 'SELECT COUNT(*) FROM emails WHERE url = ' + '"' + url + '"'
		result = c.execute(sql).fetchone()
		
		if(result[0] == 0):
			print("No hay correos electrónicos para borrar")
			input("Pulsa enter para continuar")
			menu()
			
		else:
			option = str(input("Are you sure you want to delete " + str(result[0]) + " emails? Y/N :"))
			
			if(option == "Y" or option == "y"):
				c.execute("DELETE FROM emails WHERE url = " + '"' + url + '"')
				conn.commit()

				print("Emails deleted")
				input("Pulsa enter para continuar")
				menu()
				
			elif(option == "N" or option == "n"):
				print("operacion cancelada, retornando al menu ...")
				time.sleep(2)
				menu()
				
			else:
				print("Pulsa enter para continuar")
				time.sleep(2)
				deleteUrl(db_file, url)
				
		conn.close()
		
	except Error as e:
		print(e)
		input("Pulsa enter para continuar")
		menu()
		
	finally:
		conn.close()

# Borra todos los correos de una Frase específica
def deletePhrase(db_file, phrase):
	try:
		conn = sqlite3.connect(db_file)
		c = conn.cursor()
		sql = 'SELECT COUNT(*) FROM emails WHERE phrase = ' + '"' + phrase + '"'
		result = c.execute(sql).fetchone()
		
		if(result[0] == 0):
			print("No hay correos electrónicos para borrar")
			input("Pulsa enter para continuar")
			menu()
			
		else:
			option = str(input("Are you sure you want to delete " + str(result[0]) + " emails? Y/N :"))
			
			if(option == "Y" or option == "y"):
				c.execute("DELETE FROM emails WHERE phrase = " + '"' + phrase + '"')
				conn.commit()

				print("Emails eliminados")
				input("Pulsa enter para continuar")
				menu()
				
			elif(option == "N" or option == "n"):
				print("operacion cancelada, retornando al menu ...")
				time.sleep(2)
				menu()
				
			else:
				print("Pulsa enter para continuar")
				time.sleep(2)
				deleteUrl(db_file, phrase)
				
		conn.close()
				
	except Error as e:
		print(e)
		input("Pulsa enter para continuar")
		menu()
		
	finally:
		conn.close()

# Borra todos los correos
def deleteAll(db_file):
	try:
		conn = sqlite3.connect(db_file)
		c = conn.cursor()
		sql = 'SELECT COUNT(*) FROM emails'
		result = c.execute(sql).fetchone()

		if(result[0] == 0):
			print("No hay correos que eliminar")
			input("Pulsa enter para continuar")
			menu()
		
		
		else:			
			option = str(input("Estas seguro de eliminarlos " + str(result[0]) + " emails? Y/N :"))
			
			if(option == "Y" or option == "y"):
				c.execute("DELETE FROM emails")
				conn.commit()
				crearTabla("Emails.db", True)
				print("Todos los correros eliminados")
				input("Pulsa enter para continuar")
				menu()

			elif(option == "N" or option == "n"):
				print("operacion cancelada, retornando al menu ...")
				time.sleep(2)
				menu()

			else:
				print("Selecciona una opcion correccta")
				time.sleep(2)
				deleteAll(db_file)
				
		conn.close()

	except Error as e:
		print(e)
		input("Pulsa enter para continuar")
		menu()

	finally:
		conn.close()

# Lista correos por frase
def listarPorFrase(db_file):
	try:
		phrase = str(input("Insertar frase: "))
		conn = sqlite3.connect(db_file)
		c = conn.cursor()
		
		sql = 'SELECT COUNT(*) FROM emails WHERE phrase LIKE "%' + phrase.strip() + '%"'
		result = c.execute(sql).fetchone()

		if(result[0] == 0):
				print("No results for the specified url")
				input("Pulsa enter para continuar")
				menu()
				
		else:
			c.execute('SELECT * FROM emails WHERE phrase LIKE "%' + phrase.strip() + '%"')

			for i in c:

				print ("")
				print ("Number: " + str(i[0]))
				print ("Phrase: " + str(i[1]))
				print ("Email: " + str(i[2]))
				print ("Url: " + str(i[3]))
				print ("-------------------------------------------------------------------------------")

		conn.close()
		
		print ("")
		input("Pulsa enter para continuar")
		menu()
		
	except Error as e:
		print(e)
		input("Pulsa enter para continuar")
		menu()
	
	finally:
		conn.close()

# Lista correos por URL
def listarPorUrl(db_file):
	try:
		print("Example URL: http://www.pythondiario.com ")
		url = str(input("Insert a Url: "))
		conn = sqlite3.connect(db_file)
		c = conn.cursor()

		sql = 'SELECT COUNT(*) FROM emails WHERE url LIKE "%' + url.strip() + '%"'
		result = c.execute(sql).fetchone()

		if(result[0] == 0):
				print("No results for the specified url")
				input("Pulsa enter para continuar")
				menu()

		else:
			c.execute('SELECT * FROM emails WHERE url LIKE "%' + url.strip() + '%"')

			for i in c:

				print ("")
				print ("Number: " + str(i[0]))
				print ("Phrase: " + str(i[1]))
				print ("Email: " + str(i[2]))
				print ("Url: " + str(i[3]))
				print ("-------------------------------------------------------------------------------")

		conn.close()
		
		print ("")
		input("Pulsa enter para continuar")
		menu()

	except Error as e:
		print(e)
		input("Pulsa enter para continuar")
		menu()
		
	finally:
		conn.close()

# Lista todos los correos
def listarTodo(db_file):
	try:
		conn = sqlite3.connect(db_file)
		c = conn.cursor()

		sql = 'SELECT COUNT(*) FROM emails'
		result = c.execute(sql).fetchone()

		if(result[0] == 0):
			print("The data base is Empty")
			input("Pulsa enter para continuar")
			menu()

		c.execute("SELECT * FROM emails")

		for i in c:

			print ("")
			print ("Number: " + str(i[0]))
			print ("Phrase: " + str(i[1]))
			print ("Email: " + str(i[2]))
			print ("Url: " + str(i[3]))
			print ("-------------------------------------------------------------------------------")

		conn.close()
		
		print ("")
		input("Pulsa enter para continuar")
		menu()

	except Error as e:
		print(e)
		input("Pulsa enter para continuar")
		menu()

	finally:
		conn.close()

# Extrae los correos de una única URL
def extractOnlyUrl(url):
	try:
		print ("Buscando correos por favor espere")

		count = 0
		listUrl = []

		req = urllib.request.Request(
    			url, 
    			data=None, 
    			headers={
        		'User-Agent': ua.random
    		})

		try:
			conn = urllib.request.urlopen(req, timeout=10)

		except timeout:
			raise ValueError('Timeout ERROR')

		except (HTTPError, URLError):
			raise ValueError('Bad Url...')

		status = conn.getcode()
		contentType = conn.info().get_content_type()

		if(status != 200 or contentType == "audio/mpeg"):
    			raise ValueError('Bad Url...')


		html = conn.read().decode('utf-8')

		emails = re.findall(r'[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,4}', html)

		for email in emails:
			if (email not in listUrl and email[-3:] not in imageExt):
				count += 1
				print(str(count) + " - " + email)
				listUrl.append(email)
				if(searchEmail("Emails.db", email, "Busqueda especifica") == 0):
					insertEmail("Emails.db", email, "Busqueda especifica", url)

		print("")
		print("***********************")
		print(str(count) + " Correos encontrados")
		print("***********************")

	except KeyboardInterrupt:
		input("Pulsa enter para continuar")
		menu()

	except Exception as e:
		print (e)
		input("Pulsa enter para continuar")
		menu()

# Extrae los correos de una Url - 2 niveles
def extractUrl(url):
	print ("Buscando correos, por favor espera...")
	print ("Esta operacion puede tardar algunos minutos")
	try:
		count = 0
		listUrl = []
		req = urllib.request.Request(
    			url, 
    			data=None, 
    			headers={
        		'User-Agent': ua.random
    		})

		try:
			conn = urllib.request.urlopen(req, timeout=10)

		except timeout:
			raise ValueError('Timeout ERROR')

		except (HTTPError, URLError):
			raise ValueError('Url Malo...')

		status = conn.getcode()
		contentType = conn.info().get_content_type()

		if(status != 200 or contentType == "audio/mpeg"):
    			raise ValueError('Url Malo...')

		html = conn.read().decode('utf-8')
		
		emails = re.findall(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,4}", html)
		print ("Searching in " + url)
		
		for email in emails:
			if (email not in listUrl and email[-3:] not in imageExt):
					count += 1
					print(str(count) + " - " + email)
					listUrl.append(email)

		soup = BeautifulSoup(html, "lxml")
		links = soup.find_all('a')

		print("They will be analyzed " + str(len(links) + 1) + " Urls..." )
		time.sleep(2)

		for tag in links:
			link = tag.get('href', None)
			if link is not None:
				try:
					print ("Searching in " + link)
					if(link[0:4] == 'http'):
						req = urllib.request.Request(
							link, 
							data=None, 
							headers={
							'User-Agent': ua.random
							})

						try:
							f = urllib.request.urlopen(req, timeout=10)

						except timeout:
							print("Bad Url..")
							time.sleep(2)
							pass

						except (HTTPError, URLError):
							print("Bad Url..")
							time.sleep(2)
							pass

						status = f.getcode()
						contentType = f.info().get_content_type()

						if(status != 200 or contentType == "audio/mpeg"):
							print("Bad Url..")
							time.sleep(2)
							pass
						
						s = f.read().decode('utf-8')

						emails = re.findall(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,4}", s)

						for email in emails:
							if (email not in listUrl and email[-3:] not in imageExt):
								count += 1
								print(str(count) + " - " + email)
								listUrl.append(email)
								if(searchEmail("Emails.db", email, "Especific Search") == 0):
									insertEmail("Emails.db", email, "Especific Search", url)

				# Sigue si existe algun error
				except Exception:
					pass
		
		print("")
		print("***********************")
		print("Terminado: " + str(count) + " Correos encontrados")
		print("***********************")
		input("Pulsa enter para continuar")
		menu()

	except KeyboardInterrupt:
		input("Pulsa enter para continuar")
		menu()

	except Exception as e:
		print(e)
		input("Pulsa enter para continuar")
		menu()

# Extrae los correos de todas las Url encontradas en las busquedas
# De cada Url extrae los correo - 2 niveles
def extractFraseGoogle(frase, cantRes):
	print ("Buscando correos.... por favor espera")
	print ("Esta operacion puede tardar varios")
	try:
		listUrl = []
		listEmails = []

		for url in search(frase, stop=cantRes):
			listUrl.append(url)

		for i in listUrl:
			try:
				req = urllib.request.Request(
							i, 
							data=None, 
							headers={
							'User-Agent': ua.random
							})
				try:
					conn = urllib.request.urlopen(req)
				except timeout:
					print("Bad Url..")
					time.sleep(2)
					pass
				except(HTTPError, URLError):
					print("Bad Url..")
					time.sleep(2)
					pass

				status = conn.getcode()
				contentType = conn.info().get_content_type()

				if(status != 200 or contentType == "audio/mpeg"):
					print("Bad Url..")
					time.sleep(2)
					pass

				html = conn.read()

				soup = BeautifulSoup(html, "lxml")
				links = soup.find_all('a')

				print("They will be analyzed " + str(len(links) + 1) + " Urls..." )
				time.sleep(2)

				for tag in links:
					link = tag.get('href', None)
					if link is not None:
    					# Fix TimeOut
						searchSpecificLink(link, listEmails, frase)
		
			except urllib.error.URLError as e:
				print("Problems with the url:" + i)
				print(e)
				pass
			except (http.client.IncompleteRead) as e:
				print(e)
				pass
			except Exception as e:
				print(e)
				pass
		
		print("")
		print("*******")
		print("Terminado")
		print("*******")
		input("Pulsa retornar para continuar")
		menu()

	except KeyboardInterrupt:
		input("Pulsa retornar para continuar")
		menu()

	except Exception as e:
		print(e)
		input("Pulsa enter para continuar")
		menu()
		
# Extraer lista de palabras claves de txt
def extractKeywordsList(txtFile):
	f = open(txtFile, 'r')
	text = f.read()
	keywordList = text.split(sep='\n')
	for key in keywordList:
    		print(key)



# Limpia la pantalla según el sistema operativo
def clear():
	try:
		if os.name == "posix":
			os.system("clear")
		elif os.name == "ce" or os.name == "nt" or os.name == "dos":
			os.system("cls")
	except Exception as e:
		print(e)
		input("Pulsa enter para continuar")
		menu()
   
def searchSpecificLink(link, listEmails, frase):
	try:

		global count_email_in_phrase

		print ("Searching in " + link)
		if(link[0:4] == 'http'):
			f = urllib.request.urlopen(link, timeout=10)
			s = f.read().decode('utf-8')
			emails = re.findall(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,4}", s)
			for email in emails:
				if (email not in listEmails):
					count_email_in_phrase += 1
					listEmails.append(email)
					print(str(count_email_in_phrase) + " - " + email)										
					if (searchEmail("Emails.db", email, frase) == 0):
						insertEmail("Emails.db", email, frase, link)
						
	# Sigue si existe algun error	
	except (HTTPError, URLError) as e:
		print(e)
		pass
	except timeout:
		print('socket timed out - URL %s', link)
		pass
	except (http.client.IncompleteRead) as e:
		print(e)
		pass
	except Exception as e:
		print(e)
		pass

# Inicio de Programa
def Main():
	clear()
	crearTabla("Emails.db", False)	
	menu()

Main()
