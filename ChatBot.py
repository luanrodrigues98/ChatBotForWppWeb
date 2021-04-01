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
        
        ##pane-side > div:nth-child(1) > div > div > div:nth-child(9) > div > div > div.TbtXF
        #span[class='_38M1B']
        self.css = {"new_message" : "#pane-side > div:nth-child(1) > div > div > div:nth-child(2) > div > div > div.TbtXF > div._2pkLM > div._3Dr46 > span > span",
                    "chat_box" : "#main > footer > div.vR1LG._3wXwX.copyable-area > div._2A8P4 > div > div._2_1wd.copyable-text.selectable-text",
                    "send_button" : "#main > footer > div.vR1LG._3wXwX.copyable-area > div:nth-child(3) > button > span",
                    "lasts_user_msg" : "#main > div._2wjK5 > div > div > div._11liR",
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
            #self.send_message()
            self.get_new_message()
        else:
            self.is_new_message()

    def is_new_message(self):
        #<span class="_38M1B" aria-label="6 mensagens não lidas">6</span>
        try: 
            if self.driver.find_element(By.CSS_SELECTOR, self.css.get("new_message")):
                self.openLastChat(True)
            elif not self.driver.find_element(By.CSS_SELECTOR, self.css.get("new_message")):
                self.is_new_message()
        except NoSuchElementException:
            pass
    
    def send_message(self, message = "Olá, esse é o bot do wpp do Luan."):
        if self.driver.find_element(By.CSS_SELECTOR, self.css.get("chat_box")):
            print("Entrei")
            self.driver.find_element(By.CSS_SELECTOR, self.css.get("chat_box")).click()
            self.driver.find_element(By.CSS_SELECTOR, self.css.get("chat_box")).send_keys(message + Keys.ENTER)
            time.sleep(5)
            self.is_new_message()
            
            
        else: 
            print("nao entrei")
    def get_new_message(self):
        if self.driver.find_element(By.CSS_SELECTOR, self.css.get("lasts_user_msg")):
            msg = self.driver.find_element(By.CSS_SELECTOR, self.css.get("lasts_user_msg")).text
            list_today_msg = msg.splitlines()
        message = self.handler_string(list_today_msg)
        
        if self.driver.find_element(By.CSS_SELECTOR, self.css.get("client_name")):
            self.person_name = self.driver.find_element(By.CSS_SELECTOR, self.css.get("client_name")).text
        self.last_client_msgs = {}
        self.last_client_msg = {}
        self.last_client_msgs[self.person_name] = message
        self.last_client_msg[self.person_name] = message[-1]
        print(self.last_client_msg)

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
        for i in range(len(time)):
            message.append(string[i] + " [" + time[i] + "]")
        return message

zapBot = ChatBot()
zapBot.is_new_message()
#zapBot.get_new_message()
#main > div._2wjK5 > div > div > div._11liR > div:nth-child(29) > div > div > div > div.xkqQM.copyable-text > div > span._3-8er.selectable-text.copyable-text > span