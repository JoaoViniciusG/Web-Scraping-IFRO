def linksVendaGA_PD(service, options) -> list:
    from selenium import webdriver
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC 
    from selenium.webdriver.common.by import By
    from time import sleep

    links = []

    driver = webdriver.Chrome(service=service, options=options)
    
    imob = [["https://www.imobiliariapadraoro.com.br/buscar?order=most_relevant&direction=desc&availability=buy&city=Vilhena",
             "https://www.imobiliariapadraoro.com.br/buscar?order=most_relevant&direction=desc&availability=rent&city=Vilhena",
             "https://www.gamavilhena.com.br/buscar?order=highest_value&direction=desc&availability=buy&city=Vilhena",
             "https://www.gamavilhena.com.br/buscar?order=highest_value&direction=desc&availability=rent&city=Vilhena"],
            ["a", "a", "button", "button"]]

    for index, link_imob in enumerate(imob[0]):
        driver.get(link_imob)
        print(link_imob)

        first_load = True

        while True:
            if first_load == True: sleep(2); driver.find_element(By. XPATH, f'//*[@id="search"]/section[2]/imobzi-property-list/imobzi-pagination/section/h3[1]').click(); first_load = False
            WebDriverWait(driver, 20).until(EC.presence_of_element_located((By. XPATH, '//*[@id="search"]/section[2]/imobzi-property-list/section/mat-card[1]/mat-card-content/div/button')))

            for ad_card in driver.find_elements(By. CLASS_NAME, "swiper-wrapper"):
                links.append(ad_card.get_attribute("href"))

            for ad_card in driver.find_elements(By. CLASS_NAME, "property-gallery.info-gallery.ng-star-inserted"):
                links.append(ad_card.get_attribute("href"))

            script = f"document.evaluate(\
                        '/html/body/imobzi-root/mat-sidenav-container/mat-sidenav-content/imobzi-search/section/section[2]/imobzi-property-list/imobzi-pagination/section/{imob[1][index]}[2]',\
                        document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue.click()"
            
            if driver.find_element(By. XPATH, f'//*[@id="search"]/section[2]/imobzi-property-list/imobzi-pagination/section/{imob[1][index]}[2]').get_attribute("class").find("disabled") == -1: driver.execute_script(script=script)
            else: break

    driver.quit()
    return list(links)