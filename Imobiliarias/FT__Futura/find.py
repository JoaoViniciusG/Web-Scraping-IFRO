def findVendaFT(service, options) -> list:
    from selenium import webdriver
    from selenium.webdriver.common.by import By
    try: from FT__Futura.main import linksVendaFT
    except: from main import linksVendaFT

    links = linksVendaFT(service, options)

    driver = webdriver.Chrome(options=options, service=service)
    
    #Área total, área do terreno, área construída, área útil, dormitórios, suítes, banheiros, vagas garagem, descrição,
    #código do imóvel, endereço, valor
    infos = [[],[],[],[],[],[],[],[],[],[],[],[]]

    infos_sub_primary = [["total", "terreno", "construída", "útil", "dormitório", "suíte", "banheiro", "vaga"],[0,1,2,3,4,5,6,7]]

    for link in links:
        driver.get(link)
        print(f"{links.index(link)+1}/{len(links)}", link)

        div_master = driver.find_elements(By. CLASS_NAME, 'infos_imovel')[0]

        for div_info in div_master.find_elements(By. CLASS_NAME, "detalhes")[0].find_elements(By. TAG_NAME, "div"):
            info_text = div_info.find_elements(By. TAG_NAME, "span")[-1].text.split(" ")[-1].strip()
            if info_text[-1] == "s": info_text = info_text[:-1]
            try: index = infos_sub_primary[1][infos_sub_primary[0].index(info_text)]
            except: continue

            infos[index].append(div_info.find_elements(By. TAG_NAME, "span")[0].text.replace("m²","").replace(".","").replace(",",".").replace("sendo","").strip().split(" ")[0])

        #Descrição:
        try: 
            desc_text = driver.find_element(By. XPATH, '//*[@id="ctrl_sticky"]/div/div[1]/div[3]/div').text
            if desc_text != "": infos[8].append(desc_text)
        except: pass

        #Código do imóvel:
        try: infos[9].append(driver.find_element(By. XPATH, '//*[@id="ctrl_sticky"]/div/div[1]/div[1]/div[1]/span').text)
        except: pass

        #Endereço:
        try: infos[10].append(driver.find_element(By. XPATH, '//*[@id="ctrl_sticky"]/div/div[1]/div[1]/h2').text)
        except: pass

        #Valor:
        try: infos[11].append(float(driver.find_element(By. XPATH, '//*[@id="ctrl_sticky"]/div/div[1]/div[1]/div[3]/div[1]/div/h4').text.replace("R$","").replace(".","").replace(",",".").strip()))
        except: pass

        #Adiciona None nos campos sem informações:
        for info_verify in infos:
            if len(info_verify) < links.index(link) + 1: info_verify.append("None")

    return infos