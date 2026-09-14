# --- Splits data into pairs of two  ---
def tokenize(self, data):
    return([data[i:i+2] for i in range(0, len(data), 2)]) #Returns a list of tokenized code