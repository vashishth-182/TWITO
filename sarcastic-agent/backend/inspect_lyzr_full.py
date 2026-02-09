import lyzr
import inspect

print("Attributes in lyzr module:")
for attr in dir(lyzr):
    if not attr.startswith("__"):
        print(f" - {attr}")

print("\n-------------------------")
try:
    from lyzr import ChatBot
    print("ChatBot found.")
    print(f"ChatBot init signature: {inspect.signature(ChatBot.__init__)}")
    print("ChatBot methods:")
    for method_name in dir(ChatBot):
        if not method_name.startswith("__"):
            method = getattr(ChatBot, method_name)
            if callable(method):
                try:
                    sig = inspect.signature(method)
                    print(f" - {method_name}{sig}")
                except:
                    print(f" - {method_name} (no signature)")
except Exception as e:
    print(f"Error inspecting ChatBot: {e}")

print("\n-------------------------")
# Check if there is a Client class
if hasattr(lyzr, 'Client'):
    print("Client class found.")
    print(f"Client init signature: {inspect.signature(lyzr.Client.__init__)}")

