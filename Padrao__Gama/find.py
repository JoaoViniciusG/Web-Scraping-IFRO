def findVendaGA_PD(service, options) -> list:
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC 
    from selenium.webdriver.chrome.options import Options
    from joblib import Parallel, delayed
    try: from Padrao__Gama.main import linksVendaGA_PD
    except: from main import linksVendaGA_PD
    from selenium import webdriver
    
    from time import sleep

    links = linksVendaGA_PD(service, options)
    
    options = Options()
    options.add_argument('log-level=3')
    options.add_argument('--blink-settings=imagesEnabled=false')

    driver = webdriver.Chrome(options=options, service=service)
    driver.maximize_window()

    infos_sub_primary = [["Área Útil","Área do Terreno", "Área Construída", "Dormitório", "Suíte", "Banheiro", "Vaga"],
                         [0,1,2,3,4,5,6]]
    
    #Área útil, área do terreno, área do construída, dormitórios, suítes, banheiros, vagas garagem, descrição, código do imóvel, bairro, valor
    infos = [[],[],[],[],[],[],[],[],[],[],[]]
    
    for link in links:
        driver.get(link)
        print(f"{links.index(link)+1}/{len(links)}", link)

        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By. XPATH, '//*[@id="widget-container"]/mat-card/imobzi-widget-card/mat-card/mat-card-actions/imobzi-buttons-actions/button')))

        infos_primary = driver.find_elements(By. CLASS_NAME, "attributes-item.ng-star-inserted")

        for info_primary in infos_primary:
            info_primary_title = info_primary.get_attribute("title")
            if info_primary_title[-1] == "s": info_primary_title = info_primary_title[:-1]

            try: index = infos_sub_primary[1][infos_sub_primary[0].index(info_primary_title)]
            except: continue

            infos[index].append(info_primary.text.split(" ")[0].replace("m²",""))

        #Descrição:
        try: infos[7].append(driver.find_element(By. XPATH, '//*[@id="property-abstract"]/div[2]/div[4]/div').text)
        except: pass
        
        #Código do Imóvel:
        infos[8].append(int(link.split("code-")[-1]))

        #Bairro:
        text_neighborhood = driver.find_element(By. XPATH, '//*[@id="property-abstract"]/div[2]/imobzi-property-title/div/h3').text
        text_neighborhood = text_neighborhood.replace("(vende-se)", "").replace("- Vilhena", "").replace(", RO","").split("em")[-1].strip()
        infos[9].append(text_neighborhood)

        #Valor:
        try: infos[10].append(driver.find_element(By. XPATH, '//*[@id="property-widget"]/div[1]/h3[2]').text.replace("R$","").replace(".","").replace(",",".").strip())
        except: pass

        #Adiciona None nos campos sem informações
        for info_verify in infos:
            if len(info_verify) < links.index(link) + 1: info_verify.append("None")

    driver.quit()
    return infos