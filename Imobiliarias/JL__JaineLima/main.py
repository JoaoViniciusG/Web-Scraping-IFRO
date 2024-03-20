def linksVendaJL(service, options) -> list:
    from selenium import webdriver
    from selenium.webdriver.common.by import By
    from time import sleep
    links = []

    driver = webdriver.Chrome(options=options, service=service)
    driver.get('https://jainelimacorretora.com.br/comprar-alugar/imoveis/vilhena-ro?sort=-created_at%2Cid&offset=1&limit=21&typeArea=total_area&floorComparision=equals')

    while True:
        for div_ad in driver.find_elements(By.CLASS_NAME, "src__Box-sc-1sbtrzs-0.sc-hlcmlc-0.jeFFeJ.CardProperty"):
            #Remove os imóveis rurais:
            if div_ad.find_elements(By.CLASS_NAME, "sc-hlcmlc-1.gQklzn")[0].text.lower().find("rural") != -1: continue

            links.append(("https://jainelimacorretora.com.br"+div_ad.get_attribute("href")))

        next_button = driver.find_elements(By.CLASS_NAME, "pagination")[0].find_elements(By.TAG_NAME, "li")[-1]

        if next_button.get_attribute("class").find("disabled") != -1: break
        next_button.click()
        sleep(1.5)

    driver.quit()
    return links