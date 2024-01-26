def linksVendaAR(service, options) -> list:
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC 
    from selenium import webdriver

    links = []

    driver = webdriver.Chrome(options=options, service=service)
    driver.get("https://www.arevalimoveis.com.br/imoveis/a-venda/vilhena")

    while True:
        try: WebDriverWait(driver, timeout = 3).until(EC.element_to_be_clickable((By. XPATH, "/html/body/div[3]/section[1]/div/div/div/div/div[1]/div[2]/div[2]/div[2]/div/div/div/button")))
        except: break

        driver.execute_script("document.getElementsByClassName('btn btn-md btn-primary btn-next')[0].click()")

    links_loc = driver.find_elements(By. CLASS_NAME, "card_split_vertically")
    
    for element in links_loc:
        links.append(element.get_attribute("href"))

    driver.quit()
    return links