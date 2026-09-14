# --- Importing Libraries ---
import json
import types
import os
import importlib
from pathlib import Path

rootDirectory = Path(__file__).resolve().parent

# --- NumScript Virtual Machine ---
class NumScriptVirtualMachine():
    
    # --- Setup of "Global variables" ---
    def __init__(self):
        
        # --- Defining Global variables ---
        self.math = ["++", "--", "**", "//", ">>", "<<", "==", "&&", "||", "~~"] #List of all math symbols, used in operandAssembler

        self.nsascii = {
            "00": "a", "01": "b", "02": "c", "03": "d", "04": "e", 
            "05": "f", "06": "g", "07": "h", "08": "i", "09": "j",
            "10": "k", "11": "l", "12": "m", "13": "n", "14": "o", 
            "15": "p", "16": "q", "17": "r", "18": "s", "19": "t",
            "20": "u", "21": "v", "22": "w", "23": "x", "24": "y",
            "25": "z", "26": "A", "27": "B", "28": "C", "29": "D",
            "30": "E", "31": "F", "32": "G", "33": "H", "34": "I", 
            "35": "J", "36": "K", "37": "L", "38": "M", "39": "N",
            "40": "O", "41": "P", "42": "Q", "43": "R", "44": "S",
            "45": "T", "46": "U", "47": "V", "48": "W", "49": "X",
            "50": "Y", "51": "Z", "52": "0", "53": "1", "54": "2", 
            "55": "3", "56": "4", "57": "5", "58": "6", "59": "7",
            "60": "8", "61": "9", "62": "!", "63": "\"", "64": "#",
            "65": "$", "66": "%", "67": "&", "68": "'", "69": "(",
            "70": ")", "71": "*", "72": "+", "73": ",", "74": "-", 
            "75": ".", "76": "/", "77": ":", "78": ";", "79": "<",
            "80": "=", "81": ">", "82": "?", "83": "@", "84": "[", 
            "85": "\\", "86": "]", "87": "^", "88": "_", "89": "`",
            "90": "{", "91": "|", "92": "}", "93": "~", "94": "€", 
            "95": "£", "96": "¥", "97": "¢", "98": "§", "99": " "}
        
        self.reversedNSAscii = {"a": "00", "b": "01", "c": "02", "d": "03", "e": "04",
                                "f": "05", "g": "06", "h": "07", "i": "08", "j": "09", 
                                "k": "10", "l": "11", "m": "12", "n": "13", "o": "14",
                                "p": "15", "q": "16", "r": "17", "s": "18", "t": "19",
                                "u": "20", "v": "21", "w": "22", "x": "23", "y": "24",
                                "z": "25", "A": "26", "B": "27", "C": "28", "D": "29",
                                "E": "30", "F": "31", "G": "32", "H": "33", "I": "34",
                                "J": "35", "K": "36", "L": "37", "M": "38", "N": "39",
                                "O": "40", "P": "41", "Q": "42", "R": "43", "S": "44",
                                "T": "45", "U": "46", "V": "47", "W": "48", "X": "49", 
                                "Y": "50", "Z": "51", "0": "52", "1": "53", "2": "54", 
                                "3": "55", "4": "56", "5": "57", "6": "58", "7": "59", 
                                "8": "60", "9": "61", "!": "62", """: "63", "#": "64", 
                                "$": "65", "%": "66", "&": "67", """: "68", "(": "69", 
                                ")": "70", "*": "71", "+": "72", ",": "73", "-": "74", 
                                ".": "75", "/": "76", ":": "77", ";": "78", "<": "79", 
                                "=": "80", ">": "81", "?": "82", "@": "83", "[": "84", 
                                "\\": "85", "]": "86", "^": "87", "_": "88", "`": "89", 
                                "{": "90", "|": "91", "}": "92", "~": "93", "€": "94", 
                                "£": "95", "¥": "96", "¢": "97", "§": "98", " ": "99"}

        self.indexChange = 1 #Defines if code is red from top to bottom or from bottom to top

        self.lindex = 0 #Tokenized code index, specifies which line of code is currently interpreted
        self.higherLindex = 0 #Higher tokenized code index, specifies which line of code is currently interpreted

        self.tokenizedCode = [] #Tokenized code
        self.higherTokenizedCode = [] #Tokenized code with higher priority

        self.depth = 0 #Depth when it comes to conditional statements/loops
        self.maxDepth = 0 #Max depth when it comes to conditional statements/loops

        self.variables = {} #Variable variables
        self.stacks = {} #Pointer variables
        self.definitions = {} #definitions variables

        self.currentDefinition = "" #Current definiton that is being defined

        self.loopCallback = False #Helper variable for loops

        self.nsOut = "" #List that contains print output

        # --- Importing modules ---
        with open(rootDirectory / "json" / "modulePaths.json", "r", encoding="utf-8") as modulePathsFile:
            modulesToImport = json.load(modulePathsFile)

            for modulePath, functionName in modulesToImport.items():
                module = importlib.import_module(f"source.{modulePath}")
                func = getattr(module, functionName)
                setattr(self, functionName, types.MethodType(func, self))
        
        # --- Settings of Interpreter ---
        with open(rootDirectory / "json" / "settings.json", "r", encoding="utf-8") as settings_file:
            settings = json.load(settings_file)
            
            self.states = settings["states"]

            # --- Determines if print output should be printed to shell or saved into self.nsOut ---
            self.shellOutput = settings["shellOutput"]

            # --- CLI GUI settings ---
            self.shellInSymbol = settings["symbols"]["shellIn"]

            if self.shellOutput:
                self.shellOutSymbol = settings["symbols"]["shellOut"]

            else:
                self.shellOutSymbol = ""

            self.input_symbol = settings["symbols"]["input"]

            # --- File I/O path variables ---
            self.codePath = settings["paths"]["codePath"]
            self.definitionsPath = settings["paths"]["definitionsPath"]
            self.filesPath = settings["paths"]["filesPath"]
            self.stacksPath = settings["paths"]["stacksPath"]
            self.variablesPath = settings["paths"]["variablesPath"]

            # --- Init file ---
            if settings["init"] == True: #If init is enabled, the init code is executed
                with open(rootDirectory / "1318.ns", "r", encoding="utf-8") as file:
                    importedCode = [line.rstrip('\n') for line in file]

                    for lineOfCode in importedCode:
                        lineOfCode = self.tokenizer(lineOfCode.replace(" ", ""))


                        self.tokenizedCode.append(lineOfCode)

                    self.run()

        # --- Checking if data folders exist ---
        for folder in [f"{self.codePath}/code",
                       f"{self.definitionsPath}/definitions", 
                       f"{self.filesPath}/files", 
                       f"{self.stacksPath}/stacks", 
                       f"{self.variablesPath}/variables"]:
            if not os.path.exists(f"data/{folder}"):
                os.makedirs(f"data/{folder}")