def linksVendaCD_IC(service, options) -> list:
    from selenium import webdriver
    from selenium.webdriver.common.by import By
    from time import sleep

    links = []
    links_imob = ["https://carlosdepine.com/imoveis/Venda/Tipo-de-imovel/Cidade/Bairro/Minimo_Area-minima/Maximo_Area-maxima/Codigo/Quartos_Garagem_Banheiros",
                  "https://imobiliariaceara.com.br/imoveis/Venda/Tipo-de-imovel/Cidade/Bairro/Minimo_Area-minima/Maximo_Area-maxima/Codigo/Quartos_Garagem_Banheiros"]

    driver = webdriver.Chrome(options=options, service=service)

    for link in links_imob:
        driver.get(link)
        while True:
            for element_div in driver.find_elements(By. CLASS_NAME, "property-image"):
                #Remove imóveis rurais:
                if element_div.find_element(By.CLASS_NAME, "property-title").text.lower().find("rural") != -1: continue

                #Remove os lançmentos de bairros/condomínios:
                try:
                    if element_div.find_element(By.CLASS_NAME, "post-status").text.lower() == "lançamento": continue
                except: pass

                links.append(element_div.find_elements(By. TAG_NAME, "a")[0].get_attribute("href"))

            if driver.find_element(By. ID, 'proximo').get_attribute("class") != "btn btn-block btn-theme next": break
            driver.find_element(By. ID, 'proximo').click()
            sleep(1)

    driver.quit()
    return links