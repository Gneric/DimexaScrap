import time, os, pandas as pd

import locale
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service

from pathlib import Path
from os.path import join

from config.globals import *

if __name__ == '__main__':

    def log(msg):
        print(f'{datetime.now()} - {msg} ')

    local_path = Path.cwd()
    chrome_driver_service =Service(join(local_path,'driver','chromedriver.exe'))
    browser = webdriver.Chrome(service=chrome_driver_service)
    browser.get(WEB_PAGE_URL)
    #browser.maximize_window()

    def scrapActionClick(xpath, val):
        browser.find_element(by=By.XPATH, value=xpath).click()
        time.sleep(val)

    def scrapActionKeys(xpath, text):
        browser.find_element_by_xpath(xpath).send_keys(text)

    current_year = datetime.strftime(datetime.now(), '%Y')
    current_month = datetime.strftime(datetime.now(), '%B').upper()

    # Login
    time.sleep(3)
    scrapActionKeys("//input[@id='z_d__l']", "P0786")
    scrapActionKeys("//input[@id='z_d__o']", "876451")
    scrapActionClick("//button[@id='z_d__r']", 15)

    for region in REGIONS:
            if region == 'AREQUIPA':
                log('Entrando a Venta Detallada')
                scrapActionClick("/html/body/div/div/div/div/div[2]/div/div/div/div/div/div/div/div[2]/table/tbody/tr/td/table/tbody/tr/td[1]/div/div[1]/table/tbody/tr/td/table/tbody/tr/td[17]/div/div/div/img", 15)
            else:
                log('Limpiando tabla')
                scrapActionClick("//div[contains(text(),'Ignorar')]", 1)
            # CboUnidad
            # log('Seleccionando CboUnidad')
            scrapActionClick("/html/body/div[3]/div[3]/div/div/div/div[1]/div[2]/table/tbody[2]/tr[1]/td[2]/div/i/input", 1)

            # Seleccionar Sede
            if region == 'AREQUIPA':
                log('Seleccionando sede Arequipa')
                scrapActionClick(f"//tbody//tr[@class = 'z-comboitem z-comboitem-seld']//td[text()='{region}']", 1)
            else:
                log(f'Seleccionando sede {region}')
                scrapActionClick(f"//tbody//tr[@class = 'z-comboitem']//td[text()='{region}']", 1)

            if region == 'AREQUIPA':
                print(f"Seleccionando CboBoxes de : Linea, Proveedor, Periodo y Año-Mes - {current_year}/{current_month}")
                # CboLinea
                #log('Selecionando CboLinea')
                scrapActionClick("/html/body/div[3]/div[3]/div/div/div/div[1]/div[2]/table/tbody[2]/tr[1]/td[4]/div/i/i", 1)
                # Seleccionar Softys
                #log('Selecionando Softys')
                scrapActionClick("/html/body/div[4]/table/tbody/tr/td[2]", 1)
                # CboPeriodo
                #log('Selecionando CboPeriodo')
                scrapActionClick("/html/body/div[3]/div[3]/div/div/div/div[1]/div[2]/table/tbody[2]/tr[2]/td[2]/div/i/i", 1)
                # Seleccionar Año-Mes
                #log('Selecionando CboAño-Mes')
                scrapActionClick(f"//*[contains(text(),'{current_month}') and starts-with(text(),'{current_year}')]", 1)

            #CboDivision
            #log('Selecionando Division')
            scrapActionClick("/html/body/div[3]/div[3]/div/div/div/div[1]/div[2]/table/tbody[2]/tr[1]/td[7]/div/i/i", 1)
            # Selecionar Todos
            #log('Selecionando Todos')
            scrapActionClick("/html/body/div[4]/table/tbody/tr[1]/td[2]", 1)
            # BtnProcesar
            log('Procesando data de '+ region)
            scrapActionClick("//button[@class='z-button-os']", GENERATE_SEC)
            # BtnExportar
            #log('Selecionando Exportar')
            scrapActionClick("//div[contains(text(),'Exportar')]", 3)

            # Lectura de xlsx y creacion de csv
            log('Leyendo excel y convirtiendo a csv')
            data = pd.read_excel(DOWNLOAD_FILE_PATH, sheet_name='Dimexa1')
            data.to_csv( join(local_path,'data',f'{region.capitalize()}','ventas.csv') , index=False, sep='|',header=False) 
            os.remove(DOWNLOAD_FILE_PATH)
            time.sleep(3)

    browser.close()