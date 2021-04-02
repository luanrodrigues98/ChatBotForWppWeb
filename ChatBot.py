import time 
#pip install selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
#pip install webdriver-manager
from webdriver_manager.chrome import ChromeDriverManager
import os
import pprint
class ChatBot():
    # O local de execução do nosso script
    dir_path = os.getcwd()
    # O caminho do chromedriver
    chromedriver = os.path.join(dir_path, "chromedriver.exe")
    # Caminho onde será criada pasta profile
    profile = os.path.join(dir_path, "profile", "wpp")
    def __init__(self):
        self.thing_knowed = [
            "1 - Qual o nome completo do Luan?\n",
            "2 - Quando o Luan nasceu?\n",
            "3 - Onde ele estuda?\n"
            "4 - Qual o nome da mãe do Luan?\n"
        ]
        self.answers = [
            'Luan Rodrigues Soares de Souza.',
            '26 de janeiro de 2000.',
            'Instituto Politécnico Do Estado Do Rio De Janeiro - IPRJ é o campus da Universidade do Estado do Rio de Janeiro em Nova Friburgo.',
            'Jozelma.'
        ]
        self.week_days = ["HOJE", "ONTEM", "TERÇA-FEIRA", "SEGUNDA-FEIRA", "QUARTA-FEIRA", "QUINTA-FEIRA", "SEXTA-FEIRA", "SÁBADO", "DOMINGO"]
        self.session_status = False
        ##pane-side > div:nth-child(1) > div > div > div:nth-child(9) > div > div > div.TbtXF
        #span[class='_38M1B']
        self.css = {"new_message" : "#pane-side > div:nth-child(1) > div > div > div:nth-child(11) > div > div > div.TbtXF > div._2pkLM > div._3Dr46 > span",
                    "chat_box" : "#main > footer > div.vR1LG._3wXwX.copyable-area > div._2A8P4 > div > div._2_1wd.copyable-text.selectable-text",
                    "send_button" : "#main > footer > div.vR1LG._3wXwX.copyable-area > div:nth-child(3) > button > span",
                    "lasts_user_msg" : "#main",
                    "client_name": "#main > header > div._2uaUb > div > div > span"}
        # Inicializa o webdriver
        #<div tabindex="-1" class="_1JAUF _2x4bz"><div class="OTBsx" style="visibility: visible;">Digite uma mensagem</div><div class="_2_1wd copyable-text selectable-text" contenteditable="true" data-tab="6" dir="ltr" spellcheck="true"></div></div>
        self.driver = webdriver.Chrome(
            ChromeDriverManager().install())
        # Abre o whatsappweb
        self.driver.get("https://web.whatsapp.com/")
        self.driver.maximize_window()
        # Aguarda alguns segundos para validação manual do QrCode
        self.driver.implicitly_wait(15)
    
    def openLastChat(self, status):
        if (status == True):
            self.driver.find_element(By.CSS_SELECTOR, self.css.get("new_message")).click()
            time.sleep(5)
            self.get_new_message()
        else:
            self.is_new_message()
    def openSession(self):
        self.session_status = True
        last_msg = self.last_client_msg.get(self.person_name).casefold()
        pprint.pprint(last_msg)
        welcome_msg = ['oi', 'olá', 'oii', 'oiii', 'ola', 'olaa', 'olaaa']
        
        if last_msg in welcome_msg:
            self.send_message()
        elif last_msg != welcome_msg:
            self.send_message()
            time.sleep(5)
            self.send_message(self.thing_knowed)
        time.sleep(15)
        self.get_new_message(False)
        
        last_msg = self.last_client_msg.get(self.person_name).casefold()
        pprint.pprint(last_msg)
        
        for i in range(len(self.thing_knowed)):
            print(last_msg.endswith(self.thing_knowed[i][len(last_msg) - 3 : ]))
            if last_msg.startswith(self.thing_knowed[i][0]) or last_msg.endswith(self.thing_knowed[i][-4:]):
                self.send_message(self.answers[int(self.thing_knowed[i][0]) - 1])



    def is_new_message(self):
        #<span class="_38M1B" aria-label="6 mensagens não lidas">6</span>
        try: 
            if self.driver.find_element(By.CSS_SELECTOR, self.css.get("new_message")):
                self.openLastChat(True)
            elif not self.driver.find_element(By.CSS_SELECTOR, self.css.get("new_message")):
                self.is_new_message()
        except NoSuchElementException:
            pass
    
    def send_message(self, message = ['Olá, sou a Natália, assistente virtual do Whatsapp do Luan. Vou te mostrar algumas coisas que sei fazer.']):
        if self.driver.find_element(By.CSS_SELECTOR, self.css.get("chat_box")):
            print("Entrei")
            self.driver.find_element(By.CSS_SELECTOR, self.css.get("chat_box")).click()
            self.driver.find_element(By.CSS_SELECTOR, self.css.get("chat_box")).send_keys(message)
            self.driver.find_element(By.CSS_SELECTOR, self.css.get("chat_box")).send_keys(Keys.ENTER)
            time.sleep(5)
            #self.is_new_message()
        else: 
            print("nao entrei")

    def get_new_message(self, param = True):
        if self.driver.find_element(By.CSS_SELECTOR, self.css.get("lasts_user_msg")):
            msg = self.driver.find_element(By.CSS_SELECTOR, self.css.get("lasts_user_msg")).text
            list_today_msg = msg.splitlines()
        self.person_name = list_today_msg[0]
        list_today_msg.pop(0)
        list_today_msg.pop(-1)
        data = self.handler_string(list_today_msg)
        self.last_client_msgs = {}
        self.last_client_msg = {}
        self.last_client_msgs[self.person_name] = data
        self.last_client_msg[self.person_name] = data[-1]
        if param:
            self.openSession()




    def handler_string(self, string):
        import re
        from datetime import datetime
        time = []
        message = []
        r = re.compile('.{2}:.{2}')
        audio = re.compile('.{1}:.{2}')
        for i in string:
            if len(i) == 5:
                if r.match(i):
                    aux = string.index(i)
                    time.append(i)
                    string.pop(aux)
        for i in string:
            if len(i) == 4:
                if audio.match(i):
                    aux = string.index(i)
                    string.pop(aux)
            elif i.endswith("MENSAGENS NÃO LIDAS"):
                aux = string.index(i)
                string.pop(aux)
            elif i.startswith("@"):
                aux = string.index(i)
                string.pop(aux)
        i = 0
        while i < len(string):
            if string[i] in self.week_days:
                string.remove(string[i])
                i = 0
            else:
                i = i + 1 
        while len(string) != len(time):
            string.pop(0)
        for i in range(len(time)):
            message.append(string[i] + " [" + time[i] + "]")
        return message

zapBot = ChatBot()
zapBot.is_new_message()
#zapBot.get_new_message()
#main > div._2wjK5 > div > div > div._11liR > div:nth-child(29) > div > div > div > div.xkqQM.copyable-text > div > span._3-8er.selectable-text.copyable-text > span