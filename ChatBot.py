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
        self.css = {"new_message" : "span[class='_38M1B']",
                    "chat_box" : "#main > footer > div.vR1LG._3wXwX.copyable-area > div._2A8P4 > div > div._2_1wd.copyable-text.selectable-text",
                    "send_button" : "#main > footer > div.vR1LG._3wXwX.copyable-area > div:nth-child(3) > button > span"}
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
            self.send_message()
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
            self.driver.find_element(By.CSS_SELECTOR, self.css.get("chat_box")).send_keys(message)
            time.sleep(4)
            self.driver.find_element(By.CSS_SELECTOR, self.css.get("send_button")).click()
            time.sleep(5)
            self.is_new_message()
            
            
        else: 
            print("nao entrei")
zapBot = ChatBot()
zapBot.is_new_message()
