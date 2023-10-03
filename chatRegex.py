import sys
import time
import requests as req
from bs4 import BeautifulSoup as bs
import re as regex

class ChatRegex:
    def __init__(self) -> None:
        self.processRun = True
        self.bookStore = {}
        self.onlyAlphabets = r'\b([A-Za-z]+)\b'

    def spinningCursor(self):
        while True:
            for cursor in '|/-\\': yield cursor

    def extractUrl(self, url):
        response = req.get(url)
        title = response.text.split('<title>')[1].split('</title>')[0] 
        text = bs(response.content, 'html.parser').get_text()
        return title, text 

    def print_red(text):
        print(f"\033[91m{text}\033[0m")

    def loadData(self, url):
        spinner = self.spinningCursor()
        for _ in range(50):
            sys.stdout.write(next(spinner))
            sys.stdout.flush()
            time.sleep(0.1)
            sys.stdout.write('\b')
        title, text = self.extractUrl(url)
        title = title.replace("The Project Gutenberg eBook of ", "")
        self.bookStore[title] = text
        print(title + " " +"Novel data loaded... \n")
        
    def processQuery(self, query):
        r'^(who|what|where|when|why|how)\s'
        return 
    
    def run(self):

        while self.processRun:
            print("Type 'exit' or 'quit' to terminate\n")
            queryString = input("Enter the query: ")
            if not regex.match(self.onlyAlphabets, queryString):
                self.print_red("Please enter only english alpherbets")

            if queryString == "quit" or queryString == "exit":
                self.processRun = False
            
            self.processQuery(queryString)

        print("Chat completed..!\n")

chat = ChatRegex()

chat.loadData("https://www.gutenberg.org/cache/epub/2852/pg2852-images.html")
chat.loadData("https://www.gutenberg.org/files/244/244-h/244-h.htm")
chat.loadData("https://www.gutenberg.org/cache/epub/1155/pg1155-images.html")

chat.run()
