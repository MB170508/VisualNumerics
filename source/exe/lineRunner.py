# --- Function that runs tokenized code in a list, used in exe ---        
def lineRunner(self, currentTokenizedCode, index):
    line = self.interpreter(currentTokenizedCode[index])

    # --- No error ---
    if line[0] != "-":
        if self.states["splitter"]:
            self.handleOutput(self.shellOutSymbol + ' '.join([line[i:i + 2] for i in range(0, len(line), 2)]))

        else:
            self.handleOutput(f"{self.shellOutSymbol}{line}")
            
    # --- Error code --
    else:
        if self.states["debug"]:
            self.handleOutput(f"{self.shellOutSymbol}{line.replace("-", "")}")

    # --- Printing tokens ---
    if self.states["printTokens"]:
        self.handleOutput(f"{self.shellOutSymbol}{currentTokenizedCode[index]}")

    # --- Printing memory ---
    if self.states["printMemory"]:
        self.handleOutput(f"{self.shellOutSymbol}{self.variables}\n{self.definitions}\n{self.stacks}")