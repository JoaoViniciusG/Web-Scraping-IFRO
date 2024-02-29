def findVendaFB_CF_SR_CR(service, options) -> list:
    from selenium import webdriver
    from selenium.webdriver.common.by import By
    try: from Fb_Corretor__Caio_Fernandes__Samuel__Concretize.main import linksVendaFB_CF_SR_CR
    except: from main import linksVendaFB_CF_SR_CR
    from time import time

    time_start = time()

    links = linksVendaFB_CF_SR_CR(service, options)

    driver = webdriver.Chrome(options=options, service=service)

    #Área total, área do terreno, área construída, dimensões, dormitórios, suítes, banheiros, vagas garagem, descrição, código do imóvel, bairro, valor
    infos = [[],[],[],[],[],[],[],[],[],[],[]]

    infos_sub_primary = [["Área Total", "Área Terreno", "Área Construída", "Código", "Bairro", "Dormitório", "Suíte", "Banheiro", "Vaga"], 
                         [0,1,2,8,9,3,4,5,6]]

    for link in links:
        driver.get(link)
        print(f"{links.index(link)+1}/{len(links)}", link)

        for tag in driver.find_element(By. ID, "desc_tags").find_elements(By. TAG_NAME, "p"):
            try: index = infos_sub_primary[1][infos_sub_primary[0].index(tag.text.split(":")[0])]
            except: continue
            info = tag.text.split(":")[1].replace(".","").replace(",",".").replace("m²","").strip()
            try: 
                if float(info) == "0": continue
            except: pass

            infos[index].append(info)

        #Cômodos
        for tag_rooms in driver.find_elements(By. CLASS_NAME, "info__tag"):
            text_room = tag_rooms.find_elements(By. TAG_NAME, "p")[-1].text.split(" ")[-1]
            if text_room[-1] == "s": text_room = text_room[:-1]

            try: index = infos_sub_primary[1][infos_sub_primary[0].index(text_room)]
            except: continue

            infos[index].append(tag_rooms.find_elements(By. TAG_NAME, "p")[-1].text.split(" ")[0])

        #Descrição:
        try: 
            text_desc = driver.find_element(By. XPATH, '//*[@id="desc_descricao"]/p[1]').text
            if text_desc != "": infos[7].append(text_desc)
        except: pass
        
        #Valor:
        try: infos[10].append(float(driver.find_element(By. ID, "info__valor").text.replace("R$ ","").replace(".","").replace(",",".")))
        except: pass        

        #Adiciona None nos campos sem informações:
        for info_verify in infos:
            if len(info_verify) < links.index(link) + 1: info_verify.append("None")

        #Retira o Código do Imóvel dos anúncios da imobiliária Samuel Richard, pois estão erroneamente classificados como tal:
        if link.find("samuelrichard.com") != -1:
            infos[8][-1] = "None"
    
    
    time_final = time()
    print(f"{time_final - time_start} segundos")
    return infos