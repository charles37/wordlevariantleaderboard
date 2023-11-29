import os
import re
import requests
import json
from signalbot import SignalBot, Command, Context

class TradleScoreCommand(Command):
    async def handle(self, c: Context):
        # Check if the message is a Tradle score message
        print(c.message.raw_message['envelope']['sourceName'])
        print(c.message.text)
        print(c.message.group)
        if '#Tradle' in c.message.text and c.message.group == "HExDD/TB2/d7YYgLY1yOCdy49bPJpR7IbkuG2XwDf50=":
            # Parse the score and name
            score_match = re.search(r"#Tradle #\d+ ([X\d]+/\d+)", c.message.text)
            if score_match:
                score = score_match.group(1)
                if score.startswith('X'):
                    score = '7' + score[1:]  # Replace 'X' with '7'
                name = c.message.raw_message['envelope']['sourceName']

                                # Prepare headers for the request
                headers = {
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:113.0) Gecko/20100101 Firefox/113.0',
                    'Accept': '*/*',
                    'Accept-Language': 'en-US,en;q=0.5',
                    'Accept-Encoding': 'gzip, deflate',
                    'Referer': 'http://www.wordlevariantleaderboard.com/',
                    'Content-Type': 'application/json',
                    'Origin': 'http://www.wordlevariantleaderboard.com',
                    'Connection': 'keep-alive'
                }

                # Submit score to Flask app
                response = requests.post('http://www.wordlevariantleaderboard.com/submit', headers=headers, json={
                    'name': name,
                    'score': score
                })
                # print the full response object
                #print(response)

                response_str = json.dumps(response.__dict__, indent=4, default=str)
                print(response_str)  # Print the context in the Python console

                await c.send(f"TradleBot Submitting score {score} for {name}... visit www.wordlevariantleaderboard.com to see scores")

                if response.status_code == 201:
                    await c.reply("Score submitted successfully.")
                else:
                    await c.reply("Failed to submit score.")


if __name__ == "__main__":
    os.environ['PYTHONHTTPSVERIFY'] = '0'
    bot = SignalBot({
        "signal_service": os.environ["SIGNAL_SERVICE"],
        "phone_number": os.environ["PHONE_NUMBER"]
    })
    bot.register(TradleScoreCommand())
    bot.start()

