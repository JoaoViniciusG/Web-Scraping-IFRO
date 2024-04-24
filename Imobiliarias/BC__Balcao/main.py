def linksVendaBC(service, options) -> list:
    from selenium import webdriver
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC 
    from time import sleep

    #Links, Tipo do Imóvel, Tipo de Negócio 
    links_infos = [[],[],[]]

    links_imob = [["https://balcaodealuguel.com.br/comprar/imoveis/vilhena-ro?typeArea=total_area&floorComparision=equals&sort=is_price_shown%2Ccalculated_price%2Cid&offset=1&limit=42",
                  "https://balcaodealuguel.com.br/alugar/imoveis/vilhena-ro?typeArea=total_area&floorComparision=equals&sort=is_price_shown%2Ccalculated_price%2Cid&offset=1&limit=42"],

                  ["VE", "LO"]]
    
    types_of_add = [["apartamento", "galpão", "casa", "terreno", "prédio", "sala comercial", "salão comercial"],
                   ["AP", "BA", "CA", "TE", "PR", "SA", "SA"]]

    driver = webdriver.Chrome(options=options, service=service)

    for index_link, link in enumerate(links_imob[0]):
        driver.get(link)
        
        count_timeOut = 0

        while True:
            try:
                div_master = driver.find_element(By.CLASS_NAME, "src__Box-sc-1sbtrzs-0.src__Flex-sc-1sbtrzs-1.sc-1rvsmwh-0.jCiDUz")
            except:
                count_timeOut += 1
                continue

            if len(div_master.find_elements(By.TAG_NAME, "div")) > 1:
                break
            
            if count_timeOut == 20: raise Exception("Time Out Exception")

            count_timeOut += 1
            sleep(0.5)


        while True:
            divs_ad = driver.find_elements(By.CLASS_NAME, "src__Box-sc-1sbtrzs-0.sc-j8ewmh-0.iCmbbj.CardProperty")

            for div in divs_ad:
                #Preenche o campo "Tipo de Imóvel"
                add_type = div.find_element(By.CLASS_NAME, "sc-j8ewmh-6.EKGmN").text.lower()

                for index_type, type_add_verify in enumerate(types_of_add[0]):
                    if add_type.find(type_add_verify) != -1: 
                        links_infos[1].append(types_of_add[1][index_type])
                        break
                else:
                    #Remove os imóveis sem tipo declarado:
                    continue

                #Preenche o campo "Tipo de Negócio":
                links_infos[2].append(links_imob[1][index_link])

                #Preenche o campo "Links":
                links_infos[0].append(div.find_elements(By.TAG_NAME, "a")[0].get_attribute("href"))

            try:
                next_button = driver.find_element(By.XPATH, '//*[@id="__next"]/div[1]/div/main/div[2]/section/div/ul').find_elements(By.TAG_NAME, "li")[-1]
            except: break

            if next_button.get_attribute("class").find("disabled") != -1: 
                break
            
            next_button.click()
            sleep(2)

    driver.quit()
    return links_infos