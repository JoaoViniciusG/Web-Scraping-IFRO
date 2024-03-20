def findVendaJL(service, options) -> list:
    from selenium import webdriver
    from selenium.webdriver.common.by import By
    from selenium.webdriver.chrome.options import Options
    try: from JL__JaineLima.main import linksVendaJL
    except: from main import linksVendaJL

    links = linksVendaJL(service, options)
    
    options = Options()
    options.add_argument('log-level=3')
    options.add_argument('--blink-settings=imagesEnabled=false')

    driver = webdriver.Chrome(options=options, service=service)
    driver.maximize_window()

    #Área total, área construída, dormitórios, suítes, banheiros, vagas, bairro, código do imóvel, valor
    infos = [[],[],[],[],[],[],[],[],[]]

    infos_sub_h2 = [["cômodos", "áreas"],
                    ["infos_sub_rooms", "infos_sub_areas"]]
    
    infos_sub_rooms = [["dormitório", "suíte", "banheiro", "garage"],
                       [2,3,4,5], " ", -1]
    infos_sub_areas = [["terreno área total", "área cotruída"],
                       [0,1], ":", 0]

    for link in links:
        driver.get(link)
        print(f"{links.index(link)+1}/{len(links)}", link)

        for div_master_info in driver.find_elements(By.CLASS_NAME, "sc-duc0lc-0.iRRdZZ"):
            try: 
                div_master_title = div_master_info.find_elements(By.TAG_NAME, "h2")[0].text.lower()

                #Código do imóvel:
                if div_master_title == "outras informações":
                    for index_code, text_div_code in enumerate(div_master_info.text.split("\n")):
                        if text_div_code == "Referência:": 
                            infos[7].append(div_master_info.text.split("\n")[index_code+1]); break 
                        
                #Bairro:                
                elif div_master_title == "localização":
                    location_text = div_master_info.find_elements(By.TAG_NAME, "span")[0].text.split("-")
                    for index_neigh, text_span_neigh in enumerate(location_text):
                        if text_span_neigh.find("Vilhena/RO") != -1: infos[6].append(location_text[index_neigh - 1].strip())
            except: pass
            
            try: infos_sub = eval(infos_sub_h2[1][infos_sub_h2[0].index(div_master_title)])
            except: continue

            for div_info in div_master_info.find_elements(By.CLASS_NAME, "sc-kqaiuw-0"):
                for content_text in div_info.text.split(", sendo "):
                    title_text = content_text.split(infos_sub[2])[infos_sub[3]].lower().strip().replace("ns","")
                    if title_text[-1] == "s": title_text = title_text[:-1]

                    try: index = infos_sub[1][infos_sub[0].index(title_text)]
                    except: continue

                    result = content_text.split(infos_sub[2])[(-infos_sub[3]) - 1].replace(".","").replace(",",".").replace("m²","").strip()

                    try:
                        result = float(result)
                        if result == int(result): result = int(result)
                    except: pass

                    infos[index].append(result)
        
        #Valor:
        price_text = driver.find_elements(By.CLASS_NAME, 'sc-7gfa57-1.izkZFF')[0].text
        infos[8].append(float(price_text.replace("R$","").replace(".","").replace(",",".").strip()))

        #Adiciona None nos campos sem informação:
        for info in infos:
            if len(info) < links.index(link) + 1: info.append("None")

    driver.quit()
    return infos