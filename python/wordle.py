import json
import random
from collections import Counter

from termcolor import colored
import colorama

import string

# windows support
colorama.init()

NUM_GUESSES = 6

answers = None
answers_set = None
guesses_set = None

word = None
word_count = None

letter_state = Counter()
state_map = [
    'on_grey',
    'on_red',
    'on_yellow',
    'on_green',
]

def print_letter_state():
    for l in string.ascii_lowercase:
        print(colored(l, 'white', state_map[letter_state[l]]), end='')

    print()

with open('../words.json') as f:
    data = json.load(f)
    answers = data['possibleAnswers']
    answers_set = set(answers)
    guesses_set = set(data['otherGuesses'])
    
print('Welcome to Wordle')
retry_idx = input('Enter word # to try previous word, or press ENTER to start with random word.\n')

if retry_idx.isnumeric():
    idx = int(retry_idx)
    if idx > len(answers):
        print('Invalid number! Generating random word.')
        idx = random.randrange(0, len(answers))
    
    word = answers[idx]
    word_count = Counter(word)
    print(f'Word {idx} loaded')
else:
    idx = random.randrange(0, len(answers))
    word = answers[idx]
    word_count = Counter(word)
    print(f'Word {idx} loaded')


for guess_num in range(1, NUM_GUESSES + 1):
    cur_guess = ''
    while len(cur_guess) != 5 or (cur_guess not in answers_set and cur_guess not in guesses_set):
        cur_guess = input(f'Enter guess {guess_num}:\n').lower()

    res_str = ''

    l_c = Counter()

    for i, c in enumerate(cur_guess):
        if c == word[i]:
            res_str += colored(c, 'green')
            letter_state[c] = 3
            l_c[c] += 1
        elif word_count[c] > l_c[c]:
            res_str += colored(c, 'yellow')
            letter_state[c] = max(letter_state[c], 2)
            l_c[c] += 1
        else:
            res_str += colored('#', 'red')
            letter_state[c] = max(letter_state[c], 1)

    print_letter_state()

    print(res_str)

    if cur_guess == word:
        print('Congrats!')
        break
# all guesses exhausted
else:
    print('Sorry, you did not win this time!')
