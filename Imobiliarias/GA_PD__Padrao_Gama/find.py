def findVendaGA_PD(service, options) -> list:
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC 
    from selenium.webdriver.chrome.options import Options
    try: from Imobiliarias.GA_PD__Padrao_Gama.main import linksVendaGA_PD
    except: from main import linksVendaGA_PD
    from selenium import webdriver
    
    from time import sleep
    
    options = Options()
    options.add_argument('log-level=3')
    options.add_argument('--blink-settings=imagesEnabled=false')

    links_infos = linksVendaGA_PD(service, options)

    driver = webdriver.Chrome(options=options, service=service)
    driver.maximize_window()

    infos_sub_primary = [["área útil","área do terreno", "área construída", "dormitório", "suíte", "banheiro", "vaga"],
                         [1,2,3,4,5,6,7]]
    
    #(0) Url, (1) área total (área útil), (2) área do terreno (excluída ao final), (3) área construída, (4) dormitórios, (5) suítes, (6) banheiros, (7) vagas garagem, (8) bairro, (9) valor, (10) tipo de imóvel, (11) tipo de negócio, (12) descrição
    infos = [[],[],[],[],[],[],[],[],[],[],[],[],[]]
    
    for index_links, link in enumerate(links_infos[0]):
        driver.get(link)
        print(f"{links_infos[0].index(link)+1}/{len(links_infos[0])}", link)

        pg_404 = False

        while True:
            try:
                WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By. XPATH, '//*[@id="widget-container"]/mat-card/imobzi-widget-card/mat-card/mat-card-actions/imobzi-buttons-actions/button')))
                break
            except:
                if driver.current_url == "https://www.gamavilhena.com.br/pagina-nao-encontrada":
                    pg_404 = True
                    break

        if pg_404 == True: continue

        #Preenche os campos "Links", "Tipo do Imóvel" e "Tipo de Negócio":
        infos[0].append(link)
        infos[10].append(links_infos[1][index_links])
        infos[11].append(links_infos[2][index_links])

        infos_primary = driver.find_elements(By. CLASS_NAME, "attributes-item.ng-star-inserted")

        for info_primary in infos_primary:
            info_primary_title = info_primary.get_attribute("title").lower()
            if info_primary_title[-1] == "s": info_primary_title = info_primary_title[:-1]

            try: index = infos_sub_primary[1][infos_sub_primary[0].index(info_primary_title)]
            except: continue

            res = info_primary.text.split(" ")[0].replace("m²","")

            try:
                res = float(res)
                if res == int(res): res = int(res)
            except: pass

            infos[index].append(res)

        #Bairro:
        text_neighborhood = driver.find_element(By. XPATH, '//*[@id="property-abstract"]/div[2]/imobzi-property-title/div/h3').text
        text_neighborhood = text_neighborhood.replace("(vende-se)", "").replace("- Vilhena", "").replace(", RO","").split(" em ")[-1].split(" no ")[-1].strip()
        infos[8].append(text_neighborhood)

        #Valor:
        try: 
            text_value = driver.find_element(By. XPATH, '//*[@id="property-widget"]/div[1]/h3[2]').text.replace("R$","").replace(".","").replace(",",".").strip()
            infos[9].append(text_value)
        except: pass

        #Descrição:
        try: 
            text_description = driver.find_element(By. CLASS_NAME, 'property-description.h3.col-xs-12.col-sm-12.col-md-8.col-lg-8.col-xl-10.ng-star-inserted').text
            infos[12].append(text_description)
        except: pass

        #Adiciona None nos campos sem informações
        for info_verify in infos:
            if len(info_verify) < links_infos[0].index(link) + 1: info_verify.append("None")


        #Filtra a área total correta entre os campos "Área Total" e "Área do Terreno":
        areaTotal = infos[1][-1]
        areaTerreno = infos[2][-1]
        areaCons = infos[3][-1] 

        areas = [infos[1][-1], infos[2][-1], infos[3][-1]]

        areas = sorted([val for val in areas if val != "None"])
        
        areas = sorted(list(set(areas)))

        if areaTotal != "None" and areaTotal == areas[-1]: 
            pass

        elif len(areas) > 1 or (len(areas) == 1 and (areas[0] == areaTotal or areas[0] == areaTerreno)):
            infos[1][-1] = areas[-1]

        #Filtra a área construída correta entre todos os campos de área caso o campo "Área Construída" seja igual a "None":
            
        if areaCons != "None" and areaCons == areas[0]:
            pass

        elif len(areas) > 1 or (len(areas) == 1 and areas[0] == areaCons):
            infos[3][-1] = areas[0]

    
    #Deleta o campo "Área do Terreno" pois todas as suas informações pertinentes já foram movidas para o campo "Área Total":
    del infos[2]

    driver.quit()
    return infos