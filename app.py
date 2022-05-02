from bs4 import BeautifulSoup
import requests
import pandas as pd
import time
import boto3
import datetime

def extraer(event, context):
	s3 = boto3.client('s3')
	fecha = datetime.datetime.now()
	anio = fecha.year
	mestexto = fecha.strftime("%B")
	mes = fecha.month
	dia = fecha.day

	s3.download_file('htmlnews',f'headlines/raw/periodico=BBC/year={anio}/month={mestexto}/day={dia}/bbc.html','/tmp/bbc.html')

	ruta_Archivo = "/tmp/bbc.html"
	f = open(ruta_Archivo,'r')
	Fe =  f.read()
	soup=BeautifulSoup(Fe, 'html.parser')

	tag= soup.find_all('a', class_='media__tag')
	link = soup.find_all("a", class_='block-link__overlay-link')
	tags=list()
	links=list()
	titles=list()

	count = 0
	for i in tag:
		if count < 8:
			tags.append(i.text)
		else:
			break
		count+=1

	count =0
	for i in link:
		if count < 8:
			links.append('https://www.bbc.com'+i.get("href"))
			x=i.string
			titles.append(x.strip())
		else:
			break
		count+=1

	df=pd.DataFrame({'Categoria':tags,'Titulo':titles,'Link':links})
	df.to_csv("/tmp/bbc.csv", index = True)
	ruta_Archivo = "/tmp/bbc.csv"
	s3.upload_file(ruta_Archivo,'scrapinghtml',f'news/final/periodico=bbc/year={anio}/month={mestexto}/day={dia}/bbc.csv')

	s3.download_file('htmlnews',f'headlines/raw/periodico=semana/year={anio}/month={mestexto}/day={dia}/semana.html','/tmp/semana.html')
	ruta_Archivo2 = "/tmp/semana.html"
	s = open(ruta_Archivo,'r')
	Se =  s.read()
	soup2=BeautifulSoup(Se, 'html.parser')
	tags2=list()
	links2=list()
	titles2=list()
	count2=0
	titulo2=soup2.find_all('h2',class_="card-title")
	clase2=soup2.find_all('h2',class_='card-category')
	link2=soup2.find_all('a',href=True)

	for i in titulo2:
		if count2 < 8:
			a=i.get_text()
			titles2.append(a)
		else:
			break
		count2+=1
	count2=0

	for i in clase2:
		if count2 < 8:
			b=i.find('span').text
			tags2.append(b)
		else:
			break
		count2+=1
	count2=0

	for i in link2:
		if count2 < 8:
			c=i['href']
			links2.append("https://www.semana.com"+c)
		else:
			break
		count2+=1
	count2=0
	df2=pd.DataFrame({'Categoria':tags2,'Titulo':titles2,'Link':links2})
	df2.to_csv('/tmp/semana.csv', index = True)
	ruta_Archivo2 = "/tmp/semana.csv"
	s3.upload_file(ruta_Archivo2,'scrapinghtml',f'news/final/periodico=semana/year={anio}/month={mestexto}/day={dia}/semana.csv')
