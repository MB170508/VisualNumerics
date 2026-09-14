# --- Clean var index constructor, used in operandAssembler ---       
def indexByVariableCheck(self):
    numbers = self.tokenize(self.operandAssemblerOutputPart)

    if self.indexByVariable not in self.variables:
        self.variables[self.indexByVariable]= "00"

    self.indexByVariable = int(self.variables[self.indexByVariable])

    if 0 <= self.indexByVariable < len(numbers):
        self.operandAssemblerOutputPart = numbers[self.indexByVariable]

    else:
        if numbers:
            self.operandAssemblerOutputPart = numbers[-1]
            
        else:
            self.operandAssemblerOutputPart = "00"

    self.indexByVariable = ""