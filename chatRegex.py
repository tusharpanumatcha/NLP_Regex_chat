import html
import sys
import time
import requests as req
from bs4 import BeautifulSoup as bs
import re
import random

class ChatRegex:
    def __init__(self) -> None:
        self.processRun = True
        self.bookStore = {}
        self.onlyAlphabets = r'\b([A-Za-z]+)\b'
        self.chapters = []
        self.novelName = {
            "1": "The Hound of the Baskervilles by Arthur Conan Doyle",
            "2": "The Secret Adversary, by Agatha Christie",
            "3": "The Mysterious Affair at Styles by Agatha Christie"
        }
        self.detectiveAnswerTemplates = [
            {
                "template": "In the novel [Novel Title], the investigator [Investigator Name] first appears in Chapter [Chapter Number], sentence [Sentence Number].\n",
                "variables": ["Novel Title", "Investigator Name", "Chapter Number", "Sentence Number"]
            },
            {
                "template": "You first encounter the investigator [Investigator Name] in Chapter [Chapter Number], sentence number [Sentence Number].\n",
                "variables": ["Novel Title", "Investigator Name", "Chapter Number", "Sentence Number"]
            },
            {
                "template": "The investigator [Investigator Name] makes their initial appearance in Chapter [Chapter Number], specifically in sentence [Sentence Number].\n",
                "variables": ["Novel Title", "Investigator Name", "Chapter Number", "Sentence Number"]
            },
            {
                "template": "In [Novel Title], the investigator [Investigator Name] is introduced for the first time in Chapter [Chapter Number], sentence [Sentence Number].\n",
                "variables": ["Novel Title", "Investigator Name", "Chapter Number", "Sentence Number"]
            },
            {
                "template": "The first appearance of the investigator [Investigator Name] takes place in Chapter [Chapter Number], sentence [Sentence Number].\n",
                "variables": ["Novel Title", "Investigator Name", "Chapter Number", "Sentence Number"]
            }
        ]
        self.crimeAnswerTemplates = [
            {
                "template": "The first mention of the crime in [Novel Title] occurs in Chapter [Chapter Number], sentence [Sentence Number].\n",
                "variables": ["Novel Title", "Chapter Number", "Sentence Number"]
            },
            {
                "template": "In Chapter [Chapter Number] of [Novel Title], the crime is first mentioned in sentence [Sentence Number].\n",
                "variables": ["Novel Title", "Chapter Number", "Sentence Number"]
            },
            {
                "template": "The crime is initially introduced in Chapter [Chapter Number] of [Novel Title], specifically in sentence [Sentence Number].\n",
                "variables": ["Novel Title", "Chapter Number", "Sentence Number"]
            },
            {
                "template": "You first learn about the crime in [Novel Title] in Chapter [Chapter Number], sentence [Sentence Number].\n",
                "variables": ["Novel Title", "Chapter Number", "Sentence Number"]
            },
            {
                "template": "The initial mention of the crime in [Novel Title] takes place in Chapter [Chapter Number], sentence [Sentence Number].\n",
                "variables": ["Novel Title", "Chapter Number", "Sentence Number"]
            }
        ]
        self.perpetratorAnswerTemplates = [
            {
                "template": "The perpetrator is first mentioned in [Novel Title] in Chapter [Chapter Number], sentence [Sentence Number].\n",
                "variables": ["Novel Title", "Chapter Number", "Sentence Number"]
            },
            {
                "template": "In Chapter [Chapter Number] of [Novel Title], the perpetrator is first introduced in sentence [Sentence Number].\n",
                "variables": ["Novel Title", "Chapter Number", "Sentence Number"]
            },
            {
                "template": "You first encounter the perpetrator in Chapter [Chapter Number] of [Novel Title], specifically in sentence [Sentence Number].\n",
                "variables": ["Novel Title", "Chapter Number", "Sentence Number"]
            },
            {
                "template": "The initial mention of the perpetrator in [Novel Title] occurs in Chapter [Chapter Number], sentence [Sentence Number].\n",
                "variables": ["Novel Title", "Chapter Number", "Sentence Number"]
            },
            {
                "template": "The perpetrator makes their first appearance in [Novel Title] in Chapter [Chapter Number], sentence [Sentence Number].\n",
                "variables": ["Novel Title", "Chapter Number", "Sentence Number"]
            }
        ]
        self.perpetratorSurroundingAnswerTemplates = [
            {
                "template": "The three words that occur around each mention of the perpetrator in [Novel Title] are the following:\n",
                "variables": ["Novel Title"]
            },
            {
                "template": "In [Novel Title], the three words that are said around each mention of the criminal are the following:\n",
                "variables": ["Novel Title"]
            },
            {
                "template": "The following are the three words that occur around each mention of the perpetrator in [Novel Title]:\n",
                "variables": ["Novel Title"]
            }
        ]
        self.togetherAnswerTemplates = [
            {
                "template": "In the novel [Novel Title], the investigator [Investigator Name] and perpetrator [Perpetrator Name] first appear together in Chapter [Chapter Number], sentence [Sentence Number].\n",
                "variables": ["Novel Title", "Investigator Name", "Perpetrator Name", "Chapter Number", "Sentence Number"]
            },
            {
                "template": "You first encounter the investigator [Investigator Name] and perpetrator [Perpetrator Name] together in Chapter [Chapter Number], sentence number [Sentence Number].\n",
                "variables": ["Novel Title", "Investigator Name", "Perpetrator Name", "Chapter Number", "Sentence Number"]
            },
            {
                "template": "The investigator [Investigator Name] and the perpetrator [Perpetrator Name] make their initial appearance together in Chapter [Chapter Number], specifically in sentence [Sentence Number].\n",
                "variables": ["Novel Title", "Investigator Name", "Perpetrator Name", "Chapter Number", "Sentence Number"]
            },
            {
                "template": "In [Novel Title], the investigator [Investigator Name] and perpetrator [Perpetrator Name] are introduced together for the first time in Chapter [Chapter Number], sentence [Sentence Number].\n",
                "variables": ["Novel Title", "Investigator Name", "Perpetrator Name", "Chapter Number", "Sentence Number"]
            },
            {
                "template": "The first appearance of the investigator [Investigator Name] and perpetrator [Perpetrator Name] together takes place in Chapter [Chapter Number], sentence [Sentence Number].\n",
                "variables": ["Novel Title", "Investigator Name", "Perpetrator Name", "Chapter Number", "Sentence Number"]
            }
        ]
        self.suspectsIntroducedAnswerTemplates = [
            {
                "template": "Other suspects are first introduced in [Novel Title] in Chapter [Chapter Number], sentence [Sentence Number].\n",
                "variables": ["Novel Title", "Chapter Number", "Sentence Number"]
            },
            {
                "template": "In Chapter [Chapter Number] of [Novel Title], other suspects make their first appearance in sentence [Sentence Number].\n",
                "variables": ["Novel Title", "Chapter Number", "Sentence Number"]
            },
            {
                "template": "You first encounter other suspects in Chapter [Chapter Number] of [Novel Title], specifically in sentence [Sentence Number].\n",
                "variables": ["Novel Title", "Chapter Number", "Sentence Number"]
            },
            {
                "template": "The initial introduction of other suspects in [Novel Title] occurs in Chapter [Chapter Number], sentence [Sentence Number].\n",
                "variables": ["Novel Title", "Chapter Number", "Sentence Number"]
            },
            {
                "template": "Other suspects make their first appearance in [Novel Title] in Chapter [Chapter Number], sentence [Sentence Number].\n",
                "variables": ["Novel Title", "Chapter Number", "Sentence Number"]
            }
        ]

    def generateAnswer(self, respArray, values):
        num = random.randint(0, len(respArray)-1)
        template = respArray[num]
        for variable in template["variables"]:
            if variable in values:
                template["template"] = template["template"].replace(f"[{variable}]", str(values[variable]))
            else:
                print(f"Warning: Variable '{variable}' not found in values dictionary.")
        text = template["template"]
        for char in text:
            print(char, end='', flush=True)
            time.sleep(0.05) 
        print()

    def spinningCursor(self):
        while True:
            for cursor in '|/-\\': yield cursor

    def extractUrl(self, url):
        response = req.get(url)
        html_content = response.content
        soup = bs(html_content, 'html.parser')

        chapter_divs = soup.find_all('div', class_='chapter')

        chapters = []
        pattern = r'(Chapter\s+[IVXLCDM\d]+\s*\.?\s*|\b[A-Za-z]+\b)'
        for chapter_div in chapter_divs:
            chapter_name = chapter_div.find('h2').text if chapter_div.find('h2') else None
            if chapter_name is not None and re.findall(pattern, chapter_name):
                chapter_content = ' '.join([html.unescape(p.text.strip()) for p in chapter_div.find_all('p')]) if chapter_div.find_all('p') else None
                chapter_name = chapter_name.replace("\n", "")
                chapters.append({"chapterName": chapter_name, "chapterContent": chapter_content})
        # for i, chapter in range(chapters):
        #     print(chapter.chapterName)
        return chapters

    def print_red(text):
        print(f"\033[91m{text}\033[0m")

    def loadData(self, url):
        spinner = self.spinningCursor()
        for _ in range(50):
            sys.stdout.write(next(spinner))
            sys.stdout.flush()
            time.sleep(0.1)
            sys.stdout.write('\b')
        #List of chapters and contents as {"chapterName":"" , "chapterContent": ""}
        self.chapters = self.extractUrl(url)

        #for chapter in self.chapters:
        #    print(f"Chapter Name: {chapter['chapterName']}")
        #    print(f"Chapter Content: {chapter['chapterContent']}")    
        
    def processQuery(self, query, novel_selection):
        if novel_selection == '1':
            investigatorOne = r'\b(?:((Mr. )?Sherlock Holmes|(Mr. )?Sherlock|(Mr. )?Holmes))\b'
            investigatorTwo = r'\b(?:Dr\.)?\s?(?:John\s)?Watson\b'
            crime = r'\b(?:kill|killed|killing|manslaughter|assassination|execution|annihilation|liquidation|slaughter|butchery|termination|carnage|death|demise|extermination|murder)\b'
            perpetrator = r'\b(?:(John |Mr. )?Stapleton|Rodger( Baskerville)?)\b'
            suspectRegexArray = [
                r'\bDr\.\sJames\sMortimer\b',
                r'\bJack\sStapleton\b',
                r'\bBeryl\sStapleton\b',
                r'\bFrankland\b',
                r'\bMr\.\sBarrymore\b',
                r'\bMrs\.\sBarrymore\b',
                r'\bMr\.\sLaura\sLyons\b',
                r'\bMrs\.\sLaura\sLyons\b',
                r'\bSelden\b'
            ]
        elif novel_selection == '2':
            investigatorOne = r'\b(?:(Mr.)?(Tommy|Thomas)( Beresford)?)\b'
            investigatorTwo = r'\b(?:(Miss )?Prudence( Cowley)?|(Miss )?Tuppence)\b'
            #(the )?Young Adventurers(, Ltd.)?|
            crime = r'\b(?:Labour Unrest|Revolution(s)?|(Labour )?coup?)\b'
            perpetrator = r'\b(?:(Mr. )?Brown|(Sir )?James( Peel Edgerton)?)\b'
            suspectRegexArray = [
                r'\b(?:(Mr. )?((Edward )?Whittington))\b',
                r'\b(?:(Mr. )?(Julius P. |Julius )?Hersheimmer)\b',
                r'\b(?:Jane( Finn)?)\b'
            ]
        elif novel_selection == '3':
            investigatorOne = r'\b(?:(Monsieur |Hercule )?Poirot)\b'
            investigatorTwo = "FALSE"
            crime = r'\b(?:(strychnine )?(poisoned|poisoning)?|(Wilful )?Murder(ing|ed)?|Killed)\b'
            perpetrator = r'\b(?:Mr. Alfred Inglethorp|Alfred Inglethorp|Alfred|Mr. Inglethorp|Miss Howard|Evelyn( Howard)?)\b'
            suspect1 = r'\b(?:(Mr.( John)?|John|(Mrs. )?Lawrence) Cavendish|Cavendishes)\b'
            suspect2 = r'\b(?:(Miss|Evelyn) Howard|Evelyn)\b'
            suspect3 = r'\b(?:Mrs. Raikes)\b'

        q1 = r'^(?=.*\bwhen\b)(?=.*\b(investigator(s)?|pair|duo|partner(s)?|detective(s)?)\b)(?=.*\bfirst\b)(?=.*\b(mention(ed)?|appear(s)?|occur(s)?|show(s)? up|shown|introduce(d)?|arrive(s)?)\b)'
        q2 = r'^(?=.*\bwhen\b)(?=.*\b(crime(s)?|theft(s)?|burglary|burglaries|murder(s)?|attack(s)?)\b)(?=.*\bfirst\b)(?=.*\b(mention(ed)?|appear(s)?|occur(s)?|show(s)? up|shown|introduce(d)?|arrive(s)?|happen(s)?)\b)'
        q3 = r'^(?=.*\bwhen\b)(?=.*\b(perpetrator(s)?|criminal(s)?|thief(s)?|murderer(s)?|attacker(s)?|burglar(s)?)\b)(?=.*\bfirst\b)(?=.*\b(mention(ed)?|appear(s)?|occur(s)?|show(s)? up|shown|introduce(d)?|arrive(s)?)\b)'
        q4 = r'^(?=.*\bwhat\b)(?=.*\bthree\b)(?=.*\bwords\b)(?=.*\b(mention(ed)?|appear(s)?|occur(s)?|show(s)? up|shown|introduce(d)?|happen(s)?)\b)(?=.*\b(perpetrator(s)?|criminal(s)?|thief(s)?|murderer(s)?|attacker(s)?|burglar(s)?)\b)'
        q5 = r'^(?=.*\bwhen\b)(?=.*\b(investigator(s)?|pair|duo|partner(s)?|detective(s)?)\b)(?=.*\b(perpetrator(s)?|criminal(s)?|thief(s)?|murderer(s)?|attacker(s)?|burglar(s)?)\b)(?=.*\b(co |co-)?(together|mention(ed)?|appear(s)?|occur(s)?|show(s)? up|shown|introduce(d)?|arrive(s)?)\b)'
        q6 = r'^(?=.*\bwhen\b)(?=.*\b(suspect(s)?|accused|defendant(s)?)\b)(?=.*\bfirst\b)(?=.*\b(mention(ed)?|appear(s)?|occur(s)?|show(s)? up|shown|introduce(d)?|arrive(s)?)\b)'

        if re.search(q1, query, re.IGNORECASE):
            #print("When does the investigator (or a pair) occur for the first time -  chapter #, the sentence(s) # in a chapter")
            self.investigatorDetect(investigatorOne, novel_selection)
            if investigatorTwo != "FALSE":
                self.investigatorDetect(investigatorTwo, novel_selection)
        elif re.search(q2, query, re.IGNORECASE):
            #print("When is the crime first mentioned - the type of the crime and the details -  chapter #, the sentence(s) # in a chapter")
            self.crimeDetect(crime, novel_selection)
        elif re.search(q3, query, re.IGNORECASE):
            #print("When is the perpetrator first mentioned - chapter #, the sentence(s) # in a chapter")
            self.perpetratorDetect(perpetrator, novel_selection)
        elif re.search(q4, query, re.IGNORECASE):
            #print("What are the three words that occur around the perpetrator on each mention (i.e., the three words preceding and the three words following the mention of a perpetrator)")
            self.perpetratorSurrounding(perpetrator)
        elif re.search(q5, query, re.IGNORECASE):
            #print("When and how the detective/detectives and the perpetrators co-occur - chapter #, the sentence(s) # in a chapter")
            self.togetherDetect(investigatorOne, perpetrator, novel_selection)
            #if investigatorTwo != "FALSE":
            #    self.togetherDetect(investigatorTwo, perpetrator, novel_selection)
        elif re.search(q6, query, re.IGNORECASE):
            #print("When are other suspects first introduced - chapter #, the sentence(s) # in a chapter")
            self.suspectDetect(suspectRegexArray, novel_selection)
        else:
            print("I am unable to answer that question")

        return 
            
    def investigatorDetect(self, investigator, novel_selection):
        for chapter in self.chapters:
            content = str(chapter['chapterContent'])
            match = re.search(investigator, content)
            if match:
                matches = re.finditer(investigator, content)
                for match in matches:
                    punctuation_pattern = r'(?<!Mr|Ms|Mr|Dr)(?<!Mrs)[.!?]( |\n|\”|\"|$)'
                    punctuation_matches = re.findall(punctuation_pattern, str(chapter['chapterContent'])[:match.end()])
                    num_punctuation = len(punctuation_matches)
                    values = {
                        "Novel Title": self.novelName.get(str(novel_selection)),
                        "Investigator Name": match.group(),
                        "Chapter Number": chapter['chapterName'],
                        "Sentence Number": num_punctuation + 1
                    }
                    self.generateAnswer(self.detectiveAnswerTemplates, values)
                    return

    def crimeDetect(self, crime, novel_selected):
        for chapter in self.chapters:
            content = str(chapter['chapterContent'])
            match = re.search(crime, content)
            if match:
                matches = re.finditer(crime, content)
                for match in matches:
                    punctuation_pattern = r'(\n)'
                    punctuation_matches = re.findall(punctuation_pattern, str(chapter['chapterContent'])[:match.end()])
                    num_punctuation = len(punctuation_matches)
                    # print(match.group(), "First mentioned in: ")
                    # print("Chapter-", count)
                    # print("Sentence-", num_punctuation + 1)
                    value = {
                        "Novel Title": self.novelName[str(novel_selected)].replace("\r", ""), 
                        "Chapter Number": chapter['chapterName'].replace("\r", ""), 
                        "Sentence Number": num_punctuation + 1
                    }
                    self.generateAnswer(self.crimeAnswerTemplates, value)
                    return

    def perpetratorDetect(self, perpetrator, novel_selection):
        for chapter in self.chapters:
            content = str(chapter['chapterContent'])
            match = re.search(perpetrator, content)
            if match:
                matches = re.finditer(perpetrator, content)
                for match in matches:
                    punctuation_pattern = r'(?<!Mr|Ms|Mr|Dr)(?<!Mrs)[.!?]( |\n|\”|\"|$)'
                    punctuation_matches = re.findall(punctuation_pattern, str(chapter['chapterContent'])[:match.end()])
                    num_punctuation = len(punctuation_matches)
                    values = {
                        "Novel Title": self.novelName[str(novel_selection)], 
                        "Chapter Number": chapter['chapterName'].replace("\r", ""), 
                        "Sentence Number": num_punctuation + 1
                    }
                    self.generateAnswer(self.perpetratorAnswerTemplates, values)
                    return

    def perpetratorSurrounding(self, perpetrator):
        count = 0
        book_text = ""
        for chapter in self.chapters:
            if(chapter['chapterContent'] != None):
                book_text = book_text + " " + chapter['chapterContent']
            count = count + 1
        values = {
            "Novel Title": self.novelName[str(novel_selection)]
        }

        self.generateAnswer(self.perpetratorSurroundingAnswerTemplates, values)

        matches = re.finditer(perpetrator, book_text)
        count = 0
        for match in matches:
            count = count + 1
            words_before = re.findall(r'\w+', book_text[:match.start()])[-3:]
            words_after = re.findall(r'\w+', book_text[match.end():])[:3]

            print("Mention", count, "- 3 words before:", words_before)
            print("Mention", count, "- 3 words after: ", words_after)
            print()

    def togetherDetect(self, investigator, perpetrator, novel_selection):
        for chapter in self.chapters:
            content = str(chapter['chapterContent'])
            investigator_match = re.search(investigator, content)
            perpetrator_match = re.search(perpetrator, content)
            if investigator_match and perpetrator_match:
                #print("\n", chapter['chapterName'], "\n")
                investigator_matches = re.finditer(investigator, content)
                perpetrator_matches = re.finditer(perpetrator, content)
                for inv_match in investigator_matches:
                    for perp_match in perpetrator_matches:
                        #print("Investigator start: ", inv_match.start(), "Investigator end: ", inv_match.end())
                        #print("Perpetrator start: ", perp_match.start(), "Perpetrator end: ", perp_match.end())
                        if((inv_match.end() <= perp_match.start() <= (inv_match.end() + 200)) | (perp_match.end() <= inv_match.start() <= (perp_match.end() + 200))):
                            if(inv_match.start() < perp_match.start()):
                                block_regex = r'(?<=[.?!])[a-zA-Z0-9-\s@#%^&*()_+\-=[\]{}|;\':"“”,\/<>~`]*' + str(chapter['chapterContent'])[inv_match.start():perp_match.end()] + r'[a-zA-Z0-9-\s@#%^&*()_+\-=[\]{}|;\':"“”,\/<>~`]*[.?!]'
                                block_match = re.search(block_regex, content)
                                #print(block_match.group())
                            else:
                                block_regex = r'(?<=[.?!])[a-zA-Z0-9-\s@#%^&*()_+\-=[\]{}|;\':"“”,\/<>~`]*' + str(chapter['chapterContent'])[perp_match.start():inv_match.end()] + r'[a-zA-Z0-9-\s@#%^&*()_+\-=[\]{}|;\':"“”,\/<>~`]*[.?!]'
                                block_match = re.search(block_regex, content)
                                #print(block_match.group())
                            punctuation_pattern = r'(?<!Mr|Ms|Mr|Dr)(?<!Mrs)[.!?]( |\n|\”|\"|$)'
                            punctuation_matches = re.findall(punctuation_pattern, str(chapter['chapterContent'])[:max(inv_match.end(), perp_match.end())])
                            num_punctuation = len(punctuation_matches)
                            values = {
                                "Novel Title": self.novelName[str(novel_selection)], 
                                "Investigator Name": inv_match.group(),
                                "Perpetrator Name": perp_match.group(),
                                "Chapter Number": chapter['chapterName'].replace("\r", ""), 
                                "Sentence Number": num_punctuation + 1
                            }
                            self.generateAnswer(self.togetherAnswerTemplates, values)
                            return
                        #print("End of Perp")
                    perpetrator_matches = re.finditer(perpetrator, content)
                    #print("End of Inv")

    def suspectDetect(self, suspectRegexArray, novel_selection):
        for suspect in suspectRegexArray:
            for chapter in self.chapters:
                content = str(chapter['chapterContent'])
                match = re.search(suspect, content)
                if match:
                    punctuation_pattern = r'(?<!Mr|Ms|Mr|Dr)(?<!Mrs)[.!?]( |\n|\”|\"|$)'
                    punctuation_matches = re.findall(punctuation_pattern, str(chapter['chapterContent'])[:match.end()])
                    num_punctuation = len(punctuation_matches)
                    print(f"{match.group()} First mentioned in:")
                    print(f"Chapter - {chapter['chapterName'].strip()}")
                    print(f"Sentence - {num_punctuation + 1}")
                    break

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
