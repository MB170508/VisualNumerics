# --- Calls ta stack where its name is a value of a variable ---
def stackByVariableCheck(self):
    if self.stackByVariable not in self.variables:
        self.variables[self.stackByVariable] = "00"

    stackName = self.variables[self.stackByVariable]

    if stackName not in self.stacks:
        self.stacks[stackName] = ["00"]

    if len(self.stacks[stackName]) == 0:
        self.stacks[stackName] = ["00"]

    stackVariable = self.stacks[stackName].pop()

    if stackVariable not in self.variables:
        self.variables[stackVariable] = "00"

    self.operandAssemblerOutputPart += self.variables[stackVariable]

    self.stackByVariable = ""