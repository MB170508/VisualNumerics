# --- Clean num index constructor, used in operandAssembler ---
def indexByNumberCheck(self):
    self.indexByNumber=int(self.indexByNumber)
    numbers = self.tokenize(self.operandAssemblerOutputPart)

    if 0 <= self.indexByNumber < len(numbers):
        self.operandAssemblerOutputPart = numbers[self.indexByNumber]

    else:
        if numbers:
            self.operandAssemblerOutputPart = numbers[-1]
        
        else:
            self.operandAssemblerOutputPart = "00"

    self.indexByNumber = ""