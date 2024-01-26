def linksVendaDR(service, options) -> list:
    from selenium import webdriver
    from selenium.webdriver.common.by import By

    links = []

    driver = webdriver.Chrome(options=options, service=service)
    driver.get("http://www.deiroescritorioimobiliario.com.br/imovel/?finalidade=venda&cidade=Vilhena")

    while True:
        for div_a in driver.find_elements(By. CLASS_NAME, "imoveis_listar"):
            links.append(div_a.find_elements(By. TAG_NAME, "a")[0].get_attribute("href"))

        next_button = driver.find_element(By. XPATH, '//*[@id="conteudo_bg1"]/table[2]/tbody/tr/td[1]/table[2]/tbody/tr/td/div[10]').find_elements(By. TAG_NAME, "a")[-1]
        if next_button.get_attribute("title") != "Próxima Página":
            break
        next_button.click()

    return links