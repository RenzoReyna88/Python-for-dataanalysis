import requests
from bs4 import BeautifulSoup
import pandas as pd
from urllib.parse import urljoin
import io



def descargar_y_convertir_a_csv(url, nombre_csv_salida):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    link_element = soup.select_one('div[role=main] div.container a[href]', href=True)

    try:
    
        if link_element:
            archivo_url = urljoin(url, link_element['href'])
            #desacargar archivo
            archivo_response = requests.get(archivo_url)
            # Determinar el tipo de archivo (csv, xlsx, json) y convertirlo a CSV
            if 'csv' in archivo_response.headers['Content-Type']:
                df = pd.read_csv(io.StringIO(archivo_response.text))
            elif 'excel' in archivo_response.headers['Content-Type']:
                df = pd.read_excel(io.BytesIO(archivo_response.content))
            elif 'json' in archivo_response.headers['Content-Type']:
                df = pd.read_json(archivo_response.text)
            else:
                print("Tipo de archivo no compatible.")
                return
                
            # Guardar el DataFrame como archivo CSV
            df.to_csv(nombre_csv_salida, index=False)
            print(f"Archivo descargado y convertido a CSV: {nombre_csv_salida}")
        else:
            print("No se encontró un enlace válido.")
    except Exception as error:
        print(f'se obtuvo el sigueinte error:{error}')

# URL scrapeada y luego almacenada en ruta preestablecida
url_pagina = 'https://datosestadistica.cba.gov.ar/dataset/8c22918c-11c9-4e97-9b86-39967c537a9f/resource/a789bf51-6d05-423d-90cc-f10497731398/download/alumnos-con-sobredad.xlsx'
nombre_archivo_csv_salida = r'C:\Users\r_ger\OneDrive\Escritorio\web-scraper-python\alumnos_con_sobredad.csv'

descargar_y_convertir_a_csv(url_pagina, nombre_archivo_csv_salida)












