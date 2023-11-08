import warnings
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException
import glob
import pandas as pd
import time
import requests


import os
import sys
__file__ = os.path.abspath(__file__)
path = os.path.dirname(__file__)
mainpath = os.path.split(path)
sys.path.append(mainpath[0])
warnings.filterwarnings("ignore")


import dependencias
from dependencias.WebDriverLocal import start_browser


def selenium(browser,downloadpath):
    '''

    [Descripcion]

    [Creación]

        1. Autor:  Wilber Lopez Mucia
        2. Dia de Creación: 15/08/2023
        3. Incident: Descarga de datos de población de diferentes paises de interes  desde el año 1950 hasta la 2100

            
    [Funciones]

        selection_countries= función para seleccionar los paises de interes para la busqueda
        select_link= Función para obtener el link para redirigirse a las paginas 1950-2020, y 2020-2100
        select_countries= función que busca en todas las etiquetas de html, y selecciona solo los de interes a partir de una lista de paises predeterminados
        select= función que permite seleccionar filtros determinador a a partir de los nombres de interes como lo pueden ser ALL o No chance
        concatenar= función que busca todos los archivos csv descargados anteriormente, y los reordena para luego concatenarlos en un unico archivo
                    
   

    ''' 

    #------------------------------------
    # FUNCIONES
    #------------------------------------
    def select_link(lista, param_word):
        for option in lista:
            try:
                if param_word in option:
                    browser.get(option)
                    break
            except:
                print("No se pudo acceder a la página:", option)

    def selection_countries(lista, countries):        
        for country in countries:
            if country.text in lista:
                
                country.click()
    
    def select(lista, param_word):
        for option in lista:
            if option.text==param_word:
                option.click()
        
    def concatenar(lista_csv):
        list_csv=[]
        for file in lista_csv:
            df=pd.read_csv(file, delimiter=',')
            df=df.drop(df.columns[1], axis=1)
            list_columns=df.columns
            df_melt = pd.melt(df, id_vars=['Country'], value_vars=list_columns[:], var_name='Year', value_name='Population')
            
            list_csv.append(df_melt)
        df_concat=pd.concat(list_csv)
        return df_concat.sort_values(by=['Country', 'Year'])   

    #------------------------------------
    # MAIN
    #------------------------------------

    #------------------------------------
    # VARIABLES DE CONFIGURACION
    #----------------------------------------------------------------------------------------------------------------------------
    url='https://world-statistics.org'
    final_path=os.path.join(path, "Final_path")
    #browser.get(url)
    
    

    ########################################################
    # verificar que la pagina este online
    ########################################################
    try:
        status_genereport=requests.get(url).status_code
    except:
        status_genereport=None
    if status_genereport!=200:
        raise ValueError('La página esta caida')
    else:
        browser.get(url)


    

    #Acceder a la opción Indicador a partir de una lista de href
    indicator=WebDriverWait(browser, 60).until(EC.presence_of_all_elements_located((By.XPATH, '//ul[@class="nav-main"]/li/a')))
    list_indicators=[icons.get_attribute("href") for icons in indicator]
    select_link(list_indicators, "indicators") #ir al link de la pestaña indicators
    

    #buscar y seleccionar la población entre 1950-2020
    WebDriverWait(browser, 60).until(EC.presence_of_element_located((By.ID, "aTopic11"))).click()
    WebDriverWait(browser, 60).until(EC.element_to_be_clickable((By.XPATH, '//div[@id="subtopic117"]/a'))).click()
    population=WebDriverWait(browser, 60).until(EC.presence_of_all_elements_located((By.XPATH, '//div[@id="list117"]/a')))
    list_populations=[selection.get_attribute("href") for selection in population]
    select_link(list_populations, "1950-2020")
    
    time.sleep(3)

    #seleccionar los paises
    list_country=['Argentina', 'Bolivia (Plurinational State of)', 'Brazil', 'Chile', 'Colombia', 'Ecuador', 'Guyana', 'Paraguay', 'Peru', 'Suriname', 'Trinidad and Tobago', "Uruguay",'Venezuela (Bolivarian Republic of)']
    #'Colombia', 'Ecuador', 'Guyana', 'Paraguay', 'Peru', 'Suriname', 'Trinidad and Tobago', "Uruguay",'Venezuela (Bolivarian Republic of)'
    countries=WebDriverWait(browser, 60).until(EC.presence_of_all_elements_located((By.XPATH, "//select[@id='selcountry']/option")))
    selection_countries(list_country, countries)   

    #seleccionar la opción all del display lines
    display= WebDriverWait(browser, 60).until(EC.presence_of_all_elements_located((By.XPATH, '//div[@id="myTable_length"]/label/select/option')))
    select_all=select(display, 'All')
    #descargar el primer archivo csv 1950-2020
    WebDriverWait(browser, 60).until(EC.element_to_be_clickable((By.XPATH, "//div[@class='dt-buttons']/a[3]"))).click()        
    
    #regresar browser indicator
    WebDriverWait(browser, 60).until(EC.element_to_be_clickable((By.XPATH, '//div[@class="block-content bg-gray-lighter"]/fieldset/p/span/a'))).click()
    WebDriverWait(browser, 60).until(EC.presence_of_element_located((By.ID, "aTopic11"))).click()
    WebDriverWait(browser, 60).until(EC.element_to_be_clickable((By.XPATH, '//div[@id="subtopic117"]/a'))).click()
    select_link(list_populations, "2020-2100")
    time.sleep(3)

    #----------------------------------------
    # seleccionar los primeros  cuatro paises
    #----------------------------------------
    list_country=['Argentina', 'Bolivia (Plurinational State of)', 'Brazil', 'Chile' ]
    countries=WebDriverWait(browser, 60).until(EC.presence_of_all_elements_located((By.XPATH, "//select[@id='selcountry']/option")))
    selection_countries(list_country, countries)
    

    #seleccionar la opción all
    display= WebDriverWait(browser, 60).until(EC.presence_of_all_elements_located((By.XPATH, '//div[@id="myTable_length"]/label/select/option')))  
    select_all=select(display, 'All')

    #seleccionar la opción no chance
    variant=WebDriverWait(browser, 60).until(EC.presence_of_all_elements_located((By.XPATH, '//select[@id="selColDim1"]/option')))
    no_change=select(variant, 'No change')
    #descarga el archivo
    WebDriverWait(browser, 60).until(EC.element_to_be_clickable((By.XPATH, "//div[@class='dt-buttons']/a[3]"))).click()

    #--------------------------------seleccionar los desde colombia hasta paraguay---------------------------
    browser.refresh() #recargar la pagina selecionar el otro conjunto de paises
    time.sleep(2) #dejar cargar las etiquetas de html
    list_country=['Colombia', 'Ecuador', 'Guyana', 'Paraguay' ]
    countries=WebDriverWait(browser, 60).until(EC.presence_of_all_elements_located((By.XPATH, "//select[@id='selcountry']/option")))
    selection_countries(list_country, countries)
   
    #seleccionar la opción all
    display= WebDriverWait(browser, 60).until(EC.presence_of_all_elements_located((By.XPATH, '//div[@id="myTable_length"]/label/select/option')))  
    select_all=select(display, 'All')
    #seleccionar la opción no chance
    variant=WebDriverWait(browser, 60).until(EC.presence_of_all_elements_located((By.XPATH, '//select[@id="selColDim1"]/option')))
    no_change=select(variant, 'No change')
    #descarga el archivo
    WebDriverWait(browser, 60).until(EC.element_to_be_clickable((By.XPATH, "//div[@class='dt-buttons']/a[3]"))).click()

    #--------------------------------seleccionar el último conjunto de paises-----------------------------------#
    browser.refresh() #recargar la pagina selecionar  otro conjunto de paises

    time.sleep(2) #dejar cargar las etiquetas de html
    list_country=[ 'Peru', 'Suriname', 'Trinidad and Tobago', "Uruguay",'Venezuela (Bolivarian Republic of)' ]
    countries=WebDriverWait(browser, 60).until(EC.presence_of_all_elements_located((By.XPATH, "//select[@id='selcountry']/option")))
    selection_countries(list_country, countries)
   
    #seleccionar la opción all
    display= WebDriverWait(browser, 60).until(EC.presence_of_all_elements_located((By.XPATH, '//div[@id="myTable_length"]/label/select/option')))  
    select_all=select(display, 'All')
    #seleccionar la opción no chance
    variant=WebDriverWait(browser, 60).until(EC.presence_of_all_elements_located((By.XPATH, '//select[@id="selColDim1"]/option')))
    no_change=select(variant, 'No change')
    #descarga el archivo
    WebDriverWait(browser, 60).until(EC.element_to_be_clickable((By.XPATH, "//div[@class='dt-buttons']/a[3]"))).click()


    ##-----------------------------------------------------------------------------------------------------------------
    #buscar los documentos descargados 'World statics' para luego  luego concatenarlos
    list_data = glob.glob(os.path.join('./Download', "*.csv"))

    # Leer cada archivo CSV y concatenarlos en uno solo
    data=concatenar(list_data)

    # Exportar los datos concatenados a un archivo CSV
    data.to_csv("populations_1950-2100.csv", index=False)

   
        # ----------------------------------------------------------------------------------------------------------------------------
    


if __name__ == '__main__':
    downloadpath = os.path.join(path, "Download") 
    mozilla_bin = r'C:\Program Files\Mozilla Firefox\firefox.exe'
    browser = start_browser(downloadpath, mozilla_bin)
    selenium(browser, downloadpath)
    
    