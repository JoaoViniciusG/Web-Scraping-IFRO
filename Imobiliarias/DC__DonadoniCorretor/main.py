def linksVendaDC(service, options) -> list:
    from selenium import webdriver
    from selenium.webdriver.common.by import By

    links = []

    driver = webdriver.Chrome(options=options, service=service)
    driver.get('http://donadoniarqcorretor.com.br/imovel/?&tipo=&cid=Vilhena&bairro=0&sui=&ban=&gar=&dor=&pag=')

    while True:
        for div_ad in driver.find_elements(By.CLASS_NAME, "item-lista"):
            #Coleta apenas o URL de imóveis em área urbana:
            tag_a = div_ad.find_elements(By.TAG_NAME, "a")[0]
            if tag_a.get_attribute("title").lower().find("rural") == -1: links.append(tag_a.get_attribute("href"))

        next_button =  driver.find_elements(By.CLASS_NAME, "lista_imoveis_paginacao")[0].find_elements(By.TAG_NAME, "a")[-1]

        if next_button.get_attribute("title") != "Próxima Página": break
        next_button.click()

    driver.quit()
    return links