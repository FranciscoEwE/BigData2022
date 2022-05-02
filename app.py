from urllib.request import Request
from urllib.request import urlopen
from six.moves import urllib
import boto3
import datetime

def guardarhtml(event, context):
        s3 = boto3.client('s3')
        fecha = datetime.datetime.now()
        anio = fecha.year
        print(anio)
        mestexto = fecha.strftime("%B")
        mes = fecha.month
        dia = fecha.day

        urllib.request.urlretrieve('https://www.bbc.com/', '/tmp/bbc.html')

        ruta_Archivo = "/tmp/bbc.html"
        s3.upload_file(ruta_Archivo,'htmlnews',f'headlines/raw/periodico=BBC/year={anio}/month={mestexto}/day={dia}/bbc.html')

        urllib.request.urlretrieve('https://www.semana.com/', '/tmp/semana.html')
        ruta_Archivo2 = "/tmp/semana.html"
        s3.upload_file(ruta_Archivo2,'htmlnews',f'headlines/raw/periodico=semana/year={anio}/month={mestexto}/day={dia}/semana.html')
