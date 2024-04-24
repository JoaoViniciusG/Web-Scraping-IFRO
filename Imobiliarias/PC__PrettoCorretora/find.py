def findVendaPC(service, options) -> list:
    from selenium import webdriver
    from selenium.webdriver.common.by import By
    try: from Imobiliarias.PC__PrettoCorretora.main import linksVendaPC
    except: from main import linksVendaPC

    links_infos = linksVendaPC(service, options)
    
    driver = webdriver.Chrome(options=options, service=service)

    #(0) Url, (1) área total, (2) área construída, (3) dormitórios, (4) suítes, (5) banheiros, (6) vagas garagem, (7) bairro, (8) valor, (9) tipo de imóvel, (10) tipo de negócio, (11) descrição
    infos = [[],[],[],[],[],[],[],[],[],[],[],[]]

    infos_sub_area = [["terreno área total", "área total", "área construída"],
                      [1,1,2]]
    
    infos_sub_rooms = [["dormitório", "suíte", "banheiro", "garagem", "garagens"],
                      [3,4,5,6,6]]
    
    #Preenche os campos "(0) Url", "(10) tipo de imóvel" e "(11) tipo de negócio":
    infos[0] = links_infos[0]
    infos[7] = links_infos[3]
    infos[9] = links_infos[1]
    infos[10] = links_infos[2]

    for link in links_infos[0]: 
        driver.get(link)
        print(f"{links_infos[0].index(link)+1}/{len(links_infos[0])}", link)

        #Áreas
        for div_info_area in driver.find_elements(By.CLASS_NAME, "sc-p64o06-0.hcAPwC.Line"):
            text_area_title = div_info_area.find_elements(By.CLASS_NAME, "Line_title")[0].text.lower()

            try: index = infos_sub_area[1][infos_sub_area[0].index(text_area_title)]
            except: continue

            result_area = float((div_info_area.find_elements(By.CLASS_NAME, "Line_value")[0].text.replace("m²","").replace(".","").replace(",",".").strip()))

            if result_area == int(result_area): result_area = result_area

            infos[index].append(result_area)

        #Identifica as divs dos cômodos e da localização:
        for divs_master in driver.find_elements(By.CLASS_NAME, "sc-1n21tt0-0.jzgiUr"):
            divs_master_title = divs_master.find_elements(By.TAG_NAME, "h3")[0].text
            if  divs_master_title == "Cômodos":
                divs_rooms = divs_master.find_elements(By.CLASS_NAME, "sc-k214w6-0.ilrYr")
            elif divs_master_title == "Descrição do imóvel":
                div_description = divs_master

        #Cômodos:
        try:
            for div_info_rooms in divs_rooms:
                text_room = div_info_rooms.text.lower()

                if text_room.find(",") != -1: text_room = text_room.replace(" sendo ", "").split(",")
                else: text_room = [text_room]

                for text_info_room in text_room:
                    title_info_room = text_info_room.split(" ")[-1].strip()
                    if title_info_room[-1] == "s": title_info_room = title_info_room[:-1]

                    try: index = infos_sub_rooms[1][infos_sub_rooms[0].index(title_info_room)]
                    except: continue

                    result_room = int(text_info_room.split(" ")[0])

                    infos[index].append(result_room)
        except: pass

        #Valor:
        price_text = driver.find_elements(By.CLASS_NAME,"sc-1bci137-0.jHIKPo")[0].text
        infos[8].append(float(price_text.replace("R$","").replace(".","").replace(",",".").strip()))

        #Descrição:
        try:
            infos[11].append(div_description.find_element(By.TAG_NAME, "span").text)
        except: pass

        #Adiciona None nos campos sem informação:
        for info in infos:
            if len(info) < links_infos[0].index(link) + 1: info.append("None")

    driver.quit()
    return infos