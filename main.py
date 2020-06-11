import superhero
import superbotdiagnostics
import sys
import time
from time import sleep
import colorama
from colorama import Fore, Style
import re

def main():
  superhero.functionmemory("_______________________________________________________________________________")
  globalinput = ""
  superhero.openingscript()

  while True:
    superhero.functionmemory("main")
    if globalinput == "":
      #userinput = input(Fore.GREEN + "> ")
      userinput = superhero.userinputs()
    else:
      userinput = globalinput
      globalinput = ""

    #REGEX MATCH VARIABLES
    realname = re.match('(.*) real name',userinput)
    historyrandomsuperhero = re.match('(.*) history|random (.*) random|history (.*)',userinput)
    heropowers = re.match('(w|W)hat powers does (.*) have',userinput)
    overall_score = re.match('(.*) overall score', userinput)
    combat_score = re.match('(.*) combat score', userinput)

    # hero_image = re.match('(.*) look like', userinput)
    # works locally but not sure about repl, dont want to mess it
    # up. Check get image function to see what i changed
    #hero_image = re.match("([wW]hat) (does) (.*) (look) (like)", userinput)

    ability_scores = re.match('(.*) ability scores', userinput)
    teams = re.match('what teams (.*)',userinput)
    birthplace = re.match('where was (.*) born',userinput)
    goodbadneutral = re.match('is (.*) (good|bad|evil)|(good or bad)|(good or evil)',userinput)
    baselocation = re.match('where is (.*) base',userinput)
    height = re.match('how tall is (.*)',userinput)
    weight = re.match('(how much does)|(what does) (.*) weigh?',userinput)
    historygivenhero = re.match('(what is (.*) backstory?)|((.*) back story on (.*))',userinput)
    battle_1v1 = re.match('start battle', userinput)
    weightcompare = re.match(r"(.*)(weighs more)(.+)\bor\b(.+)", userinput)
    latestnews = re.match('(.*) latest superhero news',userinput)
    diagnostics = re.match('(.*) run diagnostics',userinput)

    help_ = re.match('((.*)help)|(what can you do?)', userinput)
    unknowninput = re.match('(.*)',userinput)
    exit = re.match('exit', userinput)
  
    #FUNCTION TREE
    if realname:
      superhero.getrealname(userinput)
      temp = userinput
      userinput = input(Fore.GREEN + "> ")
      sameheropowers = re.match('what powers d(o|oes) (he|she|they) have',userinput)
      if sameheropowers:
        superhero.getpowers(temp)
      else:
        globalinput = userinput
    elif historyrandomsuperhero:
      superhero.getrandomhistory()
    elif heropowers:
      superhero.getpowers(userinput)
    elif overall_score:
      superhero.getoverallscore(userinput)
    elif combat_score:
      superhero.getcombatscore(userinput)
    #elif hero_image:
     #52 superhero.getimage(userinput)
    elif ability_scores:
      superhero.getscore(userinput)
    elif teams:
      superhero.getteams(userinput)
    elif birthplace:
      superhero.getbirthplace(userinput)
    elif goodbadneutral:
      superhero.getalignment(userinput)
    elif baselocation:
      superhero.getbase(userinput)
    elif height:
      superhero.getheight(userinput)
    elif weight:
      superhero.getweight(userinput)
    elif historygivenhero:
      superhero.getherohistory(userinput)
    elif battle_1v1:
      superhero.battle_1v1()
    elif weightcompare:
      superhero.weightcomparison(userinput)
    elif latestnews:
      superhero.getlatestnews()
    elif diagnostics:
      superbotdiagnostics.rundiagnostics()
    elif exit:
      print("Goodbye!")
      sys.exit(0)



    elif help_:
      superhero._help_()
    elif unknowninput:
      superhero.unknowninput()
    superhero.functionmemoryclose()

if __name__ == '__main__':
  main()