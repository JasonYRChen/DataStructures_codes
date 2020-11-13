from ch5.HighScore_ch5_5.player.player import Player
from ch5.HighScore_ch5_5.score_saver.score import ScoreManagement
from random import randrange
from string import ascii_letters as al

# Test case 1
score = ScoreManagement(rank_reserve=3)
for _ in range(10):
    score.register(Player(al[randrange(0, len(al))], randrange(1, 10000)))
print('Test case 1:\n', score, '\n', sep='')

# Test case 2
score = ScoreManagement(rank_reserve=3)
players = [Player('Jason', 832), Player('Ian', 3573), Player('Lee', 923)]
for player in players:
    score.register(player)
print('Test case 2:\n', 'Original list:\n', score, '\n', sep='')
score.register(Player('Haha', 54))
print('Haha should not in the score list:\n', score, '\n', sep='')
score.register(Player('Dean', 4587))
print('Dean should be the first and Jason\'s no longer on the list:\n', score, '\n', sep='')
score.register(Player('Sean', 4089))
print('Sean should be the second and Lee\'s not on the list:\n', score, '\n', sep='')

# Test case 3
players = [Player('Jason', 832), Player('Ian', 3573), Player('Lee', 923), Player('Chris', 5467)]
score = ScoreManagement(players, 3)
print('Test case 3:\n', 'Jason should not on the board\n', score, sep='')
