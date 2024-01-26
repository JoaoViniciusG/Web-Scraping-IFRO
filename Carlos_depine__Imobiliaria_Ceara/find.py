def findVendaCD_IC(service, options) -> list:
    from selenium import webdriver
    from selenium.webdriver.common.by import By
    try: from main import linksVendaCD_IC
    except: from Carlos_depine__Imobiliaria_Ceara.main import linksVendaCD_IC
    from time import time

    time_start = time()

    links = linksVendaCD_IC(service, options)

    driver = webdriver.Chrome(options=options, service=service)

    #Área útil, área do terreno, área total, dormitórios, suítes, banheiros, vagas garagem, descrição, 
    #proximidades, código do imóvel, localização, valor
    infos = [[],[],[],[],[],[],[],[],[],[],[],[]]

    infos_sub_primary = [["Área Útil", "Área Terreno", "Área Total", "Dormitórios", "Suítes", "Banheiros", "Box (N˚ Garagem)", "Venda"],[0,1,2,3,4,5,6,11]]
    for link in links:
        driver.get(link)
        print(link)

        for info_primary in driver.find_elements(By. CLASS_NAME, "col-xs-12.col-sm-6"):
            try: index = infos_sub_primary[1][infos_sub_primary[0].index(info_primary.find_elements(By. TAG_NAME, "span")[0].text)]
            except: continue

            infos[index].append(info_primary.find_elements(By. CLASS_NAME, "pull-right")[0].text.replace("R$ ","").split(" ")[0].replace(".","").replace(",","."))

        #Descrição:
        try:
            desc_text = driver.find_element(By. XPATH, "/html/body/div/main/div/div/div/div/div[4]/div[5]/p").text
            if  desc_text == "": raise

            infos[7].append(desc_text)
        except: 
            try: 
                desc_text = ""
                for div_desc in driver.find_element(By. XPATH, "/html/body/div/main/div/div/div/div/div[4]/div[5]").find_elements(By. TAG_NAME, "div"):
                    if div_desc.get_attribute("class") != "": break
                    if div_desc.text == "": continue
                    desc_text += div_desc.text + "\n"
                infos[7].append(desc_text[:-1])
            
            except: pass

        #Proximidades:
        prox_text = ""
        try:
            for i in driver.find_element(By. XPATH, "/html/body/div/main/div/div/div/div/div[4]/div[9]/ul").find_elements(By. TAG_NAME, "li"):
                prox_text += i.text + "\n"
            infos[8].append(prox_text[:-1])
        except: pass

        #Código do imóvel:
        try: infos[9].append(driver.find_element(By. XPATH, "/html/body/div/main/div/div/div/div/div[2]").text.split("Cod.")[-1].strip())
        except: pass

        #Localização:
        try: infos[10].append(driver.find_elements(By. CLASS_NAME, "address.text-center")[0].text)
        except: pass

        #Adiciona None nos campos sem informações:
        for info_verify in infos:
            if len(info_verify) < links.index(link) + 1: info_verify.append("None")

    time_final = time()
    print(f"{time_final - time_start} segundos")
    return infos