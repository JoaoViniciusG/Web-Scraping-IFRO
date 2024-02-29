def linksVendaRM(service, options) -> list:
    from selenium import webdriver
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC 
    from time import sleep

    links = []

    driver = webdriver.Chrome(options=options, service=service)
    driver.get('https://www.remax.com.br/PublicListingList.aspx?SelectedCountryID=55&CityID=6581546')

    while True:
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'hiddenRTL')))
    
        for div_ad in driver.find_elements(By.CLASS_NAME, "gallery-item-container"):
            #Remove os imóveis já vendidos
            try:
                if div_ad.find_elements(By.CLASS_NAME, "exclusive-banner.drop-shadow")[0].text.lower() in ("vendido", "alugado"): continue
            except: pass

            #Remove os imóveis rurais:
            ad_type = div_ad.find_elements(By.CLASS_NAME, "gallery-transtype")[0].text.lower()

            for word in ("chácara","sítio","fazenda"):
                if ad_type.find(word) != -1: break
            else: links.append(div_ad.find_elements(By.CLASS_NAME, "LinkImage")[0].get_attribute("href"))

        next_li = driver.find_elements(By.CLASS_NAME, "pagination")[0].find_elements(By.TAG_NAME, "li")[-1]
        
        try:
            next_a = next_li.find_elements(By.TAG_NAME, "a")[0]
            
            for info in driver.current_url.split("&"):
                if info.find("page=") != -1: current_page = int(info[5:])

            next_a.click()
        except: break

        while True:
            for info in driver.current_url.split("&"):
                if info.find("page=") != -1: page = int(info[5:])
            if page != current_page: break
            sleep(0.5)

    driver.quit()
    return links