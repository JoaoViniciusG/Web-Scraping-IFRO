def linksVendaFB_CF_SR(service, options) -> list:
    from selenium import webdriver
    from selenium.webdriver.common.by import By
    from time import sleep

    links = []
    links_imob = ["http://www.fbcorretordeimoveis.com.br/imovel/?finalidade=&tipo=&cid=Vilhena&bairro=0&sui=&ban=&gar=&dor=&pag=1",
                  "https://www.caiofernandocorretor.com.br/imovel/?finalidade=&tipo=&cid=Vilhena&bairro=0&sui=&ban=&gar=&dor=&pag=1"]
                  #"http://www.samuelrichard.com.br/imovel/?finalidade=venda&tipo=&cid=Vilhena&bairro=0&sui=&ban=&gar=&dor=&pag=1"]

    driver = webdriver.Chrome(options=options, service=service)

    for link in links_imob:
        driver.get(link)

        while True:
            for div_a in driver.find_elements(By. CLASS_NAME, "imovelcard")[:-1]:
                links.append(div_a.find_elements(By. TAG_NAME, "a")[0].get_attribute("href"))
            

            next_button = driver.find_elements(By. CLASS_NAME, "lista_imoveis_paginacao")[0].find_elements(By. TAG_NAME, "a")[-1]
            if next_button.text != ">": break
            next_button.click()

    driver.quit()
    return links