def linksVendaGA_PD(service, options) -> list:
    from selenium import webdriver
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC 
    from selenium.webdriver.common.by import By

    links = set()

    driver = webdriver.Chrome(service=service, options=options)
    
    links_imob = ["https://www.gamavilhena.com.br/buscar?order=highest_value&direction=desc&availability=buy&city=Vilhena",
                  "https://www.imobiliariapadraoro.com.br/buscar?order=most_relevant&direction=desc&availability=buy&city=Vilhena"]

    for link_imob in list(links_imob[0]):
        driver.get(link_imob)
        while True:
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By. XPATH, '//*[@id="search"]/section[2]/imobzi-property-list/section/mat-card[1]/mat-card-content/div/button')))

            for ad_card in driver.find_elements(By. CLASS_NAME, "swiper-wrapper"):
                links.add(ad_card.get_attribute("href"))

            for ad_card in driver.find_elements(By. CLASS_NAME, "property-gallery.info-gallery.ng-star-inserted"):
                links.add(ad_card.get_attribute("href"))

            script = "document.evaluate(\
                        '/html/body/imobzi-root/mat-sidenav-container/mat-sidenav-content/imobzi-search/section/section[2]/imobzi-property-list/imobzi-pagination/section/button[2]',\
                        document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue.click()"
            
            if driver.find_element(By. XPATH, '//*[@id="search"]/section[2]/imobzi-property-list/imobzi-pagination/section/button[2]').is_enabled(): driver.execute_script(script=script)
            else: break
        driver.quit()
 
    return links