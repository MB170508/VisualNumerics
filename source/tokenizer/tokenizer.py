# --- Tokenizes code from input ---
def tokenizer(self,line):
    if isinstance(line,str):
        line = line.replace(" ","")

        # --- Checks if there are only numbers in line ---
        if line.isdigit(): 

            # --- Checks if line is in correct pair number format ---
            if len(line) % 2 != 0:
                line = self.rounder(line)

            return(self.tokenize(line))

        # --- If line is empty ---
        elif line == "":
            return(self.tokenize("00"))

        # --- If the line is not fully numerical ---
        else:
            numericalLine = ""
            
            for symbol in line:
                if symbol.isdigit():
                    numericalLine += symbol
                    
                elif symbol in self.reversedNSAscii:
                    numericalLine += self.reversedNSAscii[symbol]
                    
                else:
                    numericalLine += "00"

            return(self.tokenize(numericalLine))
    else:
        return(self.tokenize("00"))