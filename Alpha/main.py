def linksVendaAP(service, options) -> list:
    from selenium import webdriver
    from selenium.webdriver.common.by import By

    links = []

    driver = webdriver.Chrome(options=options, service=service)
    current_page = 1

    while True:
        driver.get(f'https://www.alphavilhena.com.br/buscar/buscar?payload=&aca=&tip=&cid=&bai=&dor=&vag=&min=&max=&cod=&inf=&ord=&pag={current_page}')
        
        for div_ad in driver.find_elements(By. CLASS_NAME, "bloco.miniatura-imovel.iwidth-33-3"):
            links.append(div_ad.find_elements(By. TAG_NAME, "a")[0].get_attribute("href"))
        
        if driver.find_element(By.ID, "paginacao_render").find_elements(By.TAG_NAME, "button")[-1].get_attribute("class").find("disabled") != -1: break
        current_page += 1 

    return links