from Imobiliarias.AR__Areval.find import findVendaAR
from Imobiliarias.GA_PD__Padrao_Gama.find import findVendaGA_PD
from Imobiliarias.VT__Vitoria.find import findVendaVT
from Imobiliarias.FB_CF_SR_CR__FbCorretor_CaioFernandes_Samuel_Concretize.find import findVendaFB_CF_SR_CR
from Imobiliarias.DR__Deiro.find import findVendaDR
from Imobiliarias.CD_IC__CarlosDepine_ImobiliariaCeara.find import findVendaCD_IC
from Imobiliarias.BZ__Bortolanzza.find import findVendaBZ
from Imobiliarias.FT__Futura.find import findVendaFT
from Imobiliarias.ME_CC__MariaEich_Colatto.find import findVendaME_CC
from Imobiliarias.AP__Alpha.find import findVendaAP
from Imobiliarias.BC__Balcao.find import findVendaBC
from Imobiliarias.CH__ClaudioHenrique.find import findVendaCH
from Imobiliarias.JL__JaineLima.find import findVendaJL
from Imobiliarias.DC__DonadoniCorretor.find import findVendaDC
from Imobiliarias.EM__EliaMeireles.find import findVendaEM
from Imobiliarias.RM__ReMax.find import findVendaRM
from Imobiliarias.JP__JoaoPaulo.find import findVendaJP
from Imobiliarias.PC__PrettoCorretora.find import findVendaPC
from Imobiliarias.WE__Wender.find import findVendaWE

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