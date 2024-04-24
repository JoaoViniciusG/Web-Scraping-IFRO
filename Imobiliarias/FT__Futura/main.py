def linksVendaFT(service, options) -> list:
    from selenium import webdriver
    from selenium.webdriver.common.by import By
    from math import ceil

    #Links, Tipo do Imóvel, Tipo de Negócio, Valor
    links_infos = [[],[],[],[]]
    num_page = 1

    driver = webdriver.Chrome(options=options, service=service)
    driver.get("https://www.futura-vilhena.com/imoveis/ro/ordem-valor/resultado-crescente/quantidade-48/pagina-1/")

    types_of_add = [["apartamento", "barracao", "galpao", "casa", "residencial e comercial", "sobrado", "terreno", "predio", "sala comercial", "ponto comercial", "sala"],
                   ["AP", "BA", "BA", "CA", "CA", "SO", "TE", "PR", "SA", "PT", "SA"]]
    
    while True:
        for tag_a in driver.find_elements(By. CLASS_NAME, "resultado.resultado_lista"):
            #Remove imóveis rurais:
            ad_type = tag_a.find_element(By.CLASS_NAME, "dados").find_element(By.CLASS_NAME, "tipo").text.lower()

            for word in ("fazenda", "chacara", "sitio", "chácara", "sítio"):
                if ad_type.find(word) != -1: break
            else:
                #Seleciona apenas os imóveis de Vilhena
                if tag_a.find_elements(By. CLASS_NAME, "localizacao")[0].text.lower().find("vilhena") != -1:

                    #Remove os imóveis sem tipo de negócio e valor:
                    if tag_a.find_element(By.CLASS_NAME, "alinha_valores").text.find("consulta") != -1: continue

                    #Identifica o tipo do imóvel":
                    ad_type_ref = tag_a.find_element(By.CLASS_NAME, "referencia").text[:2]

                    try:
                        types_of_add[1].index(ad_type_ref)

                    except:
                        for index_type, type_add_verify in enumerate(types_of_add[0]):
                            if ad_type.find(type_add_verify) != -1: 
                                ad_type_ref = types_of_add[1][index_type]
                                break
                        else: 
                            continue

                    #Preenche os campos necessários:
                    negcs_types_values = tag_a.find_element(By.CLASS_NAME, "alinha_valores").find_elements(By.CLASS_NAME, "valor")

                    for negc_type in negcs_types_values:
                        value = float(negc_type.text.strip().split(" ")[-1].replace(".","").replace(",","."))
                        
                        #Preenche o campo "Tipo de Negócio"
                        if negc_type.text.lower().find("venda") != -1:
                            links_infos[2].append("VE")
                        elif negc_type.text.lower().find("locação") != -1:
                            links_infos[2].append("LO")
                        else:
                            break

                        #Preenche o campo "Link":
                        links_infos[0].append(tag_a.find_element(By. TAG_NAME, "a").get_attribute("href"))

                        #Preenche o campo "Tipo do Imóvel":
                        links_infos[1].append(ad_type_ref)

                        #Preenche o campo "Valor":
                        links_infos[3].append(value)

        if num_page >= ceil(int(driver.find_element(By. XPATH, "/html/body/div[9]/div[1]/div[2]/div[1]/h1/b").text)/48): break
        num_page += 1
        driver.get(f"https://www.futura-vilhena.com/imoveis/ro/ordem-valor/resultado-crescente/quantidade-48/pagina-{num_page}/")

    driver.quit()
    return links_infos