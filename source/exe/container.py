# --- Function that allows NumScript to be embeded inside of .py files ---
def container(self,code):
    """
    Alternative run function that can be embeded inside of regular python files.
    It can take both single line of a code or a list of code.
    Example usage: number = container("10 01 10 30 01 05")
    """

    # --- Overwriting NSVM settings for the container to work properly ---
    self.shellOutput = False
    self.shellOutSymbol = ""

    # --- Loading code into tokenized code ---
    if isinstance(code,str):
        self.tokenizedCode.append(self.tokenizer(code))

    elif isinstance(code,list):
        for line in code:
            self.tokenizedCode.append(self.tokenizer(line))

    # --- NSVM is restarted after the code execution ---
    self.tokenizedCode.append("21")
    
    # --- Executing the code ---
    self.run()

    # --- Returning output ---

    return self.nsOut
