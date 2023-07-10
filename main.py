from src import JARVIS

bot = JARVIS()
bot.start_listening()

while True:
    command = input("Enter a command: quit, start, stop, history: ")
    if command == "quit":
        print("Terminating main thread...")
        break
    elif command == "start":
        bot.start_listening()
    elif command == "stop":
        bot.stop_listening()
    elif command == "history":
        print(bot.history)
    else:
        print("Invalid command.")

bot.stop_listening()
print("Program terminated.")