# --- NumScript ---

# --- Importing NumScript Virtual Machine from source ---
from source.builder import NumScriptVirtualMachine

# --- Launching the NSVM shell ---
engine = NumScriptVirtualMachine()

# --- Launching the NumScript shell ---
try:
    engine.cli()

except:
    exit()
