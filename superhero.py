import re
import sys
import time
from time import sleep
import colorama
from colorama import Fore, Style
import numpy as np
import pandas as pd
import random
import tkinter as tk
from PIL import ImageTk, Image
import requests
from io import BytesIO
import nltk
import pickle
from operator import itemgetter
import lxml
from bs4 import BeautifulSoup
import requests

df_csv = pd.read_csv('superheroes_nlp_dataset.csv')
data = pd.read_csv('superheroes_nlp_dataset.csv', index_col ="name")

def getrealname(userinput):
  getinfo(userinput, "real name is", "real_name")

def getrandomhistory():
  row = random.randint(0,1450)
  print(Fore.YELLOW + "Here is the history of",df_csv.at[row, 'name'], Style.RESET_ALL + "\n", df_csv.at[row,'history_text'], "\n")

def getpowers(userinput):
  getinfo(userinput, "powers", 'superpowers')

def getoverallscore(userinput):
  getinfo(userinput, "overall score", 'overall_score')

def getcombatscore(userinput, ret = 0):
  if ret == 0:
    getinfo(userinput, "combat score", 'combat_score')
  else:
    return getinfo(userinput, "combat score", 'combat_score', 1)

# DONT RUN
def getimage(userinput):
    # userinput = re.sub('[^A-Za-z0-9]+', '', userinput)
    # herofound = False

    # regex to recognize input between does and look
    hero_name_regex = re.compile('[wW]hat does (.*) look like')
    # get entered hero name from between does and look
    hero_name = hero_name_regex.search(userinput).group(1)
    # print("User entered", hero_name)

    showImages(hero_name)


def showImages(hero_name):
    herofound = False

    for x in range(1450):
        name = str(df_csv.at[x, 'name'])
        # name = name.split(None, 1)[0]

        if hero_name in name:
            # print(name)
            temp = str(df_csv.at[x, 'img'])
            herofound = True
            if temp != "nan":
                root = tk.Tk()
                img_url = "https://www.superherodb.com" + temp
                response = requests.get(img_url)
                img_data = response.content
                img = ImageTk.PhotoImage(Image.open(BytesIO(img_data)))
                panel = tk.Label(root, image=img)
                panel.pack(side="bottom", fill="both", expand="yes")
                panel2 = tk.Label(root, justify=tk.LEFT, padx=10, text=name).pack(side="top")
                root.mainloop()

    if not herofound:
        suggestion = didyoumean(hero_name)
        botprint("No records of Entity:" + hero_name + "\n")
        botprint("Did you mean " + suggestion + "? (yes/no)\n")
        userinput = input(Fore.GREEN + "> ")
        if userinput == 'yes':
            showImages(suggestion)
        else:
            botprint("Which hero did you mean then?\n")
            userinput = input(Fore.GREEN + "> ")
            return showImages(userinput)

def getinfo(userinput, query, search, ret=0):
  functionmemory("getinfo")
  ret_list=[]
  if len(userinput) < 15:
    userinput = userinput
  elif '-' in userinput:
    userinput = ''.join(re.findall(r'\b[A-Z0-9][-a-zA-Z0-9]+|\b[A-Z]\b', userinput))
  else: userinput = ' '.join(re.findall(r'\b[A-Z0-9][-a-zA-Z0-9]+|\b[A-Z]\b', userinput))
  #userinput = re.sub('[^A-Za-z0-9 .-]+', '', userinput)
  #userinput = userinput[:-1]
  herofound = False
  #print(userinput)
  for x in range(1450):
    name = str(df_csv.at[x,'name'])
    #name = name.split(None, 1)[0]
    if userinput in name:
      herofound = True
      temp = df_csv.at[x, search]
      if ret == 0:
        temp = str(temp)
        if temp != "nan" and temp != "[]" and temp != "-":
          print(Fore.YELLOW + df_csv.at[x,'name'], query + ": " + Style.RESET_ALL, temp, "\n")
      else:
          item = []
          item.append(name)
          item.append(temp)
          ret_list.append(item)

  if not herofound:
    suggestion = didyoumean(userinput)
    botprint("No records of Entity: " + userinput + "\n")
    botprint("Did you mean " + suggestion + "?\n")
    userinput = userinputs()
    if userinput == 'yes':
      if ret == 0:
        getinfo(suggestion, query, search)
      else:
        ret_list = getinfo(suggestion, query, search, 1)
    else:
      botprint("Please re-enter just the superheros name.\n")
      userinput = userinputs()
      if ret == 0:
        getinfo(userinput, query, search)
      else:
        ret_list = getinfo(userinput, query, search, 1)

  if ret == 1 and len(ret_list) > 0:
    return ret_list
  functionmemoryclose()

