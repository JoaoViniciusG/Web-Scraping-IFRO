def findVendaVT(service, options) -> list:
    from selenium import webdriver
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC 
    try: from VT__Vitoria.main import linksVendaVT
    except: from main import linksVendaVT
    
    links = linksVendaVT(service, options)

    driver = webdriver.Chrome(options=options, service=service)

    #Área total, área do terreno, área construída, código do imóvel, dimensões do terreno (frente/fundo X esquerda/direita), dormitórios, banheiros, suítes, vagas garagem, descrição
    #características, cômodos, proximidades, bairro, valor

    infos = [[],[],[],[],[],[],[],[],[],[],[],[],[],[],[]]

    infos_sub_areas = ["Área Total:", "Área Terreno:", "Área Construída:", "Código:"]
    infos_sub_dimensions = ["Terreno Frente:", "Terreno Fundo:", "Terreno Esquerda:", "Terreno Direita:"]
    

    for link in links:
        driver.get(link)
        print(f"{links.index(link)+1}/{len(links)}", link)

        WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By. XPATH, '//*[@id="ContatoCx1"]/div[2]/div[3]/input')))

        #Áreas e código do imóvel:
        infos_dimensions_and_code = driver.find_element(By. ID, "detimo_desc").text.split("|")

        dimensions = []

        for i, sub in enumerate([infos_sub_areas, infos_sub_dimensions]):
            for index, info_d_sub in enumerate(sub):
                for info_d_and_c in infos_dimensions_and_code:
                    if i == 0:
                        try: 
                            info_d_and_c.index(info_d_sub)
                            infos[index].append(info_d_and_c.split(info_d_sub)[-1].strip().replace(",","."))
                            del infos_dimensions_and_code[infos_dimensions_and_code.index(info_d_and_c)]
                        except: pass
                    else:
                        try: 
                            info_d_and_c.index(info_d_sub)
                            dimensions.append(info_d_and_c.split(info_d_sub)[-1].replace(",",".").replace("Metros","").strip())
                        except: pass

        if len(dimensions) == 2: infos[4].append(f"{dimensions[0]}X{dimensions[1]}")
        elif len(dimensions) == 4: infos[4].append(f"{dimensions[0]}/{dimensions[1]}X{dimensions[2]}/{dimensions[3]}")

        #Dormitórios, banheiros, suítes, vagas na garagem:
        for index, element in enumerate(driver.find_elements(By. CLASS_NAME, "detimo_itensfonte")[1:]):
            if element.text != "":
                infos[5 + index].append(element.text.split(" ")[0].strip())

        #Descrição:
        try: infos[9].append(driver.find_element(By. XPATH, '//*[@id="detimo_descricao3"]/h1').text)
        except: pass

        #Características, cômodos, proximidades:
        infos_sub_description = ["Características", "Cômodos", "Proximidades"]

        for u in driver.find_elements(By. CLASS_NAME, "fonte_padrao.imovel_cx_caracteristicas"):
            index = infos_sub_description.index(u.find_element(By. CLASS_NAME, "cxSpan").text)

            text_description = ""
            for element in u.find_elements(By. CLASS_NAME, "cxItem"):
                text_description += element.text + "\n"

            text_description = text_description[0:-1]
            infos[10 + index].append(text_description)


        #Bairro:
        text_neighborhood = driver.find_element(By. XPATH, '//*[@id="detimo_titulo"]/h1').text

        infos[13].append(text_neighborhood.split(",")[2].replace("bairro","").strip())

        #Valor:
        text_price = driver.find_element(By. CLASS_NAME, "detimo_itensfonteval.li_ftcor").find_element(By. TAG_NAME, "span").text
        try: infos[14].append(float(text_price.split("R$")[-1].replace(".","").replace(",",".")))
        except: pass

        #Adiciona None nos campos sem informações
        for info_verify in infos:
            if len(info_verify) < links.index(link) + 1: info_verify.append("None")
    
    return infos