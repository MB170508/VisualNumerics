# --- Makes sure proper token format is kept at output ---
def rounder(self, tokensToRound):
    tokensToRound = str(tokensToRound)
    if len(tokensToRound) % 2 == 1:
        return"0"+tokensToRound
    
    return(tokensToRound)