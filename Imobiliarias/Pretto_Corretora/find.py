def findVendaPC(service, options) -> list:
    from selenium import webdriver
    from selenium.webdriver.common.by import By
    try: from Pretto_Corretora.main import linksVendaPC
    except: from main import linksVendaPC

    links = linksVendaPC(service, options)
    
    driver = webdriver.Chrome(options=options, service=service)

    #Área do terreno, área construída, dormitórios, suítes, banheiros, vagas garagem, código do imóvel, bairro, endereço, valor
    infos = [[],[],[],[],[],[],[],[],[],[]]

    infos_sub_area = [["terreno área total", "área construída"],
                      [0,1]]
    
    infos_sub_rooms = [["dormitório", "suíte", "banheiro", "garagem", "garagens"],
                      [2,3,4,5,5]]
    
    for link in links: 
        driver.get(link)
        print(f"{links.index(link)+1}/{len(links)}", link)

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
            elif divs_master_title == "Localização":
                div_location = divs_master

        #Cômodos:
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

        #Código do imóvel:
        imob_code = driver.find_elements(By.CLASS_NAME, "sc-1oe743k-10.SDrPm")[0].find_elements(By.TAG_NAME, "span")[0].text.lower()
        infos[6].append(imob_code.replace("ref.:","").strip())

        #Endereço:
        infos[8].append(div_location.find_elements(By.CLASS_NAME, "sc-sbjl5d-0.ceyUbb")[0].text)

        #Bairro:
        for index_neigh, neigh_text in enumerate(infos[8][-1].split(" - ")):
            if neigh_text.find("Vilhena/RO") != -1: 
                infos[7].append(infos[8][-1].split(" - ")[index_neigh - 1].strip())
                break
        
        #Valor:
        price_text = driver.find_elements(By.CLASS_NAME,"sc-1bci137-0.jHIKPo")[0].text
        infos[9].append(float(price_text.replace("R$","").replace(".","").replace(",",".").strip()))

        #Adiciona None nos campos sem informação:
        for info in infos:
            if len(info) < links.index(link) + 1: info.append("None")

    driver.quit()
    return infos