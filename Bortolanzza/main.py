def linksVendaBZ(service, options) -> list:
    from selenium.webdriver.common.by import By 
    from selenium import webdriver

    links = []

    driver = webdriver.Chrome(options=options, service=service)
    driver.get("http://www.bortolanzza.com.br/imovel/?finalidade=venda&cidade=Vilhena")

    while True:
        for td in driver.find_elements(By. TAG_NAME, 'td'):
            if td.get_attribute("width") == "70%":
                links.append(td.find_elements(By. TAG_NAME, "a")[0].get_attribute("href"))

        next_button = driver.find_element(By. XPATH, '//*[@id="conteudo_bg1"]/table[1]/tbody/tr/td[1]/table[4]/tbody/tr/td').find_elements(By. TAG_NAME, "a")[-1]
        if next_button.get_attribute("title") != "Próxima Página":
            break
        next_button.click()

    driver.quit()
    return links