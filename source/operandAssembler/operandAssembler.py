# --- Importing Libraries ---
import sys
import random
import re
from datetime import datetime

# --- This could be best described as: It works. ---
sys.set_int_max_str_digits(1_000_000_000)

# --- Analyses code, used in most NS functions ---    
def operandAssembler(self,tokens):

    # --- Declaring variables used in operandAssembler ---
    skip = False
    index = 0
    tokens = tokens[1:]
    
    # --- The idea here is that a buffer is added at the start so in case there's for example 01 at the end of the line the operandAssembler won't crash ---
    tokensLength = len(tokens)
    tokens.append("00")
    
    deleted = 0
    
    self.operandAssemblerOutputPart = ""
    self.operandAssemblerOutput = []

    self.variableByNumber = ""
    self.variableByVariable = ""

    self.indexByNumber = ""
    self.indexByVariable = ""

    self.stackByNumber = ""
    self.stackByVariable = ""

    # --- Building print value ---
    for token in range(tokensLength):
        
        # --- Skip is used to distinguish between pair and non pair tokens ---
        if not skip:

            # --- Match used to grab the current token ---    
            match tokens[index]:
            
                # --- Checking for number ---
                case"01":
                    self.operandAssemblerUtility(None)

                    self.operandAssemblerOutputPart+=tokens[index + 1]
                    skip=True

                # --- Checking for variable ---    
                case"02":
                    self.operandAssemblerUtility("cleanVariableByNumber")
                    
                    self.variableByNumber+=tokens[index + 1]
                    skip=True

                # --- Checking for variable with name being variable value ---
                case"03":
                    self.operandAssemblerUtility("cleanVariableByVariable")

                    self.variableByVariable += tokens[index + 1]
                    skip=True

                    # --- Grabs item by num index from the existing code ---    
                
                case"04":
                    self.operandAssemblerUtility("cleanIndexByNumber")

                    self.indexByNumber += tokens[index + 1]
                    skip=True

                # --- Grabs item by var index from the existing code ---    
                case"05":
                    self.operandAssemblerUtility("cleanIndexByVariable")

                    self.indexByVariable +=tokens[index + 1]
                    skip=True

                # --- Rest is num ---    
                case"06":
                    self.operandAssemblerUtility(None)

                    tokens=tokens[index+1:]
                    self.operandAssemblerOutputPart += "".join(tokens[:-1])
                    break

                # --- Rest is var ---
                case"07":
                    self.operandAssemblerUtility(None)

                    tokens=tokens[index+1:]
                    self.variableByNumber += "".join(tokens[:-1])
                    break

                # --- Call stack with num value ---
                case"08":
                    self.operandAssemblerUtility("cleanstackByNumber")

                    self.stackByNumber += tokens[index + 1]
                    skip=True

                # --- Call stack with var value ---
                case"09":
                    self.operandAssemblerUtility("cleenstackByVariable")

                    self.stackByVariable += tokens[index + 1]
                    skip=True

                # --- Input ---    
                case"12":
                    self.operandAssemblerUtility(None)

                    self.operandAssemblerOutputPart += "".join(self.tokenizer(input(self.input_symbol).replace(" ","")))

                # --- Comment ---        
                case"22":
                    break

                # --- Checking for split between variable/variable ---            
                case"23":
                    self.variableByNumberCheck()

                # --- Checking for split between parts ---
                case"24":
                    self.operandAssemblerUtility(None)

                    self.operandAssemblerOutput.append(self.operandAssemblerOutputPart)
                    self.operandAssemblerOutputPart = ""

                # --- Adds day/month/year ---
                case"26":
                    self.operandAssemblerUtility(None)

                    now=datetime.now()
                    self.operandAssemblerOutputPart += self.rounder(now.day) + self.rounder(now.month) + self.rounder(now.year)

                # --- Adds hour/minute ---   
                case"27":
                    self.operandAssemblerUtility(None)

                    now=datetime.now()
                    self.operandAssemblerOutputPart += self.rounder(now.hour) + self.rounder(now.minute)

                # --- Checking for math logic ---
                case"30"|"31"|"32"|"33"|"34"|"35"|"36"|"37"|"38"|"39":    
                    self.operandAssemblerUtility(None)

                    self.operandAssemblerOutputPart += {"30": "++", "31": "--", "32": "**", "33": "//", "34": ">>", "35": "<<", "36": "==", "37": "&&", "38": "||", "39": "~~"}[tokens[index]]
            
                # --- Min ---
                case"70":
                    self.operandAssemblerUtility(None)
                
                    if self.operandAssemblerOutputPart == "":
                        self.operandAssemblerOutputPart = "00"

                    numbers = self.tokenize(self.operandAssemblerOutputPart)

                    self.operandAssemblerOutputPart = str(min(self.onlyNumbers(numbers)))

                # --- Max ---    
                case"71":
                    self.operandAssemblerUtility(None)

                    if self.operandAssemblerOutputPart == "":
                        self.operandAssemblerOutputPart = "00"

                    numbers = self.tokenize(self.operandAssemblerOutputPart)

                    self.operandAssemblerOutputPart = str(max(self.onlyNumbers(numbers)))

                # --- Average ---    
                case"72":
                    self.operandAssemblerUtility(None)

                    if self.operandAssemblerOutputPart == "":
                        self.operandAssemblerOutputPart = "00"

                    numbers = self.tokenize(self.operandAssemblerOutputPart)
                    total = sum(map(int, self.onlyNumbers(numbers)))
                    self.operandAssemblerOutputPart = self.rounder(total // len(numbers))

                # --- Sum ---   
                case"73":
                    self.operandAssemblerUtility(None)

                    if self.operandAssemblerOutputPart == "":
                        self.operandAssemblerOutputPart = "00"
                        
                    numbers = self.onlyNumbers(self.tokenize(self.operandAssemblerOutputPart))

                    total = 0

                    for number in numbers:
                        total += int(number)

                    self.operandAssemblerOutputPart = self.rounder(total)

                # --- Len ---    
                case"74":
                    self.operandAssemblerUtility(None)

                    self.operandAssemblerOutputPart = self.rounder(len(self.operandAssemblerOutputPart) // 2)

                # --- Sort ---    
                case"75":
                    self.operandAssemblerUtility(None)

                    if self.operandAssemblerOutputPart == "":
                        self.operandAssemblerOutputPart = "00"

                    numbers = self.tokenize(self.operandAssemblerOutputPart)
                    numbers.sort()
                    self.operandAssemblerOutputPart = "".join(numbers)

                # --- Any ---    
                case"76":
                    self.operandAssemblerUtility(None)

                    if self.operandAssemblerOutputPart == "":
                        self.operandAssemblerOutputPart = "00"

                    numbers = self.tokenize(self.operandAssemblerOutputPart)
                    self.operandAssemblerOutputPart = random.choice(self.onlyNumbers(numbers))

                # --- All Same ---
                case"77":
                    self.operandAssemblerUtility(None)

                    if self.operandAssemblerOutputPart == "":
                        self.operandAssemblerOutputPart = "00"

                    numbers = self.tokenize(self.operandAssemblerOutputPart)
                    
                    if all(x == numbers[0] for x in numbers): 
                        self.operandAssemblerOutputPart = "01"
                        
                    else:
                        self.operandAssemblerOutputPart = "00"

                # --- Random ---    
                case"78":
                    self.operandAssemblerUtility(None)

                    if self.operandAssemblerOutputPart == "":
                        self.operandAssemblerOutputPart = "00"

                    numbers = self.onlyNumbers(self.tokenize(self.operandAssemblerOutputPart))


                    self.operandAssemblerOutputPart = self.rounder(random.randint(int(min(numbers)), int(max(numbers))))

                # --- Most Common ---
                case"79":
                    self.operandAssemblerUtility(None)

                    if self.operandAssemblerOutputPart == "":
                        self.operandAssemblerOutputPart = "00"

                    self.operandAssemblerOutputPart = self.mostCommon(self.tokenize(self.operandAssemblerOutputPart))

                # --- Shuffle ---    
                case"80":
                    self.operandAssemblerUtility(None)

                    if self.operandAssemblerOutputPart == "":
                        self.operandAssemblerOutputPart = "00"

                    numbers = self.tokenize(self.operandAssemblerOutputPart)
                    random.shuffle(numbers)
                    self.operandAssemblerOutputPart = "".join(numbers)

                # --- Reverse ---    
                case"81":
                    self.operandAssemblerUtility(None)

                    if self.operandAssemblerOutputPart == "":
                        self.operandAssemblerOutputPart = "00"

                    numbers = self.tokenize(self.operandAssemblerOutputPart)
                    numbers.reverse()
                    self.operandAssemblerOutputPart = "".join(numbers)
            
                case _:
                    if self.higherTokenizedCode == []:
                        del self.tokenizedCode[self.lindex][index + 1 + self.depth - deleted]
                        deleted += 1

                    else:
                        del self.higherTokenizedCode[self.higherLindex][index + 1 + self.depth - deleted]
                        deleted += 1

        else: skip = False

        index += 1
    
    self.operandAssemblerUtility(None)
    index = 0

    if self.operandAssemblerOutputPart != "":
        self.operandAssemblerOutput.append(self.operandAssemblerOutputPart)#If output value is not "", it will be added to output

    for self.operandAssemblerOutputPart in self.operandAssemblerOutput:#Checks for math in each part

        if any(symbol in self.operandAssemblerOutputPart for symbol in self.math):#Checking for math
            self.operandAssemblerOutputPart = self.operandAssemblerOutputPart.replace("++", "+").replace("--", "-").replace("**", "*").replace(">>", ">").replace("<<", "<").replace("&&", "&").replace("||", "|").replace("~~", "~")#The math logic returns to its normal state
        
            try:#Tries to run math
                self.operandAssemblerOutputPart = eval(re.sub(r'\b0+(\d+)', r'\1', self.operandAssemblerOutputPart))#If math is found, it will try eval with removing excess 0

                if self.operandAssemblerOutputPart < 0:
                    self.operandAssemblerOutputPart *= -1 #ABS is applied as anything less than 0 doesn't exist :)

                if self.operandAssemblerOutputPart == True:
                    self.operandAssemblerOutputPart = "01"

                if self.operandAssemblerOutputPart == False:
                    self.operandAssemblerOutputPart = "00"

            except:
                self.operandAssemblerOutputPart = None #If there's an error it will return empty string

        if self.operandAssemblerOutputPart:
            self.operandAssemblerOutput[index] = self.rounder(self.operandAssemblerOutputPart)

        else:
            del self.operandAssemblerOutput[index]
    
        index += 1
        
    if self.operandAssemblerOutput == []:
        self.operandAssemblerOutput = ["00"]
        
    return(self.operandAssemblerOutput) #Returns print value
