def linksVendaGA_PD(service, options) -> list:
    from selenium import webdriver
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC 
    from selenium.webdriver.common.by import By
    from time import sleep
    from math import ceil

    #Links, Tipo do Imóvel, Tipo de Negócio:
    links_infos = [[],[],[]]

    driver = webdriver.Chrome(service=service, options=options)
    
    imob = [["https://www.imobiliariapadraoro.com.br/buscar?order=most_relevant&direction=desc&availability=buy&city=Vilhena",
             "https://www.imobiliariapadraoro.com.br/buscar?order=most_relevant&direction=desc&availability=rent&city=Vilhena",
             "https://www.gamavilhena.com.br/buscar?order=highest_value&direction=desc&availability=buy&city=Vilhena",
             "https://www.gamavilhena.com.br/buscar?order=highest_value&direction=desc&availability=rent&city=Vilhena"],
            ["VE","LO","VE","LO"]]
    
    types_of_add = [["apartamento", "barracao", "barracão", "galpão", "galpao", "sobrado", "prédio", "casa", "residencial e comercial", "terreno", "predio", "sala comercial", "ponto comercial", "sala", "garagem", "salão"],
                   ["AP", "BA", "BA", "BA", "BA", "SO", "PR", "CA", "CA", "TE", "PR", "SA", "PT", "SA", "GA", "SA"]]

    for index_link, link_imob in enumerate(imob[0]):
        current_page = 1
        total_pages = 0

        first_load = True


        while True:
            driver.get(link_imob+f"&page={current_page}")

            '''sleep(2)
            try:
                driver.find_element(By. XPATH, f'//*[@id="search"]/section[2]/imobzi-property-list/imobzi-pagination/section/h3[1]').click()
            except: print("Não foi"); pass'''

            WebDriverWait(driver, 20).until(EC.presence_of_element_located((By. XPATH, '//*[@id="search"]/section[2]/imobzi-property-list/section/mat-card[1]/mat-card-content/div/button')))

            if first_load == True:
                num_ads = int(driver.find_element(By.TAG_NAME, "imobzi-header-property-list").text.strip().split(" ")[0])

                total_pages = ceil(num_ads/15)
                first_load = False

            for ad_card in driver.find_elements(By.CLASS_NAME, "mat-card.mat-focus-indicator.ng-star-inserted"):
                ad_type = ad_card.find_element(By.CLASS_NAME, "mat-card-title.h3.color-title.bold.ng-star-inserted").text.lower()

                #Remove os anúncios rurais:
                for word in ("fazenda", "chácara", "chacara", "sítio", "sitio"):
                    if ad_type.find(word) != -1: break
                
                else:
                    try:
                        current_link = ad_card.find_element(By.CLASS_NAME, "swiper-wrapper").get_attribute("href")
                    except:
                        current_link = ad_card.find_element(By.CLASS_NAME, "mat-card-header").find_element(By.TAG_NAME, "a").get_attribute("href")

                    try:
                        links_infos[0].index(current_link)
                        continue
                    except: pass
                    
                    #Preenche o campo "Tipo do Imóvel":
                    for index_type, type_add_verify in enumerate(types_of_add[0]):
                        if ad_type.find(type_add_verify) != -1: 
                            links_infos[1].append(types_of_add[1][index_type])
                            break
                    else: 
                        links_infos[1].append("None")
                        pass
                    
                    #Preenche o campo "Links":
                    links_infos[0].append(current_link)

                    #Preenche o campo "Tipo de Negócio":
                    links_infos[2].append(imob[1][index_link])

            if current_page == total_pages: break
            else: current_page += 1

    driver.quit()
    return links_infos