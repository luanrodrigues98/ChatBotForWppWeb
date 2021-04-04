import time 
import os
import pprint
from operator import ne, eq

#pip install selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException

#pip install webdriver-manager
from webdriver_manager.chrome import ChromeDriverManager

class ChatBot(object):

    def __init__(self, data_file):
        
        self.readFile(data_file)
        self.last_thing_knowed = self.thing_knowed[-1].replace(self.thing_knowed[-1][len(self.thing_knowed[-1]) - 1:], '').casefold()
        self.week_days = ['HOJE',"digitando...","online", "ONTEM", "TERÇA-FEIRA", "SEGUNDA-FEIRA", "QUARTA-FEIRA", "QUINTA-FEIRA", "SEXTA-FEIRA", "SÁBADO", "DOMINGO"]
        self.session_status = False
        
        #span[class='_38M1B'] -> Endereço de identificação das novas mensagens 
        self.css = {"new_message" : "span[class='_38M1B']",
                    "chat_box" : "#main > footer > div.vR1LG._3wXwX.copyable-area > div._2A8P4 > div > div._2_1wd.copyable-text.selectable-text",
                    "send_button" : "#main > footer > div.vR1LG._3wXwX.copyable-area > div:nth-child(3) > button > span",
                    "lasts_user_msg" : "#main",
                    "client_name": "#main > header > div._2uaUb > div > div > span"}
        # Inicializa o webdriver
        self.driver = webdriver.Chrome(
            ChromeDriverManager().install())
        # Abre o whatsappweb
        self.driver.get("https://web.whatsapp.com/")
        self.driver.maximize_window()
        # Aguarda alguns segundos para validação manual do QrCode
        self.driver.implicitly_wait(30)
    
    #Método responsavel por abrir o ultimo chat com uma nova mensangem
    def openLastChat(self, status):
        if (status == True):
            self.driver.find_element(By.CSS_SELECTOR, self.css.get("new_message")).click()
            time.sleep(5)
            data = self.get_new_message()
            self.openSession(data)
        else:
            self.is_new_message()
    
    #Método responsavel por verificar se o cliente tem alguma duvida.
    def routineOfSession(self, messages, op):
        while op(messages[-1], self.last_thing_knowed):
            print("messages[-1] != self.last_thing_knowed")
            time.sleep(5)
            messages = self.get_new_message()
            messages[-1] = messages[-1].replace(messages[-1][len(messages[-1]) - 8:], '')
            #print("messages[-1] != self.last_thing_knowed, no while = ", (messages[-1] != self.last_thing_knowed))
            #print("Messages[-1] no while = ", messages[-1])
        time.sleep(5)
        messages = self.get_new_message()
        messages[-1] = messages[-1].replace(messages[-1][len(messages[-1]) - 8:], '')           
        if messages[-1] != self.last_thing_knowed:
            for i in range(len(self.thing_knowed)):
                if messages[-1].startswith(self.thing_knowed[i][0]) or messages[-1].endswith(self.thing_knowed[i][-9:-1]):
                    self.send_message(self.answers[int(self.thing_knowed[i][0]) - 1])
        time.sleep(5)
        self.send_message([self.need_more_help])
        more_help = ['sim', 's', 'simmm', 'simm']
        no_more_help = ['nao', 'não', 'n']
        messages = self.get_new_message()
        messages[-1] = messages[-1].replace(messages[-1][len(messages[-1]) - 8:], '')
        time.sleep(5)
        print("Messages[-1] fora do segundo while = ", messages[-1])
        #print("(messages[-1] in (more_help or no_more_help)), fora do segundo while = ", not messages[-1] in (more_help or no_more_help))
        while (not messages[-1] in more_help) and (not messages[-1] in no_more_help):
            print("estou em not messages[-1] in (more_help or no_more_help)")
            time.sleep(5)
            messages = self.get_new_message()
            messages[-1] = messages[-1].replace(messages[-1][len(messages[-1]) - 8:], '')
            print("Messages[-1] no segundo while = ", messages[-1])
            #print("not messages[-1] in (more_help or no_more_help)), dentro do segundo while = ", not messages[-1] in (more_help or no_more_help))    
        
        time.sleep(5)
        messages = self.get_new_message()
        self.doubtOrNot(messages)
        return messages
    
    #Método responsavel por abrir uma nova sessão para o atendimento de um cliente.
    def openSession(self, messages = []):
        
        self.session_status = True
        print("self.last_thing_knowed = ", self.last_thing_knowed)
        #messages = self.get_new_message()
        #pprint.pprint(messages)
        welcome_msg = ['oi', 'olá', 'oii', 'oiii', 'ola', 'olaa', 'olaaa']
        messages[-1] = messages[-1].replace(messages[-1][len(messages[-1]) - 8:], '')
        if messages[-1] in welcome_msg:
            self.send_message()
            time.sleep(5)
            self.send_message(self.thing_knowed)            
        elif messages[-1] != welcome_msg:
            self.send_message()
            time.sleep(5)
            self.send_message(self.thing_knowed)
        messages = self.get_new_message()
        messages[-1] = messages[-1].replace(messages[-1][len(messages[-1]) - 8:], '')
        ###################################################################################
        #messages = self.routineOfSession(messages)
        print(messages[-1])
        more_help = ['sim', 's', 'simmm', 'simm']    
        time.sleep(10)
        self.aux = 0
        #while self.session_status:
        #   if self.aux == 0:
        messages = self.routineOfSession(messages, ne)
        time.sleep(5)
        self.doubtOrNot(messages)
    #  else:

    # self.aux = self.aux + 1

    #Método responsavel por verificar se o cliente possui alguma dúvida.
    def doubtOrNot(self, messages):
        if messages[-1].startswith('s'):
            print("estou em if messages[-1].startswith('s')")
            self.send_message([self.doubt])
            time.sleep(5)
            self.send_message(self.thing_knowed)
            messages = self.get_new_message()
            self.routineOfSession(messages, eq)
            self.session_status = True
            return
        elif messages[-1].startswith('n'):
            print("estou em elif messages[-1].startswith('n')")
            self.send_message([self.bye])
            self.session_status = False
            self.CloseSession()
            return
    #Metodo responsavel por fechar a sessão de atendimento
    def CloseSession(self):
        if self.session_status == False:
            self.is_new_message()
            self.aux = 0
        else:
            pass

    #Metodo responsavel por verificar se existe alguma mensagem
    def is_new_message(self):
        #<span class="_38M1B" aria-label="6 mensagens não lidas">6</span>
        #pane-side > div:nth-child(1) > div > div > div:nth-child(10) > div > div > div.TbtXF > div._1SjZ2 > div._15smv > span:nth-child(1) > div > span
        try: 
            if self.driver.find_element(By.CSS_SELECTOR, self.css.get("new_message")):
                self.openLastChat(True)
            elif not self.driver.find_element(By.CSS_SELECTOR, self.css.get("new_message")):
                self.is_new_message()
        except NoSuchElementException:
            pass
    #Metodo responsavel por enviar uma mensagem
    def send_message(self, message = None):
        if message is None:
            message = self.hello_msg
        if self.driver.find_element(By.CSS_SELECTOR, self.css.get("chat_box")):
            print("Entrei")
            self.driver.find_element(By.CSS_SELECTOR, self.css.get("chat_box")).click()
            self.driver.find_element(By.CSS_SELECTOR, self.css.get("chat_box")).send_keys(message)
            self.driver.find_element(By.CSS_SELECTOR, self.css.get("chat_box")).send_keys(Keys.ENTER)
            time.sleep(5)
            #self.is_new_message()
        else: 
            print("nao entrei")
    #Metodo responsavel por receber as ultimas mensagens.
    def get_new_message(self):
        if self.driver.find_element(By.CSS_SELECTOR, self.css.get("lasts_user_msg")):
            msg = self.driver.find_element(By.CSS_SELECTOR, self.css.get("lasts_user_msg")).text
            list_today_msg = msg.splitlines()
        #pprint.pprint(list_today_msg)
        self.person_name = list_today_msg[0]
        list_today_msg.pop(0)
        list_today_msg.pop(-1)
        data = self.handler_string(list_today_msg)
        return data



    #Manipulação da lista de strings de ultimas mensagens
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
            message.append((string[i] + " [" + time[i] + "]").casefold())
        return message
    def readFile(self, data_file):
        THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))
        my_file = os.path.join(THIS_FOLDER, data_file)
        with open(my_file, 'r', encoding= 'utf8', errors='ignore') as f:
            data = f.readlines()
        list = []
        for row in data:
            if not row.startswith('#') and not row.startswith('\n'):
                list.append(row.strip())
        
        self.hello_msg, *thing_knowed, self.need_more_help, self.doubt, self.bye = list
        self.thing_knowed = []
        self.answers = []
        for thing in thing_knowed:
            if not thing.startswith("R:"):
                self.thing_knowed.append(thing + '\n')
            else:
                
                thing = thing.replace(thing[:7], '')
                
                self.answers.append(thing)
        
        

#zapBot.get_new_message()
#main > div._2wjK5 > div > div > div._11liR > div:nth-child(29) > div > div > div > div.xkqQM.copyable-text > div > span._3-8er.selectable-text.copyable-text > span