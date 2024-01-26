def linksVendaFT(service, options) -> list:
    from selenium import webdriver
    from selenium.webdriver.common.by import By
    from math import ceil

    links = []
    num_page = 1

    driver = webdriver.Chrome(options=options, service=service)
    driver.get("https://www.futura-vilhena.com/imoveis/ro/ordem-valor/resultado-crescente/quantidade-48/pagina-1/")

    while True:
        for tag_a in driver.find_elements(By. CLASS_NAME, "resultado.resultado_lista"):
            if tag_a.find_elements(By. CLASS_NAME, "localizacao")[0].text.lower().find("vilhena") != -1:
                links.append(tag_a.find_elements(By. TAG_NAME, "a")[0].get_attribute("href"))

        if num_page >= ceil(int(driver.find_element(By. XPATH, "/html/body/div[9]/div[1]/div[2]/div[1]/h1/b").text)/12): break
        num_page += 1
        driver.get(f"https://www.futura-vilhena.com/imoveis/ro/ordem-valor/resultado-crescente/quantidade-12/pagina-{num_page}/")

    driver.quit()
    return links