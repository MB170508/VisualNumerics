# --- Function that handles output ---
def handleOutput(self,output):
    if self.shellOutput:
        print(output)

    else:
        self.nsOut = output