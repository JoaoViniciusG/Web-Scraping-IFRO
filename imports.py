from Areval.find import findVendaAR
from Padrao__Gama.find import findVendaGA_PD
from Vitoria.find import findVendaVT
from Fb_Corretor__Caio_Fernandes__Samuel__Concretize.find import findVendaFB_CF_SR_CR
from Deiro.find import findVendaDR
from Carlos_depine__Imobiliaria_Ceara.find import findVendaCD_IC
from Bortolanzza.find import findVendaBZ
from Futura.find import findVendaFT
from Maria_Eich.find import findVendaME
from Alpha.find import findVendaAP
from Balcao.find import findVendaBC
from Claudio_Henrique.find import findVendaCH
from Jaine_Lima.find import findVendaJL

from joblib import Parallel, delayed
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium import webdriver

service = Service(ChromeDriverManager().install())
options = Options()
options.add_argument("headless")
options.add_argument('log-level=3')
options.add_argument('--blink-settings=imagesEnabled=false')