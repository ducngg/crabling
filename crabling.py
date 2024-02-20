'''
Usage: 
Normal player:
    python crabling.py
Bot player:
    python crabling.py [n] [code]
    
    with
    - n is the number of games per bot (bot/clever bot)
    - code is the cheat code (default 0, choose 1 for unfair dices(lower chances for the cells those have appeared previously))

** With code is 1, clever bot will perform better because it tends to prevent bet on the cells that appeared recently

'''
import sys
import statistics
from player import *
from game import *
        
if __name__ == '__main__':
    
    # Bot simulation
    if len(sys.argv) > 1:
        n = int(sys.argv[1])
        if len(sys.argv) > 2:
            code = int(sys.argv[2])
        else:
            code = 0
    
    # Normal game (played manually)
    else:
        game = Game(p_money=500, b_money=1000)
        history = game.play()
        sys.exit()
    
    bot_records = []
    clever_bot_records = []
    
    for i in range(n):
        print(f"\rBot: {i+1}/{n}", end='')
        start_time = time.time()
        game = Game(p_money=500, b_money=1000, bot=True, fast=True, code=code)
        history = game.play()
        end_time = time.time()
        bot_records.append((len(history), end_time-start_time))
    print('\n')
    
    for i in range(n):
        print(f"\rClever Bot: {i+1}/{n}", end='')
        start_time = time.time()
        game = Game(p_money=500, b_money=1000, bot=True, fast=True, clever=True, code=code)
        history = game.play()
        end_time = time.time()
        clever_bot_records.append((len(history), end_time-start_time))
        
    print('\n')
        
    print(f"MEAN BOT ITER: {statistics.mean([record[0] for record in bot_records])}")
    print(f"STD BOT ITER: {statistics.stdev([record[0] for record in bot_records])}")
    print('\n')
    print(f"MEAN CBOT ITER: {statistics.mean([record[0] for record in clever_bot_records])}")
    print(f"STD CBOT ITER: {statistics.stdev([record[0] for record in clever_bot_records])}")
