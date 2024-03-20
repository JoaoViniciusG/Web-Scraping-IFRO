def linksVendaWE(service, options) -> list:
    from selenium import webdriver
    from selenium.webdriver.common.by import By
    from time import sleep

    links = []

    driver = webdriver.Chrome(options=options, service=service)
    driver.get('https://wenderimoveis.com.br/properties/')

    current_page = 1

    while True:
        for index_ad, div_ad in enumerate(driver.find_elements(By.CLASS_NAME, "mg-bottom-30.ere-item-wrap")):
            #Retira os imóveis não pertencentes ao municício de Vilhena:
            try: 
                if div_ad.find_elements(By.CLASS_NAME, "property-location")[0].text.lower().find("vilhena") == -1: continue
            except: continue

            #Retira os imóveis rurais:
            if div_ad.find_elements(By.CLASS_NAME, "property-element-inline")[0].text.lower() in ("fazendas", "chácaras", "sítios"): continue

            #Retira os imóveis já vendidos:
            get_src_script = f"element = document.evaluate('/html/body/div[1]/div/div/div[1]/div/div/div/div[2]/div[{index_ad + 1}]/div/div[1]/noscript/text()', document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue;if (element) {"return element.nodeValue;"}"
            if driver.execute_script(get_src_script).split("src=")[1].split('"')[1] == "https://wenderimoveis.com.br/wp-content/uploads/2022/12/VENDIDO-1024x1024.jpg":
                continue

            links.append(div_ad.find_elements(By.CLASS_NAME, "property-link")[0].get_attribute("href"))
    
        next_button = driver.find_elements(By.CLASS_NAME, "paging-navigation.clearfix")[0].find_elements(By.TAG_NAME, "a")[-1]
        if next_button.get_attribute("class") != "next page-numbers": break
        next_button.click()

        while True:
            try:
                if int(driver.current_url.split("/")[-2]) == current_page + 1:
                    current_page += 1
                    sleep(0.5)
                    break
            except: pass
            sleep(0.5)

    driver.quit()
    return links