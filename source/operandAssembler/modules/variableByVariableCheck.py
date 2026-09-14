# --- Cleans var constructor, used in operandAssembler ---
def variableByVariableCheck(self):
    if self.variableByVariable not in self.variables:
        self.variables[self.variableByVariable] = "00"

    variableName = self.variables[self.variableByVariable]

    if variableName not in self.variables:
        self.variables[variableName] = "00"

    self.operandAssemblerOutputPart += self.variables[variableName]
    self.variableByVariable = ""