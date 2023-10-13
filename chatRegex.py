import sys
import time
import requests as req
from bs4 import BeautifulSoup as bs
import re

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
        self.bookStore['selected_novel'] = text
        print(title + " " +"Novel data loaded... \n")
        
    def processQuery(self, query, novel_selection):
        #Novel Information - Going to make regex expressions instead
        if novel_selection == '1':
            investigator = 'Sherlock Holmes'
            investigator2 = 'John Watson'
            crime = 'Death' #'Murder', 'Killing'
            perpetrator = r'\b(?:(John |Mr. )?Stapleton|Rodger( Baskerville)?)\b'
            suspect1 = 'James Mortimer'
            suspect2 = 'Beryl Stapleton'
            suspect3 = 'Henry Baskerville'
            suspect4 = 'Mr. Barrymore'
            suspect5 = 'Mrs. Barrymore'
        elif novel_selection == '2':
            investigatorr = r'\b(?:Young Adventurers|Tommy( Beresford)?|(Prudence )?Tuppence( Cowley)?)\b'
            investigator = 'Tommy Beresford'
            investigator2 = 'Prudence Tuppence Cowley'
            crime = 'Revolution' #Labor unrest
            perpetrator = r'\b(?:(Mr. )?Brown|(Sir )?James( Peel Edgerton)?)\b'
            suspect1 = 'Mr. Whittington'
            suspect2 = 'Julius Hersheimmer'
            suspect3 = 'Jane Finn'
            suspect4 = 'Mr. Brown'
        elif novel_selection == '3':
            investigator = 'Hercule Poirot'
            crime = 'Death' #'Murder', 'Killing'
            perpetrator = r'\b(?:Mr. Alfred Inglethorp|Alfred Inglethorp|Alfred|Mr. Inglethorp|Miss Howard|Evelyn( Howard)?)\b'
            suspect1 = 'Lawrence Cavendish'
            suspect2 = 'Cynthia Murdoch'
            suspect3 = 'Dr. Bauerstein'
            suspect4 = 'Evelyn Howard'

        book_text = self.bookStore['selected_novel']

        #Question Parsing
        q1 = r'^(?=.*\bwhen\b)(?=.*\b(investigator(s)?|pair|duo|partner(s)?|detective(s)?)\b)(?=.*\bfirst\b)(?=.*\b(mention(ed)?|appear(s)?|occur(s)?|show(s)? up|shown|introduce(d)?|arrive(s)?)\b)'
        q2 = r'^(?=.*\bwhen\b)(?=.*\b(crime(s)?|theft(s)?|burglary|burglaries|murder(s)?|attack(s)?)\b)(?=.*\bfirst\b)(?=.*\b(mention(ed)?|appear(s)?|occur(s)?|show(s)? up|shown|introduce(d)?|arrive(s)?|happen(s)?)\b)'
        q3 = r'^(?=.*\bwhen\b)(?=.*\b(perpetrator(s)?|criminal(s)?|thief(s)?|murderer(s)?|attacker(s)?|burglar(s)?)\b)(?=.*\bfirst\b)(?=.*\b(mention(ed)?|appear(s)?|occur(s)?|show(s)? up|shown|introduce(d)?|arrive(s)?)\b)'
        q4 = r'^(?=.*\bwhat\b)(?=.*\bthree\b)(?=.*\bwords\b)(?=.*\b(mention(ed)?|appear(s)?|occur(s)?|show(s)? up|shown|introduce(d)?|happen(s)?)\b)(?=.*\b(perpetrator(s)?|criminal(s)?|thief(s)?|murderer(s)?|attacker(s)?|burglar(s)?)\b)'
        q5 = r'^(?=.*\bwhen\b)(?=.*\b(investigator(s)?|pair|duo|partner(s)?|detective(s)?)\b)(?=.*\b(perpetrator(s)?|criminal(s)?|thief(s)?|murderer(s)?|attacker(s)?|burglar(s)?)\b)(?=.*\b(co |co-)?(together|mention(ed)?|appear(s)?|occur(s)?|show(s)? up|shown|introduce(d)?|arrive(s)?)\b)'
        q6 = r'^(?=.*\bwhen\b)(?=.*\b(suspect(s)?|accused|defendant(s)?)\b)(?=.*\bfirst\b)(?=.*\b(mention(ed)?|appear(s)?|occur(s)?|show(s)? up|shown|introduce(d)?|arrive(s)?)\b)'

        if re.search(q1, query, re.IGNORECASE):
            print("When does the investigator (or a pair) occur for the first time -  chapter #, the sentence(s) # in a chapter")
        elif re.search(q2, query, re.IGNORECASE):
            print("When is the crime first mentioned - the type of the crime and the details -  chapter #, the sentence(s) # in a chapter")
        elif re.search(q3, query, re.IGNORECASE):
            print("When is the perpetrator first mentioned - chapter #, the sentence(s) # in a chapter")
        elif re.search(q4, query, re.IGNORECASE):
            matches = re.finditer(perpetrator, book_text)
            count = 0
            for match in matches:
                count = count + 1
                words_before = re.findall(r'\w+', book_text[:match.start()])[-3:]
                words_after = re.findall(r'\w+', book_text[match.end():])[:3]

                print("Match ", count, ". Words before match: ", words_before, sep = '')
                print("Match ", count, ". Words after match:  ", words_after, sep = '')
        elif re.search(q5, query, re.IGNORECASE):
            print("When and how the detective/detectives and the perpetrators co-occur - chapter #, the sentence(s) # in a chapter")
        elif re.search(q6, query, re.IGNORECASE):
            print("When are other suspects first introduced - chapter #, the sentence(s) # in a chapter")
        else:
            print("I am unable to answer that question")

        #print(self.bookStore['selected_novel']) #Get text
        return 
    
    def run(self, novel_selection):
        while self.processRun:
            print("Type 'exit' or 'quit' to terminate\n")
            queryString = input("Enter the query: ")
            if not re.match(self.onlyAlphabets, queryString):
                self.print_red("Please enter only english characters")

            if queryString == "quit" or queryString == "exit":
                self.processRun = False
            else:
                self.processQuery(queryString, novel_selection)

        print("Chat completed..!\n")

chat = ChatRegex()

novel_selection = input("Select a novel to analyze(1-3): \n1. The Hound of the Baskervilles by Arthur Conan Doyle\n2. The Secret Adversary, by Agatha Christie\n3. The Mysterious Affair at Styles by Agatha Christie\nSelection: ")

while novel_selection not in ('1', '2', '3'):
    print("\nThat input was not valid. Enter a number 1-3 corresponding to a novel below")
    novel_selection = input("Select a novel to analyze(1-3): \n1. The Hound of the Baskervilles by Arthur Conan Doyle\n2. The Secret Adversary, by Agatha Christie\n3. The Mysterious Affair at Styles by Agatha Christie\nSelection: ")

print()

if novel_selection == '1': #The Hound of Baskervilles - Arthur Conan Doyle
    chat.loadData("https://www.gutenberg.org/cache/epub/2852/pg2852-images.html")
elif novel_selection == '2': #The Secret Adversary - Agatha Christie
    chat.loadData("https://www.gutenberg.org/cache/epub/1155/pg1155-images.html")
elif novel_selection == '3': #The Mysterious Affair at Styles - Agatha Christie
    chat.loadData("https://www.gutenberg.org/cache/epub/863/pg863-images.html")


chat.run(novel_selection)