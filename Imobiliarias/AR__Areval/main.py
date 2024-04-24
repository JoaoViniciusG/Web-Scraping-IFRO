def linksVendaAR(service, options) -> list:
    from selenium import webdriver
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC 

    #Links, Tipo do Imóvel, Tipo de Negócio 
    links_infos = [[],[],[]]

    links_imob = [["https://www.arevalimoveis.com.br/imoveis/a-venda/vilhena",
                  "https://www.arevalimoveis.com.br/imoveis/para-alugar/vilhena"],

                  ["VE", "LO"]]

    driver = webdriver.Chrome(options=options, service=service)

    for index_link, link in enumerate(links_imob[0]):
        driver.get(link)

        while True:
            try: WebDriverWait(driver, timeout = 3).until(EC.element_to_be_clickable((By.CLASS_NAME, "btn.btn-md.btn-primary.btn-next")))
            except: break

            driver.execute_script("document.getElementsByClassName('btn btn-md btn-primary btn-next')[0].click()")

        links_loc = driver.find_elements(By. CLASS_NAME, "card_split_vertically.borderHover")
        
        for element in links_loc:
            #Remove imóveis rurais e os lançamentos de bairros/condomínios:
            imob_type = element.find_elements(By.CLASS_NAME, "card_split_vertically__code")[0].text[:2]
            if imob_type not in ("CA", "SO", "PT", "TE", "BA"): continue
            
            #Preenche o campo "Links":
            links_infos[0].append(element.get_attribute("href"))
            
            #Preenche o campo "Tipo do Imóvel":
            links_infos[1].append(imob_type)
            
            #Preenche o campo "Tipo de Negócio":
            links_infos[2].append(links_imob[1][index_link])


    driver.quit()
    return links_infos