def getscore(userinput):
  userinput = re.sub('[^A-Za-z0-9]+', '', userinput)
  for x in range(1450):
    name = str(df_csv.at[x,'name'])
    name = name.split(None, 1)[0]
    if name in userinput:
      # intelligence_score = data.at[x, 'intelligence_score']
      scores = df_csv.loc[x,'intelligence_score':'power_score']
      print("\n--", df_csv.at[x,'name'],"--")
      print(scores)

def getteams(userinput):
  getinfo(userinput, "is part of the ", 'teams')

def getbirthplace(userinput):
  getinfo(userinput, "birth place is ", 'place_of_birth')

def getalignment(userinput):
  getinfo(userinput, "alignment is", 'alignment')

def getbase(userinput):
  getinfo(userinput, "base location", 'base')


def getheight(userinput):
  getinfo(userinput, "is",'height')
  botprint("If the version of the superhero you are looking for is not listed then their height remains a mystery to the cosmos.\n")


def getweight(userinput):
  getinfo(userinput, "weighs",'weight')
  botresponselist = ["In some versions of the universe superheros have been able to keep their weight a secret.\n","I see some Superheros dont like sharing their weight", "I'snt that interesting"]
  response = random.randrange(2)
  botprint(botresponselist[response])


def getherohistory(userinput):
  name = getnamebasic(userinput)
  getinfo(userinput, "",'history_text')
  botresponselist = ["Well thats probably going to take you a long time to read, I'll wait.", "hmmm theres some interesting stuff in there.", "Did you like the part where "+ name +"... oh never mind I dont want to spoil it.", "What a life " + name + " has lived"]
  response = random.randrange(4)
  botprint(botresponselist[response])


def unknowninput():
  botresponselist = ["Sorry, my translator must be malfunctioning again, could you rephrase that please.\n", "Do not waste my time with such meaningless questions.", "Sorry, Thanos sent me a DM what was it you wanted again?", "I refuse to respond to such nonsense", "You have the oppurtunity to learn about superheros, and you waste my time with this giberish?", "You obviously need help, just ask.", "Im still learning how to communicate with such a primitive race, could your rephrase that please.", "oh you want to be a wise guy aye!? Maybe I just wont respond next time", "Is that what you humans call a joke, becuase I dont get it..."]
  response = random.randrange(8)
  botprint(botresponselist[response])



def openingscript():
  for x in range (0,5):  
    b = "∙" * x
    print (b, end="\r")
    time.sleep(.1)
  print('\033[2K\033[1G')
  sys.stdout.write("\033[F")
  print(Fore.YELLOW)
  #botoutput0 = "ﻮгєєՇเภﻮร єคгՇђɭเภﻮ."
  botoutput0 = "¬ŒººßæÞ§^ ºÆŒß‡|æÞ§."
  botoutput1 = "Greetings earthling.\n"
  botoutput02 = "เ кภ๏ฬ ค ɭ๏Շ เ'๓ รยקєг๒๏Շ ค๒๏ยՇ  เภ Շђє ๓ยɭՇเשєгรє єשєгץ รยקєгђєг๏."
  botoutput2 = "I'm Superbot I know alot about every superhero in the multiverse.\n"
  botoutput3 = "All I ask of you, is to type in all lowercase except for the heros name whom you are looking for."
  botoutput4 = "If you are new around here ask for help.\n\n"
  print(Fore.YELLOW)
  for char in botoutput0:
    sleep(0.01)
    print(char, end='', flush=True)
  sleep(1)
  sys.stdout.write('\033[2K\033[1G')
  sys.stdout.write(botoutput1)
  print(Style.RESET_ALL)
  for x in range (0,7):  
    b = "Syncing tranlation module " + "■" * x
    print (b, end="\r")
    time.sleep(.5)
  sys.stdout.write('\033[2K\033[1G')
  sys.stdout.write("\033[F")
  sys.stdout.write(Style.RESET_ALL)
  for x in range (0,5):  
    b = "∙" * x
    print (b, end="\r")
    time.sleep(.1)
  print('\033[2K\033[1G')
  print("\033[F")
  print(Fore.YELLOW)
  for char in botoutput02:
    sleep(0.04)
    print(char, end='', flush=True)
  sleep(1)
  sys.stdout.write('\033[2K\033[1G')
  sys.stdout.write(botoutput2)
  print(Style.RESET_ALL)
  for x in range (0,6):  
    b = "Completing dialect matching procedure " + "■" * x
    print (b, end="\r")
    time.sleep(.5)
  print('\033[2K\033[1G')
  sys.stdout.write("\033[F")
  print(Fore.YELLOW)
  for char in botoutput3:
    sleep(0.01)
    print(char, end='', flush=True)
  print(Style.RESET_ALL)
  for x in range (0,5):  
    b = "∙" * x
    print (b, end="\r")
    time.sleep(.2)
  print('\033[2K\033[1G')
  print("\033[F")
  print(Fore.YELLOW)
  for char in botoutput4:
    sleep(0.01)
    print(char, end='', flush=True)

