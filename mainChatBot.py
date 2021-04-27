from ChatBot import ChatBot

def main():
    data_file = 'data.txt'
    print("Olá, essa é uma pequena interface de usuário para o ChatBot para WhatsApp Web, preciso que você me digita algumas informações.\n")
    test = input("Você precisa da detectação de novas mensagens automatica ligada? Se sim, digite 's'. Se não, cole o CSS selector correspondente ao contato de teste:\n")
    
    zapBot = ChatBot(data_file, test)
    zapBot.is_new_message()
    
if __name__ == "__main__": main()