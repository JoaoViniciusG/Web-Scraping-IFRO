def linksVendaBC(service, options) -> list:
    from selenium import webdriver
    from selenium.webdriver.common.by import By
    from time import sleep

    driver = webdriver.Chrome(service=service, options=options)

    driver.get("https://balcaodealuguel.com.br/comprar-alugar/imoveis/vilhena-ro?typeArea=total_area&floorComparision=equals&sort=is_price_shown%2Ccalculated_price%2Cid&offset=1&limit=42")

    links = []

    while True:
        divs_ad = driver.find_elements(By.CLASS_NAME, "src__Box-sc-1sbtrzs-0.sc-j8ewmh-0.iCmbbj.CardProperty")

        for div in divs_ad:
            links.append(div.find_elements(By.TAG_NAME, "a")[0].get_attribute("href"))

        next_button = driver.find_element(By.XPATH, '//*[@id="__next"]/div[1]/div/main/div[2]/section/div/ul').find_elements(By.TAG_NAME, "li")[-1]

        if next_button.get_attribute("class").find("disabled") != -1: 
            break
        
        next_button.click()
        sleep(2)

    return links