def findVendaAR(service, options) -> list:
    from selenium.webdriver.common.by import By
    try: from Areval.main import linksVendaAR
    except: from main import linksVendaAR
    from time import time
    from selenium import webdriver

    time_start = time()

    links = linksVendaAR(service, options)

    driver = webdriver.Chrome(options=options, service=service)

    infos_sub_primary = ["usable_floor_area", "gross_floor_area", "land_dimensions", "bedrooms", "suites", "bathrooms", "garages"]
    
    #Área construída, área do terreno, dimensões do terreno, dormitórios, suítes, banheiros, vagas garagem, descrição, características, código do imóvel, bairro, valor
    infos = [[],[],[],[],[],[],[],[],[],[],[],[]]

    for link in links:
        driver.get(link)
        print(f"{links.index(link)+1}/{len(links)}", link)

        infos_primary = driver.find_elements(By. CLASS_NAME, "item-info.digital")

        for info_primary in infos_primary:
            try: infos[infos_sub_primary.index(info_primary.get_attribute("class").split(" ")[-1])].append(info_primary.find_element(By. TAG_NAME, "span").text.split("\n")[0].split(" ")[0])
            except: pass

        #Descrição:
        try: infos[7].append(driver.find_element(By. XPATH, "/html/body/div[3]/section/div/div/div/div[5]/div/div[1]/div[5]/div/span").text)
        except: pass

        #Características:
        try: infos[8].append(driver.find_element(By. XPATH, "/html/body/div[3]/section/div/div/div/div[5]/div/div[1]/div[6]/div/div/div/div/div/div").text)
        except: pass

        #Código do imóvel:
        try: infos[9].append(driver.find_element(By. XPATH, "/html/body/div[3]/section/div/div/div/div[3]/div/p/span").text)
        except: pass

        #Bairro:
        neighborhood_local_divs = driver.find_elements(By. CLASS_NAME, "hidden-mobile")[0].find_elements(By. TAG_NAME, "li")
        for i in range(1, len(neighborhood_local_divs) + 1):
            try: 
                infos[10].append(neighborhood_local_divs[-i].find_elements(By. TAG_NAME, "a")[0].get_attribute("text"))
                break   
            except: pass

        #Valor:    
        code = driver.find_element(By.XPATH, "/html/body/div[3]/section/div").get_attribute(("id"))
        try: infos[11].append(driver.find_element(By.XPATH, f"//*[@id='{code}']/div/div/div[5]/div/div[1]/div[2]/div/div/div/ul/li/p/span[2]/span[1]").text.split(" ")[-1].replace(".",""))
        except: pass
        
        #Adiciona None nos campos sem informações
        for info_verify in infos:
            if len(info_verify) < links.index(link) + 1: info_verify.append("None")

    time_final = time()
    print(f"{time_final - time_start} segundos")

    return infos