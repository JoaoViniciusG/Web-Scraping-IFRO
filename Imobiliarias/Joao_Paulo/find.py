def findVendaJP(service, options) -> list:
    from selenium import webdriver
    from selenium.webdriver.common.by import By
    try: from Joao_Paulo.main import linksVendaJP
    except: from main import linksVendaJP
    from time import sleep

    links = linksVendaJP(service)

    driver = webdriver.Chrome(options=options, service=service)

    #Área total (área da propriedade), área construída, dormitórios, suítes, banheiros, vagas garagem, bairro, endereço, valor
    infos = [[],[],[],[],[],[],[],[],[]]

    infos_sub_primary = [["quartos", "suites", "banheiros", "garagens", "área propriedade", "área construida"],
                         [2,3,4,5,0,1]]
    
    for link in links:
        driver.get(link)
        print(f"{links.index(link)+1}/{len(links)}", link)
        sleep(1.5)

        #Cômodos:
        div_master_rooms = driver.find_elements(By.CLASS_NAME, "MuiStack-root.css-u46kmv")[0]

        for div_rooms in div_master_rooms.find_elements(By.TAG_NAME, "div"):
            try: index = infos_sub_primary[1][infos_sub_primary[0].index(div_rooms.text.split(":")[0].lower().strip())]
            except: continue
            
            room_text = int(div_rooms.text.split(":")[1].strip())

            if room_text == 0: room_text = ""
            infos[index].append(room_text)

        #Áreas:
        for p_area in driver.find_elements(By.CLASS_NAME,"MuiBox-root.css-15ea5xd")[0].find_elements(By.TAG_NAME, "p"):
            try: index = infos_sub_primary[1][infos_sub_primary[0].index(p_area.text.split(":")[0].lower().strip())]
            except: pass

            area_text = p_area.text.split(":")[1].replace(".","").replace(",",".").replace("m²","").strip()

            try: 
                area_text = float(area_text)
                if area_text == int(area_text): area_text = int(area_text)
                if area_text == 0: area_text = ""
            except: continue

            infos[index].append(area_text)

        #Bairro e endereço:
        head_infos = driver.find_elements(By.CLASS_NAME, "MuiStack-root.css-fq5082")[0]

        for p_address in head_infos.find_elements(By.CLASS_NAME, "MuiTypography-root.MuiTypography-body1.css-1a04ivi"):
            if p_address.text.lower().find("vilhena") == -1: continue

            infos[7].append(p_address.text)

            for index_neigh, p_neigh in enumerate(p_address.text.lower().split(",")):
                if p_neigh.find("vilhena - ro") != -1: infos[6].append(p_address.text.split(",")[index_neigh-1].strip())

        #Valor
        for value_h4 in driver.find_elements(By.CLASS_NAME, "MuiTypography-root.MuiTypography-h4.css-f4uu5s"):
            if value_h4.text.find("R$") == -1: continue

            infos[8].append(float(value_h4.text.replace(".","").replace(",",".").replace("m²","").replace("R$","").strip()))

        #Adiciona None nos campos sem informação:
        for info in infos:
            if len(info) < links.index(link) + 1: info.append("None")

    driver.quit()
    return infos