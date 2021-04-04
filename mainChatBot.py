from ChatBot import ChatBot

def main():
    data_file = 'data.txt'
    zapBot = ChatBot(data_file)
    zapBot.is_new_message()

if __name__ == "__main__": main()