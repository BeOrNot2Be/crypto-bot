import telepot
from telepot.loop import MessageLoop
import sys
import time
from crypto import (
                    calculator, main_graph,
                    crypto_graph, my_wallet, 
                    )

commands_descriptions = {
            '/help_me':'it is the discription',
            '/calculator':'it is the discription',
            '/main_graph':'it is the discription',
            '/crypto_graph':'it is the discription',
            '/my_wallet':'it is the discription',
            }


def help_me(option=[]):
    if option != []:
        commands_description = commands_descriptions.get(f'/{option[0]}', None)
        if commands_description:
            return [f'/{option[0]}', commands_description]
        else:
            return ['I DON NOT KNOW THIS COMMAND!']     
    else:
        return [ f'{command_}: \n {commands_descriptions[command_]}' for command_ in commands_descriptions]


commands = {}
for command in commands_descriptions:
    commands.update([(command,command[1:])])


def handle(msg):
    chat_id = msg['chat']['id']
    command = msg['text'].split(' ') 
    print(f'Got command: {command}')
    try:
        answer = eval(f"{commands[command[0]]}(option={command[1:]})")
    except Exception as a:
        print(a)
        answer = ['I DON NOT KNOW THIS COMMAND!']
    if answer != None :#and command[0] != '/crypto_graph':
        for i in answer:        
            bot.sendMessage(chat_id, i)
    #elif command[0] == '/crypto_graph':
    #    print(answer)
    #    with open(answer, 'rb') as p:
    #        bot.sendPhoto(chat_id, p)        
    else:
        bot.sendMessage(chat_id, 'I don not know what I have \nSorry, man')

bot = telepot.Bot('505055599:AAGYm9AE106_FYkxf7kmMH-EMuffUZiRE3c')
MessageLoop(bot, handle).run_as_thread()
print ('Listening ...')

while 1:
    time.sleep(10)