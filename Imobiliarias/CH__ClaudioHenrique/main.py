def linksVendaCH(service, options) -> list:
    from selenium import webdriver
    from selenium.webdriver.common.by import By

    links = []

    driver = webdriver.Chrome(options=options, service=service)
    driver.get('http://www.claudiohenriquecorretor.com.br/imovel/?finalidade=venda&tipo=&cid=Vilhena&bairro=0&sui=&ban=&gar=&dor=&pag=1')

    words_to_search = ["rural", "chácara", "sítio", "fazenda"]

    while True:
        for div_ad in driver.find_elements(By.CLASS_NAME, "imoveis_listar"):
            #Excluí imóveis já vendidos:
            if div_ad.find_elements(By.CLASS_NAME, "foto_tarja")[0].text.lower().find("vendid") != -1: continue

            #Excluí imóveis rurais:
            for word in words_to_search:
                if div_ad.find_elements(By.CLASS_NAME, "conteudo1")[0].text.lower().find(word) != -1: break
            else: links.append(div_ad.find_elements(By.TAG_NAME, "a")[0].get_attribute("href"))

        next_button = driver.find_elements(By.CLASS_NAME, "lista_imoveis_paginacao")[-1].find_elements(By.TAG_NAME, "a")[-1]

        if next_button.get_attribute("title") != "Próxima Página": break
        driver.get(f"http://www.claudiohenriquecorretor.com.br/imovel/?finalidade=venda&tipo=&cid=Vilhena&bairro=0&sui=&ban=&gar=&dor=&pag={int(driver.current_url[driver.current_url.find("pag=") + 4:]) + 1}")

    driver.quit()
    return links