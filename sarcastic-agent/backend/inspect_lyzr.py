import lyzr
import inspect

try:
    print("Items in lyzr module:", dir(lyzr))
    if hasattr(lyzr, 'ChatBot'):
        print("\nChatBot found.")
        print("ChatBot init signature:", inspect.signature(lyzr.ChatBot.__init__))
        print("ChatBot doc:", lyzr.ChatBot.__doc__)
    else:
        print("\nChatBot NOT found in lyzr module.")
except Exception as e:
    print(e)
