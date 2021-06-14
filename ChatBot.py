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

from unidecode import unidecode

class ChatBot(object):

    def __init__(self, data_file, test):
        
        self.readFile(data_file)
        self.last_thing_knowed = self.thing_knowed[-1].casefold()
        self.week_days = ['HOJE',"digitando...","online", "ONTEM", "TERÇA-FEIRA", "SEGUNDA-FEIRA", "QUARTA-FEIRA", "QUINTA-FEIRA", "SEXTA-FEIRA", "SÁBADO", "DOMINGO"]
        self.session_status = False
        self.helper = 0
        self.aux = 0
        #span[class='_38M1B'] -> Endereço de identificação das novas mensagens 
        ##pane-side > div:nth-child(1) > div > div > div:nth-child(11) > div > div > div.TbtXF > div._2pkLM > div._3Dr46 > span
        self.css = {"new_message" : "span[class='_38M1B']",
                    "chat_box" : "#main > footer > div.vR1LG._3wXwX.copyable-area > div._2A8P4 > div > div._2_1wd.copyable-text.selectable-text",
                    "send_button" : "#main > footer > div.vR1LG._3wXwX.copyable-area > div:nth-child(3) > button > span",
                    "lasts_user_msg" : "#main",
                    "client_name": "#main > header > div._2uaUb > div > div > span",
                    "search_box" : "#side > div.SgIJV > div > label > div > div._2_1wd.copyable-text.selectable-text"}
        #pprint.pprint(self.thing_knowed)
        #pprint.pprint(self.answers[-1])
        # Inicializa o webdriver
        
        if test != 's':
            self.css.update({"new_message" : test})
        self.driver = webdriver.Chrome(
            ChromeDriverManager().install())
        # Abre o whatsappweb
        self.driver.get("https://web.whatsapp.com/")
        self.driver.maximize_window()
        # Aguarda alguns segundos para validação manual do QrCode
        input("Pressione qualquer tecla para iniciar o assistente virtual.")
        print("------------ ChatBot INICIADO -----------------------------")
    
    #Método responsavel por abrir o ultimo chat com uma nova mensangem
    def openLastChat(self, status):
        if (status == True):
            self.driver.find_element(By.CSS_SELECTOR, self.css.get("new_message")).click()
            time.sleep(2)
            data = self.get_new_message()
            self.openSession(data)
        else:
            self.is_new_message()
    def getHuman(self, person, messages, param):
        self.driver.find_element(By.CSS_SELECTOR, self.css.get("search_box")).click()
        self.driver.find_element(By.CSS_SELECTOR, self.css.get("search_box")).send_keys(self.group_name)
        self.driver.find_element(By.CSS_SELECTOR, self.css.get("search_box")).send_keys(Keys.ENTER)
        if param == True:
            self.send_message(str(person) +" "+ self.help_msg +" "+ str([time.strftime("%H:%M:%S, %d/%m/%Y",time.localtime())])) 
            time.sleep(2)
            self.session_status = False
            self.CloseSession()
        else:
            return

    #Método responsavel por verificar se o cliente tem alguma duvida.
    def send_answer(self, messages):
        if messages[-1] != unidecode(self.last_thing_knowed.casefold()):
            for i in range(len(self.thing_knowed)):
                #print("messages[-1].startswith(self.thing_knowed[i][0]) = ", messages[-1].startswith(self.thing_knowed[i][0]))
                #print("self.answers[int(self.thing_knowed[i][0]) - 1] = "+ str(self.answers[int(self.thing_knowed[i][0]) - 1]) +" "+ str([time.strftime("%H:%M:%S, %d/%m/%Y",time.localtime())]))
                if messages[-1].startswith(unidecode(self.thing_knowed[i][0].casefold())) or messages[-1].endswith(unidecode(self.thing_knowed[i][-9:-1].casefold())):
                    try:
                        self.send_message(self.answers[int(self.thing_knowed[i][0]) - 1])
                    except ValueError:
                        print("to em except ValueError linha - 82")
                        messages = self.get_new_message()
                        aux = unidecode(messages[-1].casefold())
                        if aux.startswith('oi'):
                            self.send_message(self.thing_knowed)
                if messages[-1].startswith(unidecode(self.thing_knowed[-1][0].casefold())) or messages[-1].endswith(unidecode(self.thing_knowed[-1][-9:-1].casefold())):
                    self.send_message(self.answers[-1])
                    print("entrei em if especifico do atendente")
                    self.getHuman(self.person_name, messages, True)
    def notUnderstand(self, helper, messages):
        if self.helper == 2:
            self.send_message(self.not_ustd_msg)
            self.getHuman(self.person_name, messages, True)
            return
        else:
            return
    def waitAnswer(self, messages):
        count_loops = 0 
        while messages[-1] == unidecode(self.last_thing_knowed.casefold()):
            print("Estou em while messages[-1] == unidecode(self.last_thing_knowed) e count_loops = ", count_loops)
            time.sleep(5)
            messages = self.get_new_message()
            #messages[-1] = messages[-1].replace(messages[-1][len(messages[-1]) - 8:], '')
            count_loops = count_loops + 1
            if count_loops == 12:
                #print("estou em if count_loops == 12")
                break
            elif messages[-1] != unidecode(self.last_thing_knowed.casefold()):
                print("estou em elif messages[-1] != unidecode(self.last_thing_knowed)")
                if not self.isKnowed(messages):
                    print("estou em elif self.isKnowed(messages)")
                    self.send_message(self.not_understand)
                    self.helper = self.helper + 1
                    self.notUnderstand(self.helper, messages)
                else:
                    print("estou em else return")
                    return
            
        if count_loops == 12:
            print("estou em if count_loops == 12 fora do while")
            self.session_status = False
            self.CloseSession()
        
    def moreHelp(self, messages):
        self.send_message([self.need_more_help])
        more_help = ['sim', 's', 'simmm', 'simm', 'pode']
        no_more_help = ['nao', 'não', 'n', 'obrigado', 'obrigada', 'obg', 'valeu', 'vlw']
        messages = self.get_new_message()
        #messages[-1] = messages[-1].replace(messages[-1][len(messages[-1]) - 8:], '')
        time.sleep(1)
        print("Messages[-1] fora do segundo while = ", messages[-1])
        #print("(messages[-1] in (more_help or no_more_help)), fora do segundo while = ", not messages[-1] in (more_help or no_more_help))
        
        count_loops = 0
        while ((not messages[-1] in more_help) and (not messages[-1] in no_more_help) and
                (not bool([i for i in range(len(self.thing_knowed)) if messages[-1].startswith(unidecode(self.thing_knowed[i][0].casefold()))])) and
                not bool([i for i in range(len(self.thing_knowed)) if messages[-1].endswith(unidecode(self.thing_knowed[i][-9:-1].casefold()))])):
            print("estou em not messages[-1] in (more_help or no_more_help)")
            time.sleep(5)
            messages = self.get_new_message()
            #messages[-1] = messages[-1].replace(messages[-1][len(messages[-1]) - 8:], '')
            count_loops = count_loops + 1
            if messages[-1] != unidecode(self.need_more_help.casefold()) and messages[-1] != unidecode(self.not_understand.casefold()):
                print("estou em if messages[-1] != unidecode(self.need_more_help.casefold())")
                if (messages[-1] in more_help) or (messages[-1] in no_more_help) or messages[-1].startswith('s') or messages[-1].startswith('n'):
                    print("estou em if (messages[-1] in more_help) or (messages[-1] in no_more_help):")
                    return
                elif not self.isKnowed(messages):
                    print("estou em elif self.isKnowed(messages)")
                    self.send_message([self.not_understand])
                    self.helper = self.helper + 1
                    self.notUnderstand(self.helper, messages)
            elif messages[-1] == unidecode(self.not_understand.casefold()):
                print("estou em elif messages[-1] == unidecode(self.not_understand.casefold())")
                self.send_message([self.need_more_help])
            if count_loops == 12:
                #print("estou em if count_loops == 12")
                break
            print("Messages[-1] no segundo while = ", messages[-1])
            #print("not messages[-1] in (more_help or no_more_help)), dentro do segundo while = ", not messages[-1] in (more_help or no_more_help))    
        if count_loops == 12:
            print("estou em if count_loops == 12 fora do while")
            self.session_status = False
            self.CloseSession()

    def routineOfSession(self, messages, op):
        time.sleep(1)
        messages = self.get_new_message()
        #messages[-1] = messages[-1].replace(messages[-1][len(messages[-1]) - 8:], '')
        self.waitAnswer(messages)
        print("voltei para routineOfSession")
        messages = self.get_new_message()
        self.send_answer(messages)
        time.sleep(1)
        #self.waitAnswer(messages)
        messages = self.get_new_message()
        if messages[-1] == self.last_thing_knowed:
            self.session_status = False
            self.CloseSession()
        else:
            self.moreHelp(messages)
        
        time.sleep(1)
        messages = self.get_new_message()
        self.doubtOrNot(messages)
        return messages
    
    #Método responsavel por abrir uma nova sessão para o atendimento de um cliente.
    def openSession(self, messages = []):
        
        self.session_status = True
        print("self.last_thing_knowed = ", self.last_thing_knowed)
        #messages = self.get_new_message()
        #pprint.pprint(messages)
        #messages[-1] = messages[-1].replace(messages[-1][len(messages[-1]) - 8:], '')
        messages = self.get_new_message()
        if self.isKnowed(messages):
            print("to no if de isknowed em openSession")
            self.doubtOrNot(messages)
        else:
            print("to no else de isknowed em openSession")
            self.send_message(self.thing_knowed)
        messages = self.get_new_message()
        #messages[-1] = messages[-1].replace(messages[-1][len(messages[-1]) - 8:], '')
        ###################################################################################
        #messages = self.routineOfSession(messages)
        print("estou em open session = ", messages[-1])
        more_help = ['sim', 's', 'simmm', 'simm']    
        time.sleep(2)
        self.aux = 0
        #while self.session_status:
        #   if self.aux == 0:
        print("vou chamar routineofsession de dentro de openSession")
        messages = self.routineOfSession(messages, ne)
        time.sleep(3)
        self.doubtOrNot(messages)
    #  else:

    # self.aux = self.aux + 1
    def isKnowed(self,messages):
        if ((bool([i for i in range(len(self.thing_knowed)) if messages[-1].startswith(unidecode(self.thing_knowed[i][0].casefold()))])) or 
            (bool([i for i in range(len(self.thing_knowed)) if messages[-1].endswith(unidecode(self.thing_knowed[i][-9:-1].casefold()))]))):
            return True
        else: 
            return False

    #Método responsavel por verificar se o cliente possui alguma dúvida.
    def doubtOrNot(self, messages):
        if ((messages[-1] in ['sim', 'pode', 's']) or messages[-1].startswith('s')):
            print("estou em if messages[-1].startswith('s')")
            self.send_message(self.thing_knowed, True)
            messages = self.get_new_message()
            self.routineOfSession(messages, eq)
            self.session_status = True
            return
        elif (self.isKnowed(messages)):
            self.send_answer(messages)
            self.routineOfSession(messages, eq)
            self.session_status = True
            return
        elif messages[-1].startswith('n') or messages[-1].startswith('o') or messages[-1].startswith('v'):
            print("estou em elif messages[-1].startswith('n')")
            self.send_message([self.bye])
            self.session_status = False
            self.CloseSession()
            return
    #Metodo responsavel por fechar a sessão de atendimento
    def CloseSession(self):
        if self.session_status == False:
            self.helper = 0
            self.is_new_message()
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
            self.aux = self.aux + 1
            if self.aux == 1:
                self.getHuman("",[""], False)
            
            print("estou em except NoSuchElementException e numero de vezes = ", self.aux)
            time.sleep(10)
            self.is_new_message()
            
    #Metodo responsavel por enviar uma mensagem
    def send_message(self, message = None, help1 = False):
        if message is None:
            message = self.hello_msg
        if self.driver.find_element(By.CSS_SELECTOR, self.css.get("chat_box")):
            print("Entrei")
            self.driver.find_element(By.CSS_SELECTOR, self.css.get("chat_box")).click()
            if message != self.thing_knowed:
                self.driver.find_element(By.CSS_SELECTOR, self.css.get("chat_box")).send_keys(message)
                self.driver.find_element(By.CSS_SELECTOR, self.css.get("chat_box")).send_keys(Keys.ENTER)
            elif (message == self.thing_knowed) and (help1 == True):
                self.driver.find_element(By.CSS_SELECTOR, self.css.get("chat_box")).send_keys(self.doubt + '\ue008' + '\ue007' )
                for i in range(len(message)):
                    self.driver.find_element(By.CSS_SELECTOR, self.css.get("chat_box")).send_keys(message[i] + '\ue008' + '\ue007' )#+ '\ue00a' + '\ue007'
                self.driver.find_element(By.CSS_SELECTOR, self.css.get("chat_box")).send_keys(Keys.ENTER)
                
            else: 
                self.driver.find_element(By.CSS_SELECTOR, self.css.get("chat_box")).send_keys(self.hello_msg + '\ue008' + '\ue007')#+ '\ue00a' + '\ue007'
                for i in range(len(message)):
                    self.driver.find_element(By.CSS_SELECTOR, self.css.get("chat_box")).send_keys(message[i] + '\ue008' + '\ue007' )#+ '\ue00a' + '\ue007'
                self.driver.find_element(By.CSS_SELECTOR, self.css.get("chat_box")).send_keys(Keys.ENTER)
            time.sleep(2)
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
        for i in range(len(data)):
            data[i] = unidecode(data[i])
        
        return data



    #Manipulação da lista de strings de ultimas mensagens
    def handler_string(self, string):
        import re
        from datetime import datetime
        time1 = []
        message = []
        r = re.compile('.{2}:.{2}')
        audio = re.compile('.{1}:.{2}')
        for i in string:
            if len(i) == 5:
                if r.match(i):
                    aux = string.index(i)
                    time1.append(i)
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
        while len(string) != len(time1):
            try:
                string.pop(0)
            except IndexError:
                print("to em except IndexError")
                time.sleep(1)
                self.get_new_message()
        for i in range(len(time1)):
            message.append(string[i].casefold())
        return message
    def readFile(self, data_file):
        THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))
        my_file = os.path.join(THIS_FOLDER, data_file)
        with open(my_file, 'r', encoding= 'utf8', errors='ignore') as f:
            data = f.readlines()
        list = []
        #pprint.pprint(data)
        for row in data:
            if not row.startswith('#') and not row.startswith('\n'):
                list.append(row.strip())
        #pprint.pprint(list)
        self.hello_msg, *thing_knowed, self.need_more_help, self.doubt, self.group_name, self.help_msg, self.not_understand, self.not_ustd_msg, self.bye = list
        self.thing_knowed = []
        self.answers = []
        #pprint.pprint(thing_knowed)
        for thing in thing_knowed:
            #print("thing no for = ", thing)
            if not thing.startswith("R:"):
                self.thing_knowed.append(thing)
                #print("thing no if  = ", thing)
            else:
                #print("thing no else  = ", thing)
                thing = thing.replace(thing[:7], '')
                
                self.answers.append(thing)
        #print(self.thing_knowed)
        
data_file = 'data.txt'
test = "#pane-side > div:nth-child(1) > div > div > div:nth-child(11) > div > div > div.TbtXF"
#zapBot = ChatBot(data_file, test)
#zapBot.is_new_message()
#zapBot.readFile()        
#data_file = 'data.txt'
#zapBot = ChatBot(data_file, 's')
#zapBot.is_new_message()
#zapBot.get_new_message()
#main > div._2wjK5 > div > div > div._11liR > div:nth-child(29) > div > div > div > div.xkqQM.copyable-text > div > span._3-8er.selectable-text.copyable-text > span