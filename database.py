# -*- coding: utf-8 -*-
import os
import os.path
import time
from tkinter import filedialog
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import shutil
import pandas as pd

def bot ():

	linhagens = ['B.1.351.5', 'P.1']
	database = 'database'
	dataframe = 'lista de sequências.csv'
	destino = os.path.dirname(os.path.abspath(__file__))

	#Selecionando a pasta Downloads do computador
	print('\nSelecione a pasta de downloads do seu computador\n')
	downloads = filedialog.askdirectory() #abre a caixa de diálogo que permite selecionar o diretório
	downloads = str(downloads)

	print('\nAcessando GISAID\n')
	navegador = webdriver.Chrome()
	try:
		navegador.get("https://gisaid.org/")
		navegador.refresh()
	time.sleep(5)
	except:
	WebDriverWait(navegador, 60).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="fixo0"]/a/span'))).click()
	WebDriverWait(navegador, 60).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="menuequer"]/li[7]/a'))).click() #só vai rodar se tiver minimizado, pois não aparece o menu quando está maximizado

	print('\nAcessando EpiCov\n')
	time.sleep(5)
	login = navegador.find_element(by=By.XPATH, value='//*[@id="elogin"]')
	login.send_keys('robertoaabfilho')
	time.sleep(5)
	senha = navegador.find_element(by=By.XPATH, value='//*[@id="epassword"]') #mudei a variavel login para senha! são variaveis distintas!
	senha.send_keys('bioinformatica@2017') #variavel senha para receber a senha!
	WebDriverWait(navegador, 600).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="login"]/div[2]/input[3]'))).click()
	time.sleep(5)
	WebDriverWait(navegador, 600).until(EC.element_to_be_clickable((By.XPATH, '/html/body/form/div[5]/div/div[2]/div/div[1]/div/div/div[3]'))).click()
	time.sleep(5)

	for linhagem in linhagens:
		print('\nBuscando sequências pela linhagem: ' + linhagem)
		WebDriverWait(navegador, 600).until(EC.element_to_be_clickable((By.XPATH, '/html/body/form/div[5]/div/div[2]/div/div[2]/div[1]/div/table/tbody/tr[2]/td[5]/div/div/div[1]/div/input'))).click()
		time.sleep(5)
		WebDriverWait(navegador, 600).until(EC.element_to_be_clickable((By.XPATH, '/html/body/form/div[5]/div/div[2]/div/div[2]/div[1]/div/table/tbody/tr[3]/td[5]/div/div/div[1]/div/input'))).click()
		time.sleep(5)
		WebDriverWait(navegador, 600).until(EC.element_to_be_clickable((By.XPATH, '/html/body/form/div[5]/div/div[2]/div/div[2]/div[1]/div/table/tbody/tr[5]/td[2]/div[3]/div/div/div[1]/input'))).send_keys(linhagem)
		time.sleep(10)
		WebDriverWait(navegador, 600).until(EC.element_to_be_clickable((By.XPATH, '/html/body/form/div[5]/div/div[2]/div/div[2]/div[2]/div[1]/div[2]/table/thead/tr/th[1]/div/span/input'))).click()
		time.sleep(50)
		WebDriverWait(navegador, 600).until(EC.element_to_be_clickable((By.XPATH, '/html/body/form/div[5]/div/div[2]/div/div[2]/div[2]/div[2]/div[3]/button[2]'))).click()
		time.sleep(10)
		print('Baixando as IDs')
		iframe = WebDriverWait(navegador, 600).until(EC.element_to_be_clickable((By.TAG_NAME, 'iframe')))
		navegador.switch_to.frame(iframe)
		time.sleep(5)
		WebDriverWait(navegador, 600).until(EC.element_to_be_clickable((By.XPATH, '/html/body/form/div[5]/div/div[2]/div/div/div[3]/div/button'))).click()
		time.sleep(5)
		WebDriverWait(navegador, 600).until(EC.element_to_be_clickable((By.XPATH, '/html/body/form/div[5]/div/div[2]/div/div/div[1]/div/button'))).click()
		time.sleep(5)

		# Para transferir o arquivo .csv para a pasta principal
		lista_arquivos = os.listdir(downloads) #Lista_arquivos = variável que verificar todos os arquivos na pasta dowload
		lista_datas = [] 
		for arquivo in lista_arquivos: #Cada um da variavel arquivo é dado a variavel lista_arquivos
			if ".csv" in arquivo: #estranho perguntar (ok. por que vai pegar sempre o último )
				data = os.path.getmtime(f"{downloads}/{arquivo}")
				lista_datas.append((data, arquivo)) #Gerando uma tupla  por data e arquivo mais recente baixados todos na pasta.

		lista_datas.sort(reverse=True) # Depois o sort ordena por data e arquivo mais recente garantindo que [0] seja o mais recente
		recente = lista_datas[0][1] # Último arquivo = variável recente. Essa variavel recente vai receber o primeiro item da tupla posição [0] sendo o nome do arquivo puxado [1]
		csv = downloads +'\\' + recente
		time.sleep(5)
		shutil.move(csv, destino)
		file = linhagem + '.csv' #citar file antes. Não precisa concatenar
		os.rename(recente, file) #a variável "f" não retornava a nada por isso apagada


		print('Contando a população')
		f = pd.read_csv(file)
		total = len(f)
		print(total)
		print('Calculando o tamanho da amostra')

		def amostra(e,N):  #podia estar do lado de fora e ser puxada somente depois (na hora que precisar)
			n = (N/(1+(N*(e**2))))
			return (n)
		e_ = 0.05
		N_ = total #Pode declarar o int aqui. Pode apagar O N_ e tirar o N da equação e já puxar direto o valor da variável total
		tamanho_amostra = int(amostra(e_, N_)) #esquisito. Qual o intuito ?
		print(tamanho_amostra)
		os.remove(file) #apaga o arquivo csv

		print('Gerando amostra aleatória simples sem reposição') 
		selecionadas = f.sample(tamanho_amostra)
		temp = linhagem+'.txt'
		f = selecionadas.to_string(temp, index=False)

		print('Buscando sequências da amostra')
		with open(temp, 'r') as f:
			temp = f.read()
			WebDriverWait(navegador, 600).until(EC.element_to_be_clickable((By.XPATH, '/html/body/form/div[5]/div/div[2]/div/div[1]/div/div/div[3]'))).click()
			time.sleep(10)
			WebDriverWait(navegador, 600).until(EC.element_to_be_clickable((By.XPATH, '/html/body/form/div[5]/div/div[2]/div/div[2]/div[1]/div/table/tbody/tr[6]/td[1]/div/div/div[1]/textarea'))).send_keys(temp)
			time.sleep(10)
			WebDriverWait(navegador, 600).until(EC.element_to_be_clickable((By.XPATH, '/html/body/form/div[5]/div/div[2]/div/div[2]/div[2]/div[1]/div[2]/table/thead/tr/th[1]/div/span/input'))).click()
			time.sleep(50)
			WebDriverWait(navegador, 600).until(EC.element_to_be_clickable((By.XPATH, '/html/body/form/div[5]/div/div[2]/div/div[2]/div[2]/div[2]/div[3]/button[4]'))).click()
			time.sleep(10)
			iframe2 = navegador.find_element(by=By.TAG_NAME, value='iframe')
			time.sleep(5)
			navegador.switch_to.frame(iframe2)
			time.sleep(5)
			WebDriverWait(navegador, 600).until(EC.element_to_be_clickable((By.XPATH, '/html/body/form/div[5]/div/div[1]/div/div/table[1]/tbody/tr/td[2]/div/div[1]/div[2]/div[3]/input'))).click()
			time.sleep(5)
			WebDriverWait(navegador, 600).until(EC.element_to_be_clickable((By.XPATH, '/html/body/form/div[5]/div/div[2]/div/div/div[2]/div/button'))).click()
			time.sleep(5)
			iframe3 = navegador.find_element(by=By.TAG_NAME, value='iframe')
			time.sleep(5)
			navegador.switch_to.frame(iframe3)
			time.sleep(5)
			WebDriverWait(navegador, 600).until(EC.element_to_be_clickable((By.XPATH, '/html/body/form/div[5]/div/div[2]/div[1]/div/table/tbody/tr/td[2]/table/tbody/tr/td/div/div[1]/div/input'))).click()
			time.sleep(5)
			WebDriverWait(navegador, 600).until(EC.element_to_be_clickable((By.XPATH, '/html/body/form/div[5]/div/div[2]/div[2]/div/div[2]/div/button'))).click()
			time.sleep(5)
			try:
				time.sleep(20)
				lista_arquivos = os.listdir(downloads)
				lista_datas = []
				for arquivo in lista_arquivos:
					if ".fasta" in arquivo:
						data = os.path.getmtime(f"{downloads}/{arquivo}")
						lista_datas.append((data, arquivo))
			except:
				time.sleep(60)
				lista_arquivos = os.listdir(downloads)
				lista_datas = []
				for arquivo in lista_arquivos:
					if ".fasta" in arquivo:
						data = os.path.getmtime(f"{downloads}/{arquivo}")
						lista_datas.append((data, arquivo))
		
		lista_datas.sort(reverse=True)
		ultimo_arquivo = lista_datas[0]
		ultimo_arquivo = ultimo_arquivo[1]
		fasta = downloads+'\\'+ultimo_arquivo
		os.rename(fasta, downloads+'\\'+linhagem+'.fas')
		fasta = downloads+'\\'+linhagem+'.fas'	
		shutil.move(fasta, destino+'\\'+database)
		lista = os.listdir(destino)
		for f in lista:
			if '.txt' in f:
				os.remove(f)
				
		print('Amostra da linhagem '+linhagem+' concluída!')

	print('Base de dados concluída!')


	

bot()