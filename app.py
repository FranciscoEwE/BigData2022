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

	page=requests.get('https://www.bbc.com')
	soup=BeautifulSoup(page.content, 'html.parser')

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
			titles.append(i.string)
		else:
			break
		count+=1

	df=pd.DataFrame({'Categoria':tags,'Titulo':titles,'Link':links})
	df.to_csv("/tmp/bbc.csv")
	ruta_Archivo = "/tmp/bbc.csv"
	s3.upload_file(ruta_Archivo,'scrapinghtml',f'headlines/raw/periodico=bcc/year={anio}/month={mestexto}/day={dia}/bbc.csv')

	website2="https://www.semana.com"
	datospagina2=requests.get(website2)
	content2=datospagina2.text
	tags2=list()
	links2=list()
	titles2=list()
	count2=0
	soup2=BeautifulSoup(content2,'html.parser')
	box=soup2.find('div', class_='container HomeSemanaApertura')
	titulo2=box.find_all('h2',class_='card-title h4')
	clase2=box.find_all('h2',class_='card-category')
	link2=box.find_all('a',href=True)

	for i in titulo2:
		if count < 8:
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
	df2=pd.DataFrame({'Categoria':tags,'Titulo':titles,'Link':links})
	df2.to_csv('/tmp/semana.csv')
	ruta_Archivo2 = "/tmp/semana.csv"
	s3.upload_file(ruta_Archivo2,'scrapinghtml',f'headlines/raw/periodico=semana/year={anio}/month={mestexto}/day={dia}/semana.csv')
