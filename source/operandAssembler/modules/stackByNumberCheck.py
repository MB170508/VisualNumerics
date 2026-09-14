# --- Calls a stack where its name is a number ---
def stackByNumberCheck(self):
    if self.stackByNumber not in self.stacks:
        self.stacks[self.stackByNumber] = ["00"]

    if len(self.stacks[self.stackByNumber]) == 0:
        self.stacks[self.stackByNumber] = ["00"]

    stackVariable = self.stacks[self.stackByNumber].pop()

    if stackVariable not in self.variables:
        self.variables[stackVariable] = "00"

    self.operandAssemblerOutputPart += self.variables[stackVariable]

    self.stackByNumber = ""