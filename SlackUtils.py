from slacker import Slacker
from Config import token

slack = Slacker(token)

def print_to_slack(message):
    slack.chat.post_message("#hackaton-bot", message, 'bombila')