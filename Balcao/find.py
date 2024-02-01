def findVendaBC(service, options) -> list:
    from selenium import webdriver
    from selenium.webdriver.common.by import By
    try: from main import linksVendaBC
    except: from Balcao.main import linksVendaBC

    links = linksVendaBC(service, options)

    driver = webdriver.Chrome(service=service, options=options)

    #Área total, área construída, área privativa, dormitórios, suítes, banheiros, vagas garagem, bairro, endereço, código do imóvel, valor
    infos = [[],[],[],[],[],[],[],[],[],[],[]]

    infos_sub_primary = [["Terreno Área Total", "Área Construída", "Área Privativa", "Área Total", "dormitório", "suíte", "banheiro", "garage"],
                         [0, 1, 2, 0, 3, 4, 5, 6]]
    
    for link in links:
        driver.get(link)
        print(f"{links.index(link)+1}/{len(links)}", link)

        divs_list = driver.find_element(By.XPATH, '//*[@id="__next"]/div/div/main/div/div[1]/div[4]/div[2]').find_elements(By.TAG_NAME, "section")[-1].find_elements(By.TAG_NAME, "div")

        for div in divs_list:
            div_type = div.find_elements(By.TAG_NAME, "span")[0].text

            try: 
                index = infos_sub_primary[1][infos_sub_primary[0].index(div_type)]
            except:
                continue

            infos[index].append(div.find_elements(By.TAG_NAME, "span")[1].text.replace(".","").replace(",",".").replace("m²",""))

        try:
            for span in driver.find_element(By.XPATH, '//*[@id="__next"]/div/div/main/div/div[1]/div[4]/div[1]/section[1]/div').find_elements(By.TAG_NAME, "span"):
                for span_text in span.text.split(","):
                    span_text = span_text.lower().replace("sendo","").strip()

                    for index_sub, info_sub in enumerate(infos_sub_primary[0]):
                        if span_text.find(info_sub) > 0: index = infos_sub_primary[1][index_sub]
                        else: continue

                        infos[index].append(span_text.split(" ")[0])
                        break
        except: pass

        #Endereço:
        infos[8].append(driver.find_elements(By.CLASS_NAME, "sc-sbjl5d-0.ceyUbb")[0].text)

        #Bairro:
        neighborhood = infos[8][-1].split("-")

        for index, str_neigh in enumerate(neighborhood):
            if str_neigh.find("Vilhena/RO") == -1: continue

            infos[7].append(neighborhood[index - 1].strip())
            break

        #Código do imóvel:
        infos[9].append(link.split("/")[-1])

        #Valor:
        try: infos[10].append(float(driver.find_element(By.XPATH, '//*[@id="__next"]/div/div/main/div/div[1]/div[2]/div[1]/span').text.split("\n")[0].replace(".","").replace(",",".").replace("R$","")))
        except: pass

        #Adiciona None nos campos sem informações:
        for info in infos:
            if len(info) < links.index(link) + 1: info.append("None")

    driver.quit()
    return infos