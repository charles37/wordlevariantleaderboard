import os
from signalbot import SignalBot, Command, Context
import json
#from commands import PingCommand


class PingCommand(Command):
    async def handle(self, c: Context):
        if c.message.text == "Ping":
            print(c.message)
            # Convert the context object to a string for printing and sending
            context_str = json.dumps(c.message.__dict__, indent=4, default=str)
            print(context_str)  # Print the context in the Python console

            # Send the context information back as a response in Signal
            #await c.send(f"Context:\n{context_str}")
            #await c.send("Pong")
            
            await c.reply("Pong")


if __name__ == "__main__":
    bot = SignalBot({
        "signal_service": os.environ["SIGNAL_SERVICE"],
        "phone_number": os.environ["PHONE_NUMBER"]
    })
    bot.register(PingCommand())
    bot.start()
