def linksVendaPC(service, options) -> list:
    from selenium import webdriver
    from selenium.webdriver.common.by import By

    links = []

    driver = webdriver.Chrome(options=options, service=service)
    driver.get('https://prettocorretoradeimoveis.com.br/comprar-alugar/imoveis/vilhena-ro?sort=is_price_shown%2Ccalculated_price%2Cid&offset=1&limit=21&typeArea=total_area&floorComparision=equals')

    for div_id in driver.find_elements(By.CLASS_NAME, "src__Box-sc-1sbtrzs-0.sc-hlcmlc-0.jeFFeJ.CardProperty"):
        links.append("https://prettocorretoradeimoveis.com.br"+div_id.get_attribute("href"))

    driver.quit()
    return links