from player import *
from cells import *

class Dice:
    prev_dices = [] 
    @staticmethod
    def __fair_roll():
        return [np.random.choice([i for i in range(6)]) for _ in range(3)]
    
    @staticmethod
    def __unfair_roll():
        ws = [1/6] * 6
        for dice in Dice.prev_dices:
            decr = 0.5
            delta = ws[dice] * decr
            for i in range(6):
                if i == dice:
                    ws[i] -= delta
                else:
                    ws[i] = ws[i] + delta/5 
        return [np.random.choice([i for i in range(6)], p=ws) for _ in range(3)]

        
    @staticmethod
    def roll(wait=True, quiet=False, unfair=0):
        if not quiet:
            print("\tShaking...")
        if wait:
            time.sleep(3)
        else:
            time.sleep(0)
            
        if unfair == 0:
            dices = Dice.__fair_roll()
        elif unfair == 1:
            dices = Dice.__unfair_roll()
        Dice.prev_dices = dices
        
        result = [0 for _ in range(6)]
        for dice in dices:
            result[dice] += 1
            
        faces = [emoji_mapper(dice) for dice in dices]
                
        if not quiet:
            print('\t', faces)
            
        res = {
            HUOU: result[0],
            BAU: result[1],
            GA: result[2],
            CA: result[3],
            CUA: result[4],
            TOM: result[5]
        }
        
        return res
        
class Game:
    def __init__(self, n_players=1, p_money=10000, b_money=10000, *args, **kwargs) -> None:
        self.wait = True
        self.bank = b_money
        self.bot = False
        self.code = 0
        
        # Set these to True for no printing
        self.quiet = True
        self.pquiet = True
        
        if 'fast' in kwargs:
            self.wait = False
            
        if 'bot' in kwargs:
            self.bot = True
        
        if 'code' in kwargs:
            self.code = kwargs['code']
                    
        if self.bot:
            self.player = Bot("BOT", money=p_money, quiet=self.pquiet)
            if 'clever' in kwargs:
                self.player = CleverBot("CBOT", money=p_money, quiet=self.pquiet)
            elif 'not_so_clever' in kwargs:
                self.player = NotSoCleverBot("CBOT", money=p_money, quiet=self.pquiet)

        else:
            self.quiet = False
            self.pquiet = False
            pname = input(f"Player name: ")
            self.player = Player(pname, money=p_money)
            
    def print(self, value):
        if self.quiet:
            return
        print(value)
        
    def play(self):
        while True:
            # Ask player to bet
            pbet = self.player.bet()
            
            # Roll the dice
            if self.code == 0:
                dice_result = Dice.roll(wait=self.wait, quiet=self.quiet)
            elif self.code == 1:
                dice_result = Dice.roll(wait=self.wait, quiet=self.quiet, unfair=1)
            
            # The amount of money the player will lost, NOT BANK LOST
            lost = 0
            
            # Calculate, based on the rules on wikipedia
            for key, value in dice_result.items():
                if value == 0:
                    lost += pbet[key]
                if value == 1:
                    lost -= pbet[key]
                if value == 2:
                    lost -= pbet[key]*2
                if value == 3:
                    lost -= pbet[key]*3
            
            self.bank += lost
            self.print(f"Current casino left: {self.bank}")
            
            # Updates player money
            player_status = self.player.update(lost, dice_result=dice_result)
            if player_status == 0:
                self.print(f"Player {self.player.name} has lost! haha")
                break
            if self.bank <= 0:
                self.print(f"The casino is out of money, you won.")
                break
            
        return self.player.getHistory()