def botprint(string):
  botresponse(string)
  print(Style.RESET_ALL)
  for x in range (0,5):  
    b = Style.DIM + "SuperBot" + Style.RESET_ALL + " is thinking" + "∙" * x
    print (b, end="\r")
    time.sleep(.2)
  sys.stdout.write('\033[2K\033[1G')
  sys.stdout.write("\033[F")
  print(Fore.YELLOW)
  for char in string:
    sleep(0.001)
    print(char, end='', flush=True)
  print(Style.RESET_ALL)

def _help_():
  botprint("This is all my creators gave me, hope it helps.")
  print(Fore.YELLOW)
  print("-------------------------HELP-----------------------------")
  print("| There are numerous ways in which you can use Super Bot!|")
  print("| You can type/enter input such as:                      |")
  print("|                                                        |")
  print("| what powers does (Heroname) have?                      |")
  print("| give me the history on a random super hero.            |")
  print("| what is (Heroname) real name?                          |")
  print("| what is (Heroname) over all score?                     |")
  print("| tell me (Heroname) combat score?                       |")
  print("| what are (Heroname) ability scores?                    |")
  print("| what teams is (HeroName) in?                           |")
  print("| where was (Heroname) born?                             |")
  print("| is (Heroname) good or evil?                            |")
  print("| where is (Heroname) base?                              |")
  print("| how tall is (Heroname)?                                |")
  print("| how much does (Heroname) weigh?                        |")
  print("| what is (Heroname) back story?                         |")
  print("| who weighs more (Heroname) or (Heroname)?              |")
  print("| start battle                                           |")
  print("| whats the latest superhero news?                       |")
  print("| superbot run diagnostics (runs all available functions)|")
  print("----------------------------------------------------------")

def didyoumean(unknown_name):
    distances =[]
    multi_name = re.compile("(.*) (\(.*\))")
    for x in range(1450):
        name = str(df_csv.at[x, 'name'])

        if multi_name.match(name):
            # extract only the name if it is formatted like this Batman (1966)
            name = multi_name.search(name).group(1)
            # print(type(name), type(temp.group(1)))

        # calculate edit distance
        ed = nltk.edit_distance(unknown_name, name)
        # store names with edit distance
        distances.append((name, ed))

    # sort array of name, edit distance tuples and get first value as a suggestion
    distances.sort(key=itemgetter(1))
    # return first value in list as suggestion
    return distances[0][0]

def whichHero(hero_list, select):
  choice = "temp"
  if len(hero_list) > 1:
    count = 0
    for i in hero_list:
      if count < 9:
        print("", count+1, ". ", i[0])
      else:
        print(count + 1, ". ", i[0])
      count+=1

    #Fix if not int, print chosen
    while re.match('[^0-9]+', choice) or (int(choice) < 1 or int(choice) > count):
      choice =input(Fore.GREEN + "\nWhich " + select + " did you mean?(1-" + str(count) + "): ")
      if re.match('^-?[0-9]', choice):
        if int(choice) < 1 or int(choice) > count:
            print("\nPlease choose a number between", 1, "and", str(count) + "!")
      else:
        print("\nThat is not a number!")

  if choice != "temp":
    return int(choice)
  else:
    return 1

