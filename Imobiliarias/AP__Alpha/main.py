def linksVendaAP(service, options) -> list:
    from selenium import webdriver
    from selenium.webdriver.common.by import By

    links = []

    driver = webdriver.Chrome(options=options, service=service)
    current_page = 1

    while True:
        driver.get(f'https://www.alphavilhena.com.br/buscar/buscar?payload=&aca=&tip=&cid=&bai=&dor=&vag=&min=&max=&cod=&inf=&ord=&pag={current_page}')
        
        for div_ad in driver.find_elements(By. CLASS_NAME, "bloco.miniatura-imovel.iwidth-33-3"):
            #Remove imóveis já vendidos/alugados:
            desc_text_ad = div_ad.find_elements(By.CLASS_NAME, "miniatura-imovel-descricao")[0].text.lower()
            if  desc_text_ad.find("alugad") != -1 or desc_text_ad.find("vendid") != -1: continue

            #Remove imóveis rurais e os lançamentos de bairros/condomínios:
            type_text_ad = div_ad.find_elements(By.CLASS_NAME, "upper.strong")[0].text.lower().split("--")[0].strip()
            if type_text_ad in ("fazenda", "chácara", "sítio", "lançamento"): continue

            links.append(div_ad.find_elements(By. TAG_NAME, "a")[0].get_attribute("href"))
        
        if driver.find_element(By.ID, "paginacao_render").find_elements(By.TAG_NAME, "button")[-1].get_attribute("class").find("disabled") != -1: break
        current_page += 1 

    driver.quit()
    return links