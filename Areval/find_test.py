def findVendaAR():
    from selenium import webdriver
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.ui import WebDriverWait
    from webdriver_manager.chrome import ChromeDriverManager
    from selenium.webdriver.chrome.service import Service
    from main import linksVenda
    from joblib import Parallel, delayed
    from time import time

    time_start = time()

    links = linksVenda()

    service = Service(ChromeDriverManager().install())

    chrome_options = webdriver.ChromeOptions()
    #chrome_options.add_argument("headless")
    driver = webdriver.Chrome(chrome_options=chrome_options, service=service)

    infos_sub_primary = ["usable_floor_area", "gross_floor_area", "land_dimensions", "bedrooms", "suites", "bathrooms", "garages"]
    
    #Área construída, área do terreno, dimensões do terreno, dormitórios, suítes, banheiros, vagas garagem, descrição, características, código do imóvel, bairro, valor

    def scraping_links(link):
        infos_link = [[],[],[],[],[],[],[],[],[],[],[],[]]

        driver.get(link)
        print(link)

        infos_primary = driver.find_elements(By. CLASS_NAME, "item-info.digital")

        for info_primary in infos_primary:
            try: infos_link[infos_sub_primary.index(info_primary.get_attribute("class").split(" ")[-1])].append(info_primary.find_element(By. TAG_NAME, "span").text.split("\n")[0].split(" ")[0])
            except: pass

        #Descrição:
        try: infos_link[7].append(driver.find_element(By. XPATH, "/html/body/div[3]/section/div/div/div/div[5]/div/div[1]/div[5]/div/span").text)
        except: pass

        #Características:
        try: infos_link[8].append(driver.find_element(By. XPATH, "/html/body/div[3]/section/div/div/div/div[5]/div/div[1]/div[6]/div/div/div/div/div/div").text)
        except: pass

        #Código do imóvel:
        try: infos_link[9].append(driver.find_element(By. XPATH, "/html/body/div[3]/section/div/div/div/div[3]/div/p/span").text)
        except: pass

        #Bairro:
        neighborhood_local_divs = driver.find_elements(By. CLASS_NAME, "hidden-mobile")[0].find_elements(By. TAG_NAME, "li")
        for i in range(1, len(neighborhood_local_divs) + 1):
            try: 
                infos_link[10].append(neighborhood_local_divs[-i].find_elements(By. TAG_NAME, "a")[0].get_attribute("text"))
                break   
            except: pass

        #Valor:    
        code = driver.find_element(By.XPATH, "/html/body/div[3]/section/div").get_attribute(("id"))
        try: infos_link[11].append(driver.find_element(By.XPATH, f"//*[@id='{code}']/div/div/div[5]/div/div[1]/div[2]/div/div/div/ul/li/p/span[2]/span[1]").text.split(" ")[-1].replace(".",""))
        except: pass
        
        #Adiciona None nos campos sem informações
        for info_verify in infos_link:
            if len(info_verify) == 0: info_verify.append("None")

        return infos_link
    
    infos = []

    infos_returned = Parallel(n_jobs=10, prefer="threads")(delayed(scraping_links)(link) for link in links)

    for f in range(len(infos_returned[0])):
        infos.append([n[f][0] for n in infos_returned])

    time_final = time()
    
    print(infos)
    print(f"{time_final - time_start} segundos")

findVendaAR()