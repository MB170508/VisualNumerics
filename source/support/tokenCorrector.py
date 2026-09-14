# --- Corrects wrong tokens  ---
def tokenCorrector(self):
    if self.higherTokenizedCode:
        line = self.higherTokenizedCode[self.higherLindex]
        self.higherTokenizedCode[self.higherLindex] = line[:-len(line) + self.depth + 1]

    else:
        line = self.tokenizedCode[self.lindex]
        self.tokenizedCode[self.lindex] = line[:-len(line) + self.depth + 1]