def battle_1v1():
  print(Style.RESET_ALL)
  for x in range (0,6):  
    b = "Starting Battle Simulator " + "■" * x
    print (b, end="\r")
    time.sleep(.5)
  print('\033[2K\033[1G')
  sys.stdout.write("\033[F")
  botprint("*** Welcome to the Battle Simulator ***\n\n")
  multi_name = re.compile("(.*) (\(.*\))")

  #Get first hero
  hero_one_name  = input(Fore.GREEN + "Enter first hero: ")
  print(Fore.YELLOW)
  hero_one_combat = getcombatscore(hero_one_name, 1)

  #Fix in case didyoumean() executes in getinfo()
  if multi_name.match(hero_one_combat[0][0]):
    hero_one_name = multi_name.search(hero_one_combat[0][0]).group(1)

  first_choice = whichHero(hero_one_combat,hero_one_name)
  print(Fore.YELLOW)
  print("You chose " + hero_one_combat[first_choice-1][0] + " for your first hero!")

  #Get second hero
  print()
  hero_two_name = input(Fore.GREEN + "Enter second hero: ")
  print(Fore.YELLOW)
  hero_two_combat = getcombatscore(hero_two_name, 1)

  # Fix in case didyoumean() executes in getinfo()
  if multi_name.match(hero_two_combat[0][0]):
    hero_two_name = multi_name.search(hero_two_combat[0][0]).group(1)

  second_choice = whichHero(hero_two_combat,hero_two_name)
  print(Fore.YELLOW)
  print("You chose " + hero_two_combat[second_choice - 1][0] + " for your second hero!")

  #Compare combat scores
  print(Fore.RED)
  if(hero_one_combat[first_choice-1][1] > hero_two_combat[second_choice-1][1]):
    print(hero_one_combat[first_choice-1][0], "wins!")
  elif(hero_one_combat[first_choice-1][1] < hero_two_combat[second_choice-1][1]):
    print(hero_two_combat[second_choice-1][0], "wins!")
  else:
    print("After running 1 million simulations, a clear winner could not be found. " + hero_one_combat[first_choice-1][0] +  " and " + hero_two_combat[second_choice-1][0] + " remain formidable foes!")

  print(Fore.YELLOW)
  print(hero_one_combat[first_choice - 1][0], "combat score:", hero_one_combat[first_choice - 1][1])
  print(hero_two_combat[second_choice - 1][0], "combat score:", hero_two_combat[second_choice - 1][1])
  print()


# Takes in a list of tuples that have hero name and one attribute and asks the user which version of the hero the
# would like to select. use in the case multiple heroes exist for one name.
# returns tuple with data of the hero the user selected
# input list must be of the form [(hero_name_1, attribute), (hero_name_2, attribute) ... (hero_name_n, attribute)]
def selectHeroFromMultiple(hero_tup_list):
    count = 0
    choice = 0
    print(Fore.YELLOW + "\nMultiple entities exist. Please select one.")
    for i in hero_tup_list:
        if count < 9:
            print("", count + 1, ". ", i[0])
        else:
            print(count + 1, ". ", i[0])

        count += 1

    while choice < 1 or choice > count:
        choice = int(input(Fore.GREEN + "\nWhich did you mean?(1-" + str(count) + "): "))
        if choice < 1 or choice > count:
            print(Fore.GREEN + "\nPlease choose a number between", 1, "and", str(count) + "!")

    return hero_tup_list[choice - 1]


def weightcomparison(userinput):
    # extract names when input such as Who weighs more Batman or Superman is detected
    # weight_regex = re.compile(r"(.*)(weighs more)(.+)\bor\b(.+)")
    weight_regex = re.compile(r"((.*)(weighs more)(.+)\bor\b(.+))\b(.*)")
    names = weight_regex.search(userinput)

    # remove blank spaces from the start and end of hero names
    hero1 = names.group(4).strip()
    hero2 = names.group(5).strip()

    # get list of weights for the heros
    hero1_weights = getHeroWeights(hero1)
    hero2_weights = getHeroWeights(hero2)

    # if one or both lists contain multiple versions of a hero have the user select just one of them
    # before comparison
    if len(hero1_weights) > 1:
        temp = selectHeroFromMultiple(hero1_weights)
        hero1_weights.clear()
        hero1_weights.append(temp)
        # print(hero1_weights)

    if len(hero2_weights) > 1:
        temp = selectHeroFromMultiple(hero2_weights)
        hero2_weights.clear()
        hero2_weights.append(temp)
        # print(hero2_weights)

    # compare the heroes weights and display which is heavier
    weightWinner(hero1_weights, hero2_weights)


def getHeroWeights(hero_name):
    names_weights = []
    herofound = False

    for x in range(1450):
        name = str(df_csv.at[x, 'name'])

        # print(weight.split())
        if hero_name in name:
            herofound = True
            weight = str(df_csv.at[x, 'weight'])
            weight_string = weight.split()
            names_weights.append((name, weight_string[0].replace(',', '')))

    if not herofound:
        suggestion = didyoumean(hero_name)
        botprint("Did you mean " + suggestion + " instead of " + hero_name + " yes/no\n")
        userinput = input(Fore.GREEN + "> ")
        if userinput == 'yes':
            return getHeroWeights(suggestion)
        else:
            botprint("Which hero did you mean then?\n")
            userinput = input(Fore.GREEN + "> ")
            return getHeroWeights(userinput)

    return names_weights


def weightWinner(hero1, hero2):
    hero1_name = hero1[0][0]
    hero1_weight = hero1[0][1]
    hero2_name = hero2[0][0]
    hero2_weight = hero2[0][1]

    botprint("\nComparing " + hero1_name + " and " + hero2_name + "\n")
    if hero1_weight == '-' or hero2_weight == '-':
        botprint(
            "Cannot compare " + hero1_name + " " + hero1_weight + " lb and " + hero2_name + " " + hero2_weight + " lb")
    elif int(hero1_weight) > int(hero2_weight):
        botprint(hero1_name + " "+ hero1_weight + " lb weighs more than " + hero2_name + " " +hero2_weight + "lb\n")
    elif int(hero1_weight) < int(hero2_weight):
        botprint(hero2_name +" " + hero2_weight + " lb weighs more than " + hero1_name + " " + hero1_weight + "lb\n")
    else:
        botprint(hero1_name + " and " + hero2_name + " weigh the same.")
    print()

def getlatestnews():
  articles = 0
  botprint("Here is the latest superhero news from your Planet.\nClick the links if you would like to read the articles.\n")
  r = requests.get("https://www.superherohype.com/news")
  soup = BeautifulSoup(r.content, features = "lxml")

  #print(soup.prettify())

  news = soup.find_all('a')
  temp = "pingpongwallawallabingbong"
  for news in news:
    links = news.get("href")
    title = news.get('title')
    title = str(title)
    
    if articles > 3:
      botprint("Would you like to see more news?")
      userinput = userinputs()
      if userinput.find("no"):
        articles = 0
      else:
        break
    elif title.find("None") and title != temp:
      botprint(title + "\n")
      print(links + "\n")
      articles = articles + 1
    else:
      sys.stdout.write('\033[2K\033[1G')
      sys.stdout.write("\033[F")
      print("\t")
    temp = title


def userinputs():
  userinput = input(Fore.GREEN + "> ")
  inputmemory = open("memory.brain","a")
  inputmemory.write(" userinput: " + userinput + "\n")
  inputmemory.close()
  return userinput
def botresponse(string):
  inputmemory = open("memory.brain","a")
  inputmemory.write(" botresponce: " + string + "\n")
  inputmemory.close()
def functionmemory(function):
  inputmemory = open("memory.brain","a")
  inputmemory.write("\n{ \n\t _" + function + "_\n")
  inputmemory.close()

def functionmemoryclose():
  inputmemory = open("memory.brain","a")
  inputmemory.write("\n}")
  inputmemory.close()

def getnamebasic(userinput):
  if '-' in userinput:
    userinput = ''.join(re.findall(r'\b[A-Z][-a-zA-Z]+|\b[A-Z]\b', userinput))
  else: userinput = ' '.join(re.findall(r'\b[A-Z][-a-zA-Z]+|\b[A-Z]\b', userinput))

  return userinput