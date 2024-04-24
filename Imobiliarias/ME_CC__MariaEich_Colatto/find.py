from selenium import webdriver
from selenium.webdriver.common.by import By
try: from Imobiliarias.ME_CC__MariaEich_Colatto.main import linksVendaME_CC
except: from main import linksVendaME_CC

def findVendaME_CC(service, options) -> list:
    links = linksVendaME_CC(service, options)

    driver = webdriver.Chrome(options=options, service=service)
    
    #(0) Url, (1) área total, (2) área do terreno (excluída ao final), (3) área construída, (4) área útil (excluída ao final),(5) dormitórios, (6) suítes, (7) banheiros, (8) vagas garagem, (9) bairro, (10) valor, (11) tipo de imóvel, (12) tipo de negócio, (13) descrição
    global infos
    infos = [[],[],[],[],[],[],[],[],[],[],[],[],[],[]]

    infos_sub_primary = [["total", "terreno", "construída", "útil", "dormitório", "suíte", "banheiro", "vaga"],
                         [1,2,3,4,5,6,7,8]]
    
    types_of_add = [["apartamento", "barracao", "galpao", "casa", "sobrado", "terreno", "predio", "sala", "ponto"],
                   ["AP", "BA", "BA", "CA", "SO", "TE", "PR", "SA", "PT"]]

    for index_link, link in enumerate(links):
        driver.get(link)
        print(f"{links.index(link)+1}/{len(links)}", link)
        infos[0].append(link)

        ve_lo = False

        #Tipo de Negócio:
        negc_type = driver.find_element(By.CLASS_NAME, "pretensao").text.lower().strip()

        if negc_type == "venda": infos[12].append("VE")
        elif negc_type == "locação": infos[12].append("LO")
        elif negc_type == 'venda / locação': 
            ve_lo = True
            if links.index(link) == index_link:
                links.insert(links.index(link) + 1, link)
                infos[12].append("VE")
            else:
                infos[12].append("LO")


        else: infos[12].append("None")

        for div_info in driver.find_elements(By. CLASS_NAME, "esquerda_ficha")[0].find_elements(By. CLASS_NAME, "detalhe"):
            for text_info in div_info.text.replace("sendo","/").split(" / "):
                text_sub = text_info.split(" ")[-1]
                if text_sub == "": break
                if text_sub[-1] == "s": text_sub = text_sub[:-1]
                try: index = infos_sub_primary[1][infos_sub_primary[0].index(text_sub)]
                except: break

                infos[index].append(text_info.split(" ")[0].replace("m²","").strip())
                if text_sub == "vaga": break


        #Bairro:
        try: 
            text_neighborhood = driver.find_elements(By.CLASS_NAME, "cidade_bairro")[0].text
            infos[9].append(text_neighborhood[text_neighborhood.find("-")+1:].strip())
        except: pass


        #Valor:
        try: 
            div_price_master = driver.find_element(By.CLASS_NAME, "valor")
            index_price = 0
            
            if ve_lo == True and links.index(link) < index_link:
                index_price = 1
                
            div_price = float(div_price_master.find_elements(By.TAG_NAME, "h3")[index_price].text.replace("R$","").replace(".","").replace(",",".").strip())
            infos[10].append(div_price)
        except: infos[10].append("None")

        #Tipo do Imóvel:
        ad_type = driver.find_element(By.CLASS_NAME, "info_imovel").find_element(By.CLASS_NAME, "titulo").text.lower()

        for index_type, type_add_verify in enumerate(types_of_add[0]):
            if ad_type.find(type_add_verify) != -1: 
                infos[11].append(types_of_add[1][index_type])
                break
        else: infos[11].append("None")
        

        #Descrição:
        try: 
            descrip_text = driver.find_element(By.CLASS_NAME, "descricao").find_element(By.TAG_NAME, "div").text
            infos[13].append(descrip_text)
        except: pass


        #Adiciona None nos campos sem informações:
        for info_verify in infos:
            if len(info_verify) < links.index(link) + 1: info_verify.append("None")


        #Filtra a área total correta entre os campos "Área Total" e "Área do Terreno":
        areaTotal = infos[1][-1]
        areaTerreno = infos[2][-1]
        areaCons = infos[3][-1]
        areaPriv = infos[4][-1] 

        areas = [infos[1][-1], infos[2][-1], infos[3][-1], infos[4][-1]]

        areas = sorted([val for val in areas if val != "None"])

        areas = sorted(list(set(areas)))
        
        if areaTotal != "None" and areaTotal == areas[-1]: 
            pass

        elif len(areas) > 1 or (len(areas) == 1 and (areas[0] == areaTotal or areas[0] == areaTerreno)):
            infos[1][-1] = areas[-1]

        #Filtra a área construída correta entre todos os campos de área caso o campo "Área Construída" seja igual a "None":
            
        if areaCons != "None" and areaCons == areas[0]:
            pass

        elif len(areas) > 1 or (len(areas) == 1 and (areas[0] == areaCons or areas[0] == areaPriv)):
            infos[3][-1] = areas[0]
    
    #Deleta o campo "Área do Terreno" e "Área Privativa" pois todas as suas informações pertinentes já foram movidas para o campo "Área Total":
    del infos[2]
    del infos[3]

    driver.quit()
    return infos