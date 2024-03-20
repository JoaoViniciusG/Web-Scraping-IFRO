def findVendaME_CC(service, options) -> list:
    from selenium import webdriver
    from selenium.webdriver.common.by import By
    try: from ME_CC__MariaEich_Colatto.main import linksVendaME_CC
    except: from main import linksVendaME_CC
    import time

    links = linksVendaME_CC(service, options)

    driver = webdriver.Chrome(options=options, service=service)
    
    #Área total, área do terreno, área construída, área útil, dormitórios, suítes, banheiros, vagas garagem, descrição,
    #código do imóvel, bairro, endereço, valor
    infos = [[],[],[],[],[],[],[],[],[],[],[],[],[]]

    infos_sub_primary = [["total", "terreno", "construída", "útil", "dormitório", "suíte", "banheiro", "vaga"],[0,1,2,3,4,5,6,7]]

    for link in links:
        driver.get(link)
        print(f"{links.index(link)+1}/{len(links)}", link)

        for div_info in driver.find_elements(By. CLASS_NAME, "esquerda_ficha")[0].find_elements(By. CLASS_NAME, "detalhe"):
            for text_info in div_info.text.replace("sendo","/").split(" / "):
                text_sub = text_info.split(" ")[-1]
                if text_sub == "": break
                if text_sub[-1] == "s": text_sub = text_sub[:-1]
                try: index = infos_sub_primary[1][infos_sub_primary[0].index(text_sub)]
                except: break

                infos[index].append(text_info.split(" ")[0].replace("m²","").strip())
                if text_sub == "vaga": break

        
        #Descrição:
        try: infos[8].append(driver.find_element(By. XPATH, "/html/body/div[7]/div[2]/div[5]/div").text)
        except: pass

        #Código do imóvel:
        try: infos[9].append(driver.find_element(By. XPATH, "/html/body/div[7]/div[2]/div[3]/div[1]/div[2]/span[2]").text)
        except: pass

        #Bairro:
        try: 
            text_neighborhood = driver.find_elements(By.CLASS_NAME, "cidade_bairro")[0].text
            infos[10].append(text_neighborhood[text_neighborhood.find("-")+1:].strip())
        except: pass

        #Endereço:
        try: 
            text_address = driver.find_element(By. XPATH, "/html/body/div[7]/div[2]/div[3]/h2").text
            if driver.find_element(By. XPATH, "/html/body/div[7]/div[2]/div[3]/h1/span").text.find("undefined") == -1: text_address += driver.find_element(By. XPATH, "/html/body/div[7]/div[2]/div[3]/h1/span").text
            infos[11].append(text_address)
        except: pass

        #Valor:
        try: 
            div_price = driver.find_elements(By.CLASS_NAME, "valor")[0]
            infos[12].append(float(div_price.find_elements(By.TAG_NAME, "h3")[0].text.replace("R$","").replace(".","").replace(",",".").strip()))
        except: pass

        #Adiciona None nos campos sem informações:
        for info_verify in infos:
            if len(info_verify) < links.index(link) + 1: info_verify.append("None")

        if links.index(link) == 33: break

    return infos