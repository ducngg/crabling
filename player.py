from cells import *
        
class Command:
    def process(s):
        if s == "end":
            return 0
        if s == "check":
            return 2
        if s == "clear":
            return 3
        if s == "pray":
            return 4
        try:
            cell, money = s.split(' ')
            money = int(money)
            assert(cell in CELLS)
        except Exception:
            print("ERROR PROCESSING COMMAND, USE \'[cell] [money]\'")
            return 1
        else:
            return cell, money
        
    
class Player:
    def __init__(self, name="", money=10000, *args, **kwargs) -> None:
        self.name = name
        self.money = money
        self.betting = {}
        self.history = []
        self.quiet = False
        if 'quiet' in kwargs:
            self.quiet = True
            
    def print(self, value):
        if self.quiet:
            return
        print(value)
    
    def bet(self):
        self.clear()
        
        pre_money = self.money
                
        while True:
            cmd_result = Command.process(input(f"Player {self.name} turn. Commands: \'end\', \'check\', \'clear\', \'pray\', \'<cell> <money>\'(eg. \'{CELLS[2]} 3000\'): "))
            
            if cmd_result == 0:
                break
            
            if cmd_result == 1:
                continue
            
            if cmd_result == 2:
                self.check()
                continue
            
            if cmd_result == 3:
                self.clear()
                self.money = pre_money
                continue
                
            if cmd_result == 4:
                print("\t🪷 Nam mo a di da phat 🪷")
                continue
            
            if cmd_result[1] > self.money:
                print(f"Not enough money (current={self.money})!")
                continue
                
            if cmd_result[1] < 0:
                print(f"Can\'t bet negative value!")
                continue
            
            self.betting[cmd_result[0]] += cmd_result[1]
            self.money -= cmd_result[1]
            
        self.money = pre_money
                
        return self.betting

    
    def check(self, cell=True):
        if cell:
            for key, value in self.betting.items():
                print(f"{key}: {value}")
        self.print(f"Current money left: {self.money}")
            
    def clear(self):
        self.betting = {
            HUOU: 0,
            BAU: 0,
            GA: 0,
            CA: 0,
            CUA: 0,
            TOM: 0
        }
        self.check(cell=False)
        
    def update(self, amount, *args, **kwargs):
        """
        This function will be called by the Game instance after rolling the dice. It will update the money of the player and returns the status code.

        Parameters:
        - amount: Amount of money that LOST

        Returns:
        - 0 | 1: Status is 0 if player has no more money, else 1.
        """
        self.history.append((-amount, self.betting, kwargs['dice_result']))
        
        self.money -= amount
        if self.money <= 0:
            return 0
        else:
            return 1
    
    def getHistory(self):
        return self.history
    
class Bot(Player):
    """
    This bot will bet n times on a random cell(may bet on the same cell multiple times, and the money in that tile will add up).
    - Probability distribution of n is defined in random_times()
    """
    def __init__(self, name="", money=10000, *args, **kwargs) -> None:
        super().__init__(name, money, *args, **kwargs)
        
    def bet(self):  
        self.clear()
        n = self.random_times()
        
        pre_money = self.money
        
        for _ in range(n):
            if self.money <= 0:
                break
            cmd_result = self.random_choice()
            
            self.betting[cmd_result[0]] += cmd_result[1]
            self.money -= cmd_result[1]
        
        self.money = pre_money
        
        self.print(self.betting)
        return self.betting

    def random_times(self):
        """
        Normally, player would just bet on 1, 2 or 3 tiles maximum.
        """
        ns = [1, 2, 3, 4, 5, 6]
        ws = [0.4, 0.5, 0.1, 0, 0, 0]

        n = np.random.choice(ns, p=ws)
        return n

    def random_choice(self, low=20, high=40, ws=[1/6, 1/6, 1/6, 1/6, 1/6, 1/6]):
        money = np.random.randint(low, high)
        
        cell = np.random.choice(CELLS, p=ws)
        
        if money > self.money:
            money = self.money
        
        return cell, money
        
        
class CleverBot(Bot):
    """
    This bot will bet n times on a random cell(may bet on the same cell multiple times, and the money in that tile will add up). 
    But it can look back the history and reduce the probability of choosing the cells that just appeared recently.
    - reweight(cell, occurence) will reduce the probability of choosing the cell based on the occurence of it in recent rounds.
    """
    def __init__(self, name="", money=10000, *args, **kwargs) -> None:
        super().__init__(name, money, *args, **kwargs)
        
    def bet(self, look_back=2):  
        self.clear()
        n = self.random_times()
        ws = [1/6] * 6
        for prev_round in self.history[-look_back:]:
            dice_result = prev_round[2]
            for key, value in dice_result.items():
                ws = self.reweight(ws, index=cell_mapper(key), occurence=value)
        
        self.print(([round[2] for round in self.history[-look_back:]], ws))
        
        pre_money = self.money
        
        for _ in range(n):
            if self.money <= 0:
                break
            cmd_result = self.random_choice(ws=ws)
            
            self.betting[cmd_result[0]] += cmd_result[1]
            self.money -= cmd_result[1]
        
        self.money = pre_money
        
        self.print(self.betting)
        return self.betting
    
    def reweight(self, ws, index, occurence):
        """
        This will recude the probability of choosing a cell by X% based on the occurence.
        The reduced amount will be equally add up to other cells. 
        """
        if occurence == 0:
            pass
        
        elif occurence == 1:
            decr = 0.7
            delta = ws[index] * decr
            for i in range(6):
                if i == index:
                    ws[i] -= delta
                else:
                    ws[i] = ws[i] + delta/5 
        
        elif occurence == 2:
            decr = 0.88
            delta = ws[index] * decr
            for i in range(6):
                if i == index:
                    ws[i] -= delta
                else:
                    ws[i] = ws[i] + delta/5 
            
        elif occurence == 3:
            decr = 1
            delta = ws[index] * decr
            for i in range(6):
                if i == index:
                    ws[i] -= delta
                else:
                    ws[i] = ws[i] + delta/5 
        return ws
