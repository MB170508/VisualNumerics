# --- Cleans var constructor, used in operandAssembler ---
def variableByNumberCheck(self):
    if self.variableByNumber not in self.variables:
        self.variables[self.variableByNumber] = "00"

    self.operandAssemblerOutputPart += self.variables[self.variableByNumber]

    self.variableByNumber = ""