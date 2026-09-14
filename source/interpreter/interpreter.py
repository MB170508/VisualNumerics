# --- Importing Libraries ---
import os
import json
import time
import random

# --- Runs NS functions ---
def interpreter(self, tokens):
    if tokens == []:
        return("-99")

    # --- Checks if the code is to be added to definiton ---
    if tokens[0] == "57":
        if self.currentDefinition == "":
            self.currentDefinition = "00"
            self.definitions[self.currentDefinition] = []
            
        if self.currentDefinition not in self.definitions:
            self.definitions[self.currentDefinition] = []
            
        if len(tokens[1:]) > 0:
            self.definitions[self.currentDefinition].append(tokens[1:])
        
        return("-572400")
    
    else:
        self.currentDefinition = ""
    
    # --- TAB ---
    if tokens[0] == "50":
        self.depth,index=0,0
        
        for token in tokens:
            if token == "50":
                self.depth += 1
                
            else:
                break
            
            index += 1
        tokens = tokens[index:]
        
        if self.depth > self.maxDepth:
            return("-502400")
        
        # --- If there are no tokens left -> Empty line after going thru TABS ---
        if tokens == []:
            if self.higherTokenizedCode == []:
                del self.tokenizedCode[self.lindex]
                self.lindex -= self.indexChange

            else:
                del self.higherTokenizedCode[self.higherLindex]
                self.higherLindex -= self.indexChange

            return("-502400")
        
    else:
        self.depth, self.maxDepth = 0,0
    
    # --- Checks for functions ---
    match tokens[0]:
        
        # --- Run ---
        case "00":
            builder = self.operandAssembler(tokens)
            runValue = int("".join(builder))

            if runValue >= len(self.tokenizedCode):
                runValue = -1

            self.higherTokenizedCode = [self.tokenizedCode[runValue]]
            self.higherLindex = 0

            return ("-9900")
        
        # --- Print ---
        case "10":
            return("".join(self.operandAssembler(tokens)))
        
        # --- Print in NumScript Ascii ---
        case "11":
            return("".join([self.nsascii[letter] for letter in self.tokenize("".join(self.operandAssembler(tokens)))]))
        
        # --- Define variable ---
        case "13":
            builder = self.operandAssembler(tokens)

            while len(builder)<2:
                builder.append("00")

            variableName = builder[0]
            variableValue = "".join(builder[1:])

            # --- Variable is added to variables ---
            self.variables[variableName] = str(variableValue)

            return(f"-991324{variableName}24{variableValue}")
        
        # --- Define stack ---
        case "14":
            builder = self.operandAssembler(tokens)

            while len(builder) < 2:
                builder.append("00")

            stackName,builder = builder[0],builder[1:]
            self.stacks[stackName] = []

            for variable in builder:
                if variable not in self.variables:
                    self.variables[variable] = "00"

                self.stacks[stackName].append(variable)

            return("-991424"+"".join(builder))
        
        # --- Remove variable from stack by name ---
        case "15":
            builder = self.operandAssembler(tokens)

            while len(builder) < 2:
                builder.append("00")
            
            stackName = builder[0]
            variableName = "".join(builder[1:])
            
            if stackName not in self.stacks:
                self.stacks[stackName]=[]
                return(f"-991524{stackName}")
            
            if variableName in self.stacks[stackName]:
                del self.stacks[stackName][self.stacks[stackName].index(variableName)]
                
            return(f"-991524{stackName}")
        
        # --- Remove variable from stack by index ---
        case "16":
            builder = self.operandAssembler(tokens)

            while len(builder)<2:
                builder.append("00")

            stackName = builder[0]

            index = "".join(builder[1:])

            if stackName not in self.stacks:
                self.stacks[stackName]=[]
                return(f"-991624{stackName}")

            if int(index) >= len(self.stacks[stackName]):
                index = -1

            if self.stacks[stackName] == []:
                self.stacks[stackName] = ["00"]

            del self.stacks[stackName][int(index)]

            return(f"-991624{stackName}")
        
        # --- Append to stack ---
        case "17":
            builder = self.operandAssembler(tokens)

            while len(builder)<2:
                builder.append("00")

            name = builder[0]
            builder = builder[1:]

            if name not in self.stacks:
                self.stacks[name]=[]

            for variable in builder:

                if variable not in self.stacks[name]:
                    self.stacks[name].append(variable)

            return(f"-991724{name}")
        
        # --- Merge stacks ---
        case "18":
            builder = self.operandAssembler(tokens)

            while len(builder) < 2:
                builder.append("00")

            firststack = builder[0]
            secondstack = "".join(builder[1:])

            if firststack == secondstack:
                return(f"-991824{self.stacks[firststack]}")

            if firststack not in self.stacks:
                self.stacks[firststack] = ["00"]

            if secondstack not in self.stacks:
                self.stacks[secondstack] = ["00"]

            for variable in self.stacks[secondstack]:
                if variable not in self.stacks[firststack]:
                    self.stacks[firststack].append(variable)

            del self.stacks[secondstack]

            return(f"-991824{self.stacks[firststack]}")
        
        # --- Delete stack ---
        case "19":
            stackName = "".join(self.operandAssembler(tokens))

            if stackName in self.stacks:
                del self.stacks[stackName]

            return(f"-991924{stackName}")
        
        # --- Exit ---
        case "20":
            if len(tokens) != 1:
                self.tokenCorrector()

            exit()
            
        # --- Restart ---    
        case "21":
            if len(tokens) != 1:
                self.tokenCorrector()

            os.system('cls' if os.name == 'nt' else 'clear')
            self.asciiArt()

            self.states = {"debug":False,"splitter":False,"printTokens":False,"printMemory":False}

            self.lindex = -1
            self.tokenizedCode = []

            self.higherLindex = -1
            self.higherTokenizedCode = []
 
            self.variables = {}
            self.definitions = {}
            self.stacks = {}

            return("-9921")
        
        # --- Pass/Comment ---
        case "22":
            if len(tokens) != 1:
                self.tokenCorrector()

            return("-22")
        
        # --- Changes exe to read code from top to bottom ---
        case "28":
            if len(tokens) != 1:
                self.tokenCorrector()

            self.indexChange = 1

            return("-9928")
        
        # --- Changes exe to read code from bottom to top ---
        case "29":
            if len(tokens) != 1:
                self.tokenCorrector()

            self.indexChange = -1

            return("-9929")
        
        # --- Jump ---
        case "40":
            if self.loopCallback == True:
                if self.maxDepth > 0:
                    self.maxDepth-=1

                self.loopCallback = False

            jumpValue = "".join(self.operandAssembler(tokens))

            if self.higherTokenizedCode == []:
                self.lindex = int(jumpValue)-1

            else: 
                self.higherLindex = int(jumpValue) - 1

            return(f"-994024{jumpValue}")
        
        # --- Wait ---
        case "41":
            waitValue = "".join(self.operandAssembler(tokens))

            if int(waitValue) == 0:
                waitValue = "01"

            time.sleep(int(waitValue))

            return(f"-994124{waitValue}") #Returns wait value
        
        # --- Clean console ---
        case "42":
            if len(tokens) != 1:
                self.tokenCorrector()

            os.system('cls' if os.name == 'nt' else 'clear')
            self.asciiArt()

            return("-9942")
        
        # --- Clean states ---
        case "43":
            if len(tokens) != 1:
                self.tokenCorrector()

            self.states = {"debug":False,"splitter":False,"print_tokens":False,"print_memory":False}

            return("-9943")
        
        # --- Clean tokenized code ---
        case "44":
            if len(tokens) != 1:
                self.tokenCorrector()

            self.lindex = -1
            self.tokenizedCode = []

            return("-9944")
        
        # --- Clean higher tokenized code ---
        case "45":
            if len(tokens) != 1:
                self.tokenCorrector()

            self.higherLindex = -1
            self.higherTokenizedCode = []

            return("-9945")
        
        # --- Clean variables ---
        case "46":
            if len(tokens) != 1:
                self.tokenCorrector()

            self.variables = {}

            return("-9946")
        
        # --- Clean definitions ---
        case "47":
            if len(tokens) != 1:
                self.tokenCorrector()

            self.definitions = {}

            return("-9947")
        
        # --- Clean stacks ---
        case "48":
            if len(tokens) != 1:
                self.tokenCorrector()

            self.stacks = {}

            return("-9948")
        
        # --- Switching states ---
        case "49":
            tokens = tokens[1:]

            if len(tokens) > 4:
                tokens[3] += "".join(tokens[4:])

            while len(tokens) < 4:
                tokens.append("00")

            tokenIndex = 0

            for token in tokens:
                if token not in ["00","01"]:
                    if int(token) != 0:
                        tokens[tokenIndex] = "01"

                    else:
                        tokens[tokenIndex] = "00"

                tokenIndex += 1

            keys = ["debug", "splitter", "print_tokens", "print_memory"]

            for tokenIndex, key in enumerate(keys):
                self.states[key] = tokens[tokenIndex] == "01"

            return("-49"+"".join(tokens))
        
        # --- Break ---
        case "51":
            if len(tokens) != 1:
                self.tokenCorrector()
                
            if self.depth > 0:
                self.depth -= 1

            if self.maxDepth > 0:
                self.maxDepth -= 1

            return("-9951")
        
        # --- If ---
        case "52":
            for operandAssemblerBlock in self.operandAssembler(tokens):
                if operandAssemblerBlock == "00": return("-995200")

            self.maxDepth += 1
            self.loopCallback = True

            return("-995201")
        
        # --- While loop ---
        case "53":
            for operandAssemblerBlock in self.operandAssembler(tokens):
                if operandAssemblerBlock == "00":
                    return("-995300")
                
            self.maxDepth += 1
            if self.higherTokenizedCode != []:
                tempHigherLindex = self.higherLindex

                for higherTokenizedLine in self.higherTokenizedCode[self.higherLindex:]:
                    if len(higherTokenizedLine) < self.depth+1:
                        self.maxDepth -= 1
                        break

                    higherTokenizedLine = higherTokenizedLine[self.depth+1:]

                    if higherTokenizedLine[0] == "51":
                        jumpPart = ["40","01", self.rounder(self.higherLindex)]

                        for token in range(self.depth+1):
                            jumpPart.insert(0,"50")

                        self.higherTokenizedCode[tempHigherLindex] = jumpPart

                        break

                    tempHigherLindex+=1

                self.higherTokenizedCode[self.higherLindex][self.depth] = "52"
            else:
                tempLindex = self.lindex
                for tokenizedLine in self.tokenizedCode[self.lindex:]:
                    if len(tokenizedLine) < self.depth+1:
                        self.maxDepth -= 1
                        break

                    tokenizedLine = tokenizedLine[self.depth+1:]
                    if tokenizedLine[0] == "51":
                        jumpPart = ["40","01",self.rounder(self.lindex)]

                        for token in range(self.depth+1):
                            jumpPart.insert(0,"50")

                        self.tokenizedCode[tempLindex] = jumpPart

                        break

                    tempLindex += 1

                self.tokenizedCode[self.lindex][self.depth] = "52"

            self.loopCallback = True

            return("-995301")
        
        # --- For loop ---
        case "54":
            variableName = "".join(self.operandAssembler(tokens))

            if variableName not in self.variables:
                self.variables[variableName] = "00"

            if self.variables[variableName] == "00":
                return("-995400")
            
            self.maxDepth += 1

            if self.higherTokenizedCode != []:
                tempHigherLindex = self.higherLindex

                for tokenizedLine in self.higherTokenizedCode[self.higherLindex:]:
                    if len(tokenizedLine) < self.depth+1:
                        self.maxDepth -= 1
                        break

                    tokenizedLine = tokenizedLine[self.depth+1:]

                    if tokenizedLine[0] == "51":
                        jumpPart=["40","01", self.rounder(self.higherLindex)]
                        var_define_part=["13","01",self.rounder(variableName),"24","02",self.rounder(variableName),"31","01","01"]

                        for token in range(self.depth+1):
                            jumpPart.insert(0,"50")
                            var_define_part.insert(0,"50")

                        self.higherTokenizedCode.insert(tempHigherLindex, var_define_part)
                        self.higherTokenizedCode.insert(tempHigherLindex + 1, jumpPart)

                        break

                    tempHigherLindex += 1
                ifPart = ["52","01","00","35","02",self.rounder(variableName)]

                for depth in range(self.depth):
                    ifPart.insert(0,"50")

                self.higherTokenizedCode[self.higherLindex] = ifPart

            else:
                tempLindex = self.lindex
                for higherTokenizedLine in self.tokenizedCode[self.lindex:]:
                    if len(higherTokenizedLine) < self.depth+1:
                        self.maxDepth -= 1
                        break

                    higherTokenizedLine = higherTokenizedLine[self.depth+1:]


                    if higherTokenizedLine[0]=="51":
                        jumpPart=["40","01",self.rounder(self.lindex)]
                        var_define_part=["13","01",self.rounder(variableName),"24","02",self.rounder(variableName),"31","01","01"]

                        for token in range(self.depth+1):
                            jumpPart.insert(0,"50")
                            var_define_part.insert(0,"50")

                        self.tokenizedCode.insert(tempLindex, var_define_part)
                        self.tokenizedCode.insert(tempLindex + 1, jumpPart)

                        break

                    tempLindex += 1

                ifPart = ["52","01","00","35","02",self.rounder(variableName)]

                for depth in range(self.depth):
                    ifPart.insert(0,"50")

                self.tokenizedCode[self.lindex] = ifPart

            self.loopCallback = True

            return("-995401")
        
        # --- Do if ---
        case "55":
            if self.higherTokenizedCode != []:
                self.higherTokenizedCode[self.higherLindex][0 + self.depth] = "52"

            else:
                self.tokenizedCode[self.lindex][0 + self.depth] = "52"

            return("-9955")
        
        # --- Define ---
        case "56":
            self.currentDefinition = "".join(self.operandAssembler(tokens))
            
            self.definitions[self.currentDefinition] = []
            
            return(f"-995624{self.currentDefinition}")
        
        # --- Call definition ---
        case "58":
            definitionName = "".join(self.operandAssembler(tokens))
            
            if definitionName not in self.definitions:
                self.definitions[definitionName] = []

                return("-995800")
            
            else:
                tempHigherLindex = self.higherLindex
                                    
                for line in self.definitions[definitionName]:
                    self.higherTokenizedCode.insert(tempHigherLindex + 1, line)
                    tempHigherLindex += 1
                    
                return(f"-995824{definitionName}")
            
        # --- Lambda ---    
        case "59":
            builder = self.operandAssembler(tokens)
            
            while len(builder)<2:
                builder.append("00")
            
            definitionName = builder[0]
            definitionCode = "".join(builder[1:])

            definitionCode = self.tokenize(definitionCode)
            
            self.definitions[definitionName] = [definitionCode]
            
            return(f"-99{definitionName}24{definitionCode}")
        
        # --- Load TXT ---
        case "60": 
            builder = self.operandAssembler(tokens)

            while len(builder) < 2:
                builder.append("00")

            variableName = builder[0]

            if variableName not in self.variables:
                self.variables[variableName] = "00"

            filename = "".join(builder[1:])

            if os.path.exists(f"{self.filesPath}data/files/{filename}.txt"):
                with open(f"{self.filesPath}data/files/{filename}.txt","r") as file:
                    lines = file.readlines()
                    self.variables[variableName] = ""
                    parts = []

                    for line in lines:
                        line = line.rstrip('\n')

                        for letter in line:
                            parts.append(self.reversedNSAscii.get(letter, "00"))
                            self.variables[variableName] = "".join(parts)

                    return(f"-9960{filename}")

            else: return("-996000")
        
        # --- Save TXT ---
        case "61":
            builder = self.operandAssembler(tokens)

            while len(builder) < 2:
                builder.append("00")

            variableName = builder[0]
            if variableName not in self.variables:
                self.variables[variableName]="00"

            filename = "".join(builder[1:])

            with open(f"{self.filesPath}data/files/{filename}.txt","w") as file:
                file.write(self.variables[variableName])

            return("-9961")
        
        # --- Save TXT in NumScript Ascii ---
        case "62":
            builder = self.operandAssembler(tokens)

            while len(builder) < 2:
                builder.append("00")

            variableName = builder[0]
            if variableName not in self.variables:
                self.variables[variableName] = "00"

            filename = "".join(builder[1:])

            with open(f"{self.filesPath}data/files/{filename}.txt","w") as file:
                data = ""

                for token in self.tokenize(self.variables[variableName]):
                    data += self.nsascii[token]

                file.write(data)

            return("-9962")
        
        # --- Import variables ---
        case "63":
            builder = self.operandAssembler(tokens)

            while len(builder) < 2:
                builder.append("00")

            filename = builder[0]
            variableNames = builder[1:]

            if os.path.exists(f"{self.variablesPath}data/variables/{filename}.json"):
                with open(f"{self.variablesPath}data/variables/{filename}.json","r") as file:
                    data = json.load(file)

            else: return("-996300")
            
            for variable in variableNames:

                if variable not in data:
                    data[variable] = "00"

                self.variables[variable] = data[variable]
                
            output = "24".join(variableNames)

            return(f"-9963{output}")
        
        # --- Export variables ---
        case "64":
            builder = self.operandAssembler(tokens)

            while len(builder) < 2:
                builder.append("00")

            filename = builder[0]
            variableNames = builder[1:]
            data = {}

            for variableName in variableNames:
                if variableName not in self.variables:
                    self.variables[variableName] = "00"

                data[variableName] = self.variables[variableName]

            with open(f"{self.variablesPath}data/variables/{filename}.json","w") as file:
                json.dump(data,file,indent=4)

            consoleOutput = ""

            for variableName in variableNames:
                consoleOutput += f"24{variableName}"

            return(f"-9964{consoleOutput}")
        
        # --- Import stacks ---
        case "65":
            builder = self.operandAssembler(tokens)

            while len(builder) < 2:
                builder.append("00")

            filename = builder[0]
            stackNames = builder[1:]

            if os.path.exists(f"{self.stacksPath}data/stacks/{filename}.json"):
                with open(f"data/stacks/{filename}.json","r") as file:
                    data = json.load(file)

            else: return("-996500")
            
            for stackName in stackNames:
                if stackName not in data:
                    data[stackName] = ["00"]

                self.stacks[stackName] = data[stackName]

            consoleOutput = "24"+"24".join(stackNames)

            return(f"-9965{consoleOutput}")
        
        # --- Export stacks ---
        case "66":
            builder = self.operandAssembler(tokens)

            while len(builder) < 2:
                builder.append("00")

            filename = builder[0]
            stackNames = builder[1:]
            data = {}

            for stackName in stackNames:
                if stackName not in self.stacks:
                    self.stacks[stackName]=["00"]

                data[stackName] = self.stacks[stackName]

            with open(f"{self.stacksPath}data/stacks/{filename}.json","w") as file:
                json.dump(data,file,indent=4)

            consoleOutput = "24"+"24".join(stackNames)

            return(f"-996624{consoleOutput}")
        
        # --- Import Definition --- 
        case "67":
            builder = self.operandAssembler(tokens)
            
            while len(builder) < 2:
                builder.append("00")

            filename = builder[0]
            definitionNames = builder[1:]

            if os.path.exists(f"{self.definitionsPath}data/definitions/{filename}.json"):
                with open(f"{self.definitionsPath}data/definitions/{filename}.json","r") as file:
                    data = json.load(file)

            else: return("-996700")
            
            for definitionName in definitionNames:

                if definitionName not in data:
                    data[definitionName] = []

                self.definitions[definitionName] = data[definitionName]

            consoleOutput = "24".join(definitionNames)

            return(f"-996724{consoleOutput}")
        
        # --- Export Definition ---
        case "68":
            builder = self.operandAssembler(tokens)

            while len(builder) < 2:
                builder.append("00")

            filename = builder[0]
            definitionNames = builder[1:]
            data = {}

            for definitionName in definitionNames:
                if definitionName not in self.definitions:
                    self.definitions[definitionName]=[]

                data[definitionName] = self.definitions[definitionName]

            with open(f"{self.definitionsPath}data/definitions/{filename}.json","w") as file:
                json.dump(data,file,indent=4)

            output = "24".join(definitionNames)

            return(f"-996824{output}")
        
        # --- Load NS code from other file into higher tokenized code ---
        case "69":
            filename = "".join(self.operandAssembler(tokens))

            if os.path.exists(f"{self.codePath}data/code/{filename}.ns"):
                with open(f"{self.codePath}data/code/{filename}.ns", 'r', encoding='utf-8') as file:
                    importedCode = [line.rstrip('\n') for line in file]

            else: return("-996900")
            
            tempHigherLindex = self.higherLindex

            for lineOfCode in importedCode:
                lineOfCode = self.tokenizer(lineOfCode.replace(" ",""))

                if isinstance(lineOfCode, list):
                    self.higherTokenizedCode.insert(tempHigherLindex, lineOfCode)
                    tempHigherLindex += 1
                    
            return(f"-996924{filename}")
        
        # --- Poke variables name by index ---
        case "82":
            variableIndex = int("".join(self.operandAssembler(tokens)))

            variableNames = list(self.variables.keys())

            if 0 <= variableIndex < len(variableNames):
                return (variableNames[variableIndex])

            else:
                return ("-832400")
            
        # --- Poke variable value by index ---
        case "83":
            variableIndex = int("".join(self.operandAssembler(tokens)))

            variableValues = list(self.variables.values())

            if 0 <= variableIndex < len(variableValues):
                return(variableValues[variableIndex])
                
            else:
                return("-832400")

        # --- Insert to tokenized code ---    
        case "84":
            builder = self.operandAssembler(tokens)

            while len(builder) < 2:
                builder.append("00")

            lindex = int(builder[0])
            code = builder[1:]
            line = "".join(code)

            lines = self.compiler([self.tokenize(line)])
            lines = self.compiler(lines)

            for line in lines:
                self.tokenizedCode.insert(lindex, line)
                lindex += 1

            return("-9984")
        
        # --- Insert to higher tokenized code ---
        case "85":
            builder = self.operandAssembler(tokens)

            while len(builder) < 2:
                builder.append("00")

            higherLindex = int(builder[0])
            code = builder[1:]
            line = "".join(code)

            lines = self.compiler([self.tokenize(line)])
            lines = self.compiler(lines)

            for line in lines:
                self.higherTokenizedCode.insert(higherLindex, line)
                higherLindex += 1

            return ("-9985")
        
        # --- Remove variable from variables ---
        case "86":
            variableNames = self.operandAssembler(tokens)

            for variableName in variableNames:

                if variableName in self.variables:
                    del self.variables[variableName]

            return("-9986")
        
        # --- Remove definition from variables ---
        case "87":
            definitionNames = self.operandAssembler(tokens)

            for definitionName in definitionNames:

                if definitionName in self.definitions:
                    del self.definitions[definitionName]

            return("-9987")
        
        # --- Swap variable name with value ---
        case "88":
            variableName = self.operandAssembler(tokens)

            if variableName == []:
                variableName.append("00")

            variableName = "".join(variableName)

            if variableName not in self.variables:
                self.variables[variableName]="00"

            variableValue = self.variables[variableName]
            del self.variables[variableName]
            self.variables[variableValue] = variableName

            return(f"-9988{variableValue}24{variableName}")
        
        # --- Rename variable ---
        case "89":
            builder = self.operandAssembler(tokens)

            oldVariableName = builder[0]
            newVariableName = "".join(builder[1:])

            if oldVariableName in self.variables:
                value = self.variables[oldVariableName]
                del self.variables[oldVariableName]

            else:
                value = "00"
                
            self.variables[newVariableName] = value

            return(f"-9989{newVariableName}24{value}")
        
        # --- Contains ---
        case "90":
            builder = self.operandAssembler(tokens)

            while len(builder) < 3:
                builder.append("00")

            contains = builder[0]
            variable = builder[1]

            if variable not in self.variables:
                self.variables[variable]="00"

            builder = self.tokenize("".join(builder[2:]))

            if contains in builder:
                self.variables[variable]="01"
                return("902401")
            
            else:
                self.variables[variable]="00"
                return("902400")
            
        # --- Add token by index ---    
        case "91":
            builder = self.operandAssembler(tokens)

            while len(builder) < 3:
                builder.append("00")

            variableName = builder[0]
            index = builder[1]
            builder = builder[2:]
            expansion = "".join(builder)

            if variableName not in self.variables:
                self.variables[variableName]="00"

            variableValue = self.variables[variableName]
            numbers = self.tokenize(variableValue)

            if not(0 <= int(index) < len(numbers)):
                index = -1

            numbers.insert(int(index),expansion)
            self.variables[variableName] = self.rounder("".join(numbers))

            return(f"-9991{variableName}24{variableValue}")
        
        # --- Remove token by index ---
        case "92":
            builder = self.operandAssembler(tokens)

            while len(builder)<2:
                builder.append("00")

            variableName = builder[0]
            index = "".join(builder[1:])

            if variableName not in self.variables:
                self.variables[variableName] = "00"

            variableValue = self.variables[variableName]
            numbers = self.tokenize(variableValue)

            if not(0 <= int(index) < len(numbers)):
                index = -1

            del numbers[int(index)]
            variableValue = "".join(numbers)

            if variableValue == "":
                variableValue = "00"

            variableValue = self.rounder(variableValue)
            self.variables[variableName] = variableValue

            return(f"-9992{variableName}24{variableValue}")
        
        # --- Replace ---
        case "93":
            builder = self.operandAssembler(tokens)

            while len(builder) < 4:
                builder.append("00")

            variableName = builder[0]
            originalToken = builder[1]
            newToken = builder[2]

            if variableName not in self.variables:
                self.variables[variableName]="00"

            builder = "".join(builder[3:]).replace(originalToken,newToken)
            self.variables[variableName] = builder

            return(f"-999324{builder}")
        
        # --- Replace by index ---
        case "94":
            builder = self.operandAssembler(tokens)

            while len(builder) < 3:
                builder.append("00")

            variableName = builder[0]
            index = builder[1]
            newToken = "".join(builder[2:])

            if variableName not in self.variables:
                self.variables[variableName] = "00"

            variableValue = self.tokenize(self.variables[variableName])
            
            if not(0 <= int(index) < len(variableValue)):
                index = -1

            variableValue[int(index)] = newToken
            self.variables[variableName] = "".join(variableValue)

            return(f"-999424{self.variables[variableName]}")
        
        # --- Random randint ---
        case "95":
            builder = self.operandAssembler(tokens)

            while len(builder) < 3:
                builder.append("00")

            variableName = builder[0]
            minValue = builder[1]
            maxValue = "".join(builder[2:])

            if variableName not in self.variables:
                self.variables[variableName] = "00"

            self.variables[variableName] = self.rounder(random.randint(int(minValue),int(maxValue)))

            return(f"-999524{self.variables[variableName]}")
        
        # --- Sub string (extracts part of string by start and end) ---
        case "96":
            builder = self.operandAssembler(tokens)

            while len(builder) < 3:
                builder.append("00")

            variableName = builder[0]
            startOfSubString = int(builder[1])
            endOfSubString = int("".join(builder[2:]))

            if variableName not in self.variables:
                self.variables[variableName] = "00"

            variableValue = self.variables[variableName]

            if startOfSubString > len(variableValue):
                startOfSubString = 0

            if endOfSubString > len(variableValue):
                endOfSubString = -1

            variableValue = self.tokenize(variableValue)[startOfSubString::endOfSubString]
            variableValue = "".join(variableValue)
            self.variables[variableName] = variableValue
            
            return(f"-999624{variableValue}")
        
        # --- &= -> if variable value is same as inputed value, the variable is set to 01, else 00 ---
        case "97":
            builder = self.operandAssembler(tokens)

            while len(builder) < 2:
                builder.append("00")

            variableName = builder[0]
            builder = builder[1:]
            value = "".join(builder)

            if variableName not in self.variables:
                self.variables[variableName] = "00"

            if variableName == value:
                self.variables[variableName] = "01"

            else:
                self.variables[variableName] = "00"

            return(f"-999724{self.variables[variableName]}")
        
        # --- |= -> if variable value is not same as inputed value, the variable is set to 00, else 01 ---
        case "98":
            builder = self.operandAssembler(tokens)

            while len(builder) < 2:
                builder.append("00")

            variableName = builder[0]
            value = "".join(builder[1:])

            if variableName not in self.variables:
                self.variables[variableName] = "00"

            if variableName != value:
                self.variables[variableName] = "01"

            else:
                self.variables[variableName] = "00"

            return(f"-999824{self.variables[variableName]}")
        
        # --- Project guide ---  
        case "99":
            if len(tokens) != 1:
                self.tokenCorrector()

            return("https://numscript.xyz/\n> https://github.com/skirexwastaken/NumScript")
        
        # --- Invalid function -> Line gets deleted ---
        case _:
            if self.higherTokenizedCode == []:
                del self.tokenizedCode[self.lindex]
                self.lindex -= self.indexChange

            else:
                del self.higherTokenizedCode[self.higherLindex]
                self.higherLindex -= self.indexChange

            return("-99")