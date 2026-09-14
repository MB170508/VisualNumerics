# --- removes ALU symbols from a token list ---
def onlyNumbers(self,numbers):
    filteredNumbers = []

    for number in numbers:
        if number not in self.math:
            filteredNumbers.append(number)
    if filteredNumbers == []:
        return ["00"]

    return filteredNumbers