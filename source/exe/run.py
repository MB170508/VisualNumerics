# --- Runs code in tokenized and higer tokenized variables --- 
def run(self):
    # --- Removing THEN from tokenized code ---
    self.tokenizedCode = self.compiler(self.tokenizedCode)
    
    """
    The idea here is that tokenized code has lower priority than higher tokenized code.
    The reason behind this is that for example called function needs to be executed instantly so its added to higher tokenized cody which has higher priority.
    """

    # --- Running tokenized code --- 
    while self.lindex < len(self.tokenizedCode):
        
        # --- Line is passed to line_runner ---
        self.lineRunner(self.tokenizedCode, self.lindex)
        
        # --- If index change is valid ---
        if self.lindex+self.indexChange >= 0:
            self.lindex+=self.indexChange

        # --- If the index change would lead to selecting line before 0 or after end of file, the execution of tokenized code is stopped ---
        else:
            self.lindex=len(self.tokenizedCode)

        # --- Checking if higher tokenized code is not empty ---
        if self.higherTokenizedCode != []:

            # --- Removing THEN from higher tokenized code ---
            self.higherTokenizedCode = self.compiler(self.higherTokenizedCode)

            # --- Running higher tokenized code ---
            while self.higherLindex != len(self.higherTokenizedCode):

                # --- Line is passed to line runner ---
                self.lineRunner(self.higherTokenizedCode, self.higherLindex)

                # --- If index change is valid ---
                if self.higherLindex + self.indexChange >= 0:
                    self.higherLindex += self.indexChange

                # --- If the index change would lead to selecting line before 0 or after end of file, the execution of higher tokenized code is stopped ---
                else:
                    self.higherLindex = len(self.higherTokenizedCode)

            # --- After all of higher tokenized code is executed the variables tied to running it are set to their default values ---
            self.higherTokenizedCode = []
            self.higherLindex = 0
            
    # --- Setting variables tied to code running to their default values ---        
    self.tokenizedCode = []
    self.lindex = 0
    self.maxDepth = 0
    self.depth = 0  