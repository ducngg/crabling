# Bầu Cua (also known as Hoo Hey How, Gourd Crab Fish Tiger, or Crabling)

Bầu Cua, also known as Hoo Hey How or Crabling, is a traditional gambling game originating from Vietnam and China. It is played with enthusiasm in various cultural settings, offering an engaging blend of luck and strategic betting.

---
## About the Game

Crabling is typically played with three dice and a betting table adorned with symbols representing six different outcomes: fish, prawn, crab, rooster, deer, and gourd (the latter may vary between cultures). Each player places their bets on the symbols that they believed to be appeared.

![Bầu Cua Game](https://upload.wikimedia.org/wikipedia/commons/f/fa/Bau_cua_ca_cop.jpg)

### How It's Played

- **Betting**: Players place their bets on the table before the dealer rolls the dice. They can wager on individual symbols or opt for combinations.

- **Rolling the Dice**: The dealer, wielding a set of special dice adorned with the game's symbols, rolls them onto the table.

  ![Bầu Cua Dice](https://upload.wikimedia.org/wikipedia/commons/4/4f/Hoo_Hey_How_Thail_03.JPG)

- **Determining the Outcome**: As the dice come to rest, players anxiously await the reveal. The payout is determined by the number of occurrences of the symbol across all three dice: 100% for one occurrence, 200% for two occurrences, and 300% for three occurrences. However, those whose bets miss will lost the money on that symbol.

For more information on Bầu Cua, you can visit the [Wikipedia page](https://en.wikipedia.org/wiki/B%E1%BA%A7u_cua_c%C3%A1_c%E1%BB%8Dp).

Your README provides a clear overview of your experiment and how to use your program. However, it could benefit from some formatting improvements and additional explanations. Here's a revised version:

---

## Experiments

In general, the dealer has an average profit of 7.9% of the betting money from players (source: [Vietnamese Wikipedia](https://vi.wikipedia.org/wiki/L%E1%BA%AFc_b%E1%BA%A7u_cua)).

I conducted experiments to investigate whether there are effective betting strategies that increase the chances of winning in the game.

There will be 3 strategies:
- Random bet.
```python
class Bot
```
- More likely to bet on the symbols that are not appeared recently.
```python
class CleverBot
```
- More likely to bet on the symbols that are appeared recently.
```python
class NotSoCleverBot
```

### Experiment settings:
```json
{
    "n_games": 500,
    "initial_money": 500,
    "each_bet": randint(10, 30),
    // Other setting values are specified in the code
}
```
### Result:

I will evaluate the performance based on the number of rounds survived by the bots before running out of money. Future iterations of this experiment will incorporate additional metrics to assess the level of "cleverness" exhibited by the bots. Below are the results:

| Bot | Rounds Survived<br>(fair dice) | Rounds Survived<br>(unfair dice) |
| - | - | - |
| Bot | 185 ± 147 | 167 ± 133 | 
| Clever Bot | 189 ± 158 | 5208 ± 2848 | 
| Not so clever Bot | 193 ± 155 | 124 ± 87 | 


## Usage

#### Normal Game (Manual Play)

To play the game manually, simply run the following command:

```bash
python crabling.py
```

#### Bot Player (Statistical Analysis)

For statistical analysis and bot gameplay, use the following command:

```bash
python crabling.py [n] [code]
```

- `n`: Number of games per bot (bot/clever bot).
- `code`: Cheat code (default is 0; choose 1 for unfair dice, which lowers the chances for cells that have appeared previously).

When using `code` as 1, the clever bot will perform better as it tends to avoid betting on cells that have recently appeared.

### Requirements

This program requires Python 3.12 or later versions(for f-string). You can download Python from the official website: [Python.org](https://www.python.org/downloads/).
