# --- Utility for operandAssembler ---        
def operandAssemblerUtility(self, to_clean):
    
    # --- to_clean defines which function is not to be ran ---   
    if to_clean != "cleanVariableByNumber" and self.variableByNumber:
        self.variableByNumberCheck()
        
    if to_clean != "cleanVariableByVariable" and self.variableByVariable:
        self.variableByVariableCheck()
        
    if to_clean != "cleanIndexByVariable" and self.indexByVariable:
        self.indexByVariableCheck()
        
    if to_clean != "cleanIndexByNumber" and self.indexByNumber:
        self.indexByNumberCheck()

    if to_clean != "cleanstackByNumber" and self.stackByNumber:
        self.stackByNumberCheck()
        
    if to_clean != "cleanstackByVariable" and self.stackByVariable:
        self.stackByVariableCheck()