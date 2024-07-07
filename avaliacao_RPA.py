from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import re
import os

# Leitura da pasta dowload
usuario = os.getlogin()
diretorio = (f"C:/Users/{usuario}/Downloads")
arquivos = os.listdir(diretorio)
alvo = 'python-3.11.9-amd64.exe'

# Separa arquivos por padroes
list_python = []
list_outros = []
for i in arquivos:
    padrao1 = r'python-3\.11\.9-amd64\.exe' #Padrão 1, busca encontrar o arquivo sem numeração
    padrao2 = r'python-3\.11\.9-amd64 \(\d+\)\.exe' #Padrão 1, busca encontrar o arquivo com numeração

    # Salva o nome dos arquivos que corresponde aos padroes
    corresponde1 = re.findall(padrao1, i)
    corresponde2 = re.findall(padrao2, i)
    if corresponde1 or corresponde2:
        list_python.extend(corresponde1)
        list_python.extend(corresponde2)
    else:
        list_outros.append(i)

# Configura o webdriver para não bloquear o dowload, evitando ação humana
options = webdriver.ChromeOptions()
prefs = {
    "download.default_directory": "/caminho/para/o/diretorio/de/downloads",
    "download.prompt_for_download": False,
    "download.directory_upgrade": True,
    "safebrowsing.enabled": True
}
options.add_experimental_option("prefs", prefs)

# abre webdriver com as opções configuradas
driver = webdriver.Chrome(options=options)

# Tempo de espera para carregar paginas
driver.implicitly_wait(10)

#Acessar URL do google 
driver.get("https://www.google.com")

# Seleciona XPATH da barra de pesquisa e atribui o valor de 'baixar python'
driver.find_element(By.XPATH,'/html/body/div[1]/div[3]/form/div[1]/div[1]/div[1]/div/div[2]/textarea').send_keys('baixar python')

# Realiza o click para a pesquisa acontecer
driver.find_element(By.XPATH, '/html/body/div[1]/div[3]/form/div[1]/div[1]/div[2]/div[4]/div[6]/center/input[1]').click()

# Identifica a pagina com padrão 'https://www.python.org' e 'Download Python | Python.org', apos encontrar o padão o click é realizado.
for i in driver.find_elements(By.PARTIAL_LINK_TEXT, 'https://www.python.org'):
    print(i.text)
    if i.text == driver.find_element(By.PARTIAL_LINK_TEXT, 'Download Python | Python.org').text:
        print(i.text)
        i.click()
        break

# Seleciona XPATH para acessar dowload no site
driver.find_element(By.XPATH, '//*[@id="downloads"]').click()

# Percorre a lista até encontrar a versão correta.
for i in driver.find_elements(By.XPATH, '//*[@id="content"]/div/section/div[2]/ol/li'):
    if i.text[0:13] == 'Python 3.11.9':
        i.click()
        break

# Percorre a lista até encontrar a versão de windows 64. 
for i in driver.find_elements(By.XPATH, '//*[@id="content"]/div/section/article/table/tbody/tr/td'):
    if i.text == 'Windows installer (64-bit)':
        i.click()
        break

# Utiliza a primeira verificação de dowloads para mapear entradas de novos arquivos,
# em caso de novos arquivos haverá uma verificação de padrão, se corresponder ao padrão, o loop é finalizado. 
while True:
    list_python_nova = list_python
    usuario = os.getlogin()
    diretorio = f"C:/Users/{usuario}/Downloads"
    arquivos = os.listdir(diretorio)
    
    for arquivo in arquivos:
        if arquivo not in list_python and arquivo not in list_outros:
            padrao1 = r'python-3\.11\.9-amd64\.exe' #Padrão 1, busca encontrar o arquivo sem numeração
            padrao2 = r'python-3\.11\.9-amd64 \(\d+\)\.exe' #Padrão 2, busca encontrar o arquivo com numeração

            # Salva o nome dos arquivos que corresponde aos padroes
            corresponde1 = re.findall(padrao1, arquivo) 
            corresponde2 = re.findall(padrao2, arquivo)
            if corresponde1 or corresponde2:
                driver.quit()
                break  # Sair do loop quando o arquivo é encontrado
    else:
        continue # Recomeça o loop caso o arquivo não seja encontrado 
    break  # Sair do loop while