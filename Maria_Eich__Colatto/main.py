def linksVendaME_CC(service, options) -> list:
    from selenium import webdriver
    from selenium.webdriver.common.by import By
    from math import ceil

    links = []
    num_page = 1

    driver = webdriver.Chrome(options=options, service=service)

    imob = ["https://www.colattocorretordeimoveis.com.br",
            "https://www.mariaeichimoveis.com.br"]
    
    for link_imob in imob:
        driver.get(f"{link_imob}/imoveis/ro/ro/vilhena/ordem-valor/resultado-crescente/quantidade-48/pagina-1/")
        print(link_imob)

        while True:
            for div_res in driver.find_elements(By. CLASS_NAME, "resultado"):
                #Remove os imóveis rurais:
                if div_res.find_elements(By.CLASS_NAME, "bairro")[0].text.lower().find(" rural ") != -1: continue
                links.append(div_res.find_elements(By. TAG_NAME, "a")[0].get_attribute("href"))

            if num_page >= ceil(int(driver.find_element(By. XPATH, '//*[@id="conteudo_imoveis"]/div[2]/span[2]').text.split(" ")[0][1:])/48): break
            num_page += 1
            driver.get(f"{link_imob}/imoveis/ro/ro/vilhena/ordem-valor/resultado-crescente/quantidade-12/pagina-{num_page}/")

    driver.quit()
    return links