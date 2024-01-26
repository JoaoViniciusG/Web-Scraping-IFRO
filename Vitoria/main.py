def linksVendaVT(service, options) -> list:
    from selenium import webdriver
    from selenium.webdriver.common.by import By
    
    links = []

    driver = webdriver.Chrome(options=options, service=service)
    driver.get("http://www.vitoriaimoveis.com.br")

    td_elements = driver.find_elements(By. TAG_NAME, "td")

    for td in td_elements:
        if td.get_attribute("height") == "420": links.append(td.find_elements(By. TAG_NAME, "a")[0].get_attribute("href"))

    driver.quit()
    
    return links