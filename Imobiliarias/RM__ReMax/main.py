from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC 
from time import sleep

types_of_add = [["apartamento", "barracão", "galpão", "casa", "sobrado", "terreno", "prédio", "sala comercial", "salao comercial", "ponto comercial"],
                   ["AP", "BA", "BA", "CA", "SO", "TE", "PR", "SA", "SA", "PT"]]

def linksVendaRM(service, options) -> list:
    #Links, Tipo do Imóvel, Tipo de Negócio
    global links_infos
    links_infos = [[],[],[]]

    driver = webdriver.Chrome(options=options, service=service)
    driver.get('https://www.remax.com.br/PublicListingList.aspx?SelectedCountryID=55&CityID=6581546')

    while True:
        WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.ID, 'hiddenRTL')))
    
        for div_ad in driver.find_elements(By.CLASS_NAME, "gallery-item-container"):
            #Remove os imóveis já vendidos
            try:
                if div_ad.find_elements(By.CLASS_NAME, "exclusive-banner.drop-shadow")[0].text.lower() in ("vendido", "alugado"): continue
            except: pass

            #Remove os imóveis rurais:
            ad_type = div_ad.find_elements(By.CLASS_NAME, "gallery-transtype")[0].text.lower()

            for word in ("chácara","sítio","fazenda"):
                if ad_type.find(word) != -1: break
            else: 
                #Função que coleta as informações
                collectInfos(div_ad)
                

        next_li = driver.find_elements(By.CLASS_NAME, "pagination")[0].find_elements(By.TAG_NAME, "li")[-1]
        
        try:
            next_a = next_li.find_elements(By.TAG_NAME, "a")[0]
            
            for info in driver.current_url.split("&"):
                if info.find("page=") != -1: current_page = int(info[5:])

            next_a.click()
        except: break

        while True:
            for info in driver.current_url.split("&"):
                if info.find("page=") != -1: page = int(info[5:])
            if page != current_page: break
            sleep(0.5)

    driver.quit()
    return links_infos


def collectInfos(element_master):
    #Preenche o campo "Links":
    links_infos[0].append(element_master.find_elements(By.CLASS_NAME, "LinkImage")[0].get_attribute("href"))
    
    #Preenche o campo "Tipo do Imóvel":
    ad_type = element_master.find_element(By.CLASS_NAME, "gallery-transtype").text.lower()

    for index_type, type_add_verify in enumerate(types_of_add[0]):
            if ad_type.find(type_add_verify) != -1: 
                links_infos[1].append(types_of_add[1][index_type])
                break
    else: links_infos[1].append("None")

    #Preenche o campo "Tipo de Negócio":     
    negc_type = element_master.find_element(By.CLASS_NAME, "card-trans-type.collection-card.drop-shadow").text.lower()

    if negc_type == "venda": links_infos[2].append("VE")
    elif negc_type == "alugar": links_infos[2].append("LO")
    else: links_infos[2].append("None")