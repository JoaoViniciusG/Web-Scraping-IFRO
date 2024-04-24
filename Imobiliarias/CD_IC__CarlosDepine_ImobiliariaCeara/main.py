def linksVendaCD_IC(service, options) -> list:
    from selenium import webdriver
    from selenium.webdriver.common.by import By
    from time import sleep

    links = []
    links_imob = ["https://carlosdepine.com/imoveis/Tipo-de-negocio/Tipo-de-imovel/Vilhena/Bairro/Minimo/Maximo/Codigo/Quartos-Garagem",
                  "https://imobiliariaceara.com.br/imoveis/Tipo-de-negocio/Tipo-de-imovel/Vilhena/Bairro/Minimo/Maximo/Codigo/Quartos-Garagem"]

    driver = webdriver.Chrome(options=options, service=service)

    for link in links_imob:
        driver.get(link)
        while True:
            for element_div in driver.find_elements(By. CLASS_NAME, "property2.property-list"):
                #Remove imóveis rurais e lançamentos de bairros/condomínios:
                if element_div.find_element(By.CLASS_NAME, "property-location").text.lower().find("rural") != -1: continue

                element_title = element_div.find_element(By.CLASS_NAME, "property-type").text.lower()

                for word in ("fazenda", "chacara", "chácara", "sitio", "sítio", "lançamento", "lancamento"):
                    if element_title.find(word) != -1: 
                        break
                else:
                    links.append(element_div.find_element(By. TAG_NAME, "a").get_attribute("href"))

            if driver.find_element(By. ID, 'proximo').get_attribute("class") != "btn btn-block btn-theme next": break
            driver.find_element(By. ID, 'proximo').click()
            sleep(1)

    driver.quit()
    return links