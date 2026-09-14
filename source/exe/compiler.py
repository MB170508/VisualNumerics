# --- Compiles NS code to more simple variant ---
def compiler(self, parsedTokenizedCode):

    # --- Declaring needed variables ---
    tokenizedCodeIndex = 0
    tokenizedLineIndex = 0
    skip = False

    # --- Going thru every line of code in tokenized code ---
    while tokenizedCodeIndex < len(parsedTokenizedCode):
        tokenizedLine = parsedTokenizedCode[tokenizedCodeIndex]
        tokenizedLineIndex = 0
    
        while tokenizedLineIndex < len(tokenizedLine):
            token = tokenizedLine[tokenizedLineIndex]
            
            if not skip:
                match token:
            
                    case "01"|"02"|"03"|"04"|"05"|"08"|"09":
                        skip=True
                
                    case "06"|"07":
                        return(parsedTokenizedCode)
                
                    case "25":
                        parsedTokenizedCode[tokenizedCodeIndex] = tokenizedLine[:tokenizedLineIndex]
                        parsedTokenizedCode.insert(tokenizedCodeIndex + 1, tokenizedLine[tokenizedLineIndex + 1:])
                        tokenizedLine = tokenizedLine[:tokenizedLineIndex]
                                    
            else: skip = False
        
            tokenizedLineIndex += 1
        tokenizedCodeIndex += 1
            
    return(parsedTokenizedCode)