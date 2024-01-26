def findVendaAP(service, options) -> list:
    from selenium import webdriver
    from selenium.webdriver.common.by import By
    try: from Alpha.main import linksVendaAP
    except: from main import linksVendaAP

    links = linksVendaAP(service, options)

    driver = webdriver.Chrome(options=options, service=service)

    #Área do Terreno, área privativa, dormitórios, suítes, banheiros, vagas garagem, endereço, código do imóvel, valor
    infos = [[],[],[],[],[],[],[],[],[]]

    infos_sub_primary = [["de lote", "área privativa", "demi-suites", "suíte", "lavabo", "banheiro", "vaga"],
                         [0,1,2,3,4,4,5]]
    
    for link in links:
        driver.get(link)
        print(link)

        divs_infos_ad = []

        for div_infos in driver.find_elements(By.CLASS_NAME, "block.imovel-ver-informacoes.width-100"):

            divs_infos_ad.extend(div_infos.find_elements(By.TAG_NAME, "li"))

        for div_info in divs_infos_ad:
            info_title = div_info.text.strip()[div_info.text.find(" "):].lower().replace("m²","").strip()

            try: index = infos_sub_primary[1][infos_sub_primary[0].index(info_title)]
            except: 
                if div_info.find_elements(By.TAG_NAME, "i")[0].get_attribute("class") == "icl ic-map-marker-alt":
                    infos[6].append(div_info.text.strip())
                continue

            info_content = float(div_info.text.strip()[:div_info.text.find(" ")].replace("m²","").replace(".","").replace(",","."))

            if len(infos[index]) == links.index(link) + 1: infos[index][-1] += info_content
            else: infos[index].append(info_content)

        #Código do imóvel
        infos[7].append(driver.find_element(By.XPATH, '//*[@id="content"]/section/div[3]/div[1]/div[1]/h2/span').text.replace("ID:","").strip())

        #Valor:
        try: infos[8].append(float(driver.find_element(By.CLASS_NAME, "imovel-ver-preco.strong").replace("R$","").replace(".","").replace(",",".").strip()))
        except: pass

        #Adiciona None nos campos sem informações e converte para inteiro os valores possíveis:
        for info in infos:
            if len(info) < links.index(link) + 1: info.append("None")
            try: info[-1] = int(info[-1])
            except: pass

    print(infos)
    return infos

from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium import webdriver

service = Service(ChromeDriverManager().install())
options = Options()
options.add_argument("headless")
options.add_argument('log-level=3')
options.add_argument('--blink-settings=imagesEnabled=false')

findVendaAP(service, options)