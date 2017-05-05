import pandas as pd
import random
import numpy as np
from termcolor import colored
import time




def getGame():
    # pull one sample from csv randomly time: 0.0122 seconds
    filename = "../data/tweets.csv"
    n = sum(1 for line in open(filename)) - 1 #number of records in file (excludes header)
    s = 1 #desired sample size
    skip = sorted(random.sample(range(1,n+1),n-s)) #the 0-indexed header will not be included in the skip list
    tweet = pd.read_csv(filename, skiprows=skip)

    #read full file then pull one randomly time : 0.0134
    # tweets = pd.read_csv('../data/tweets.csv')
    # #Get the game from twitter along with other stuff
    # ran = np.random.randint(tweets.shape[0]-1, size=1)
    # tweet = tweets.iloc[[ran[0]]]


    answer = str(tweet['text']).split()
    answer = answer[:-4]
    answer.pop(0)
    answer[0] = answer[0][2:]
    game =[]
    for words in answer:
        word = []
        for letter in words:
            if letter.isalpha():
                word.append(colored('-', 'magenta'))
            else:
                word.append(letter)
        game.append(''.join(word))
    return answer, game

def playgame():
    answer, game = getGame()
    playRounds(answer, game)

def check(answer, strikes, win, lose, guessed):
    game =[]
    correct = False
    for words in answer:
        word = []
        for letter in words:
            if letter.lower() == guessed[-1]:
                word.append(guessed[-1])
                correct = True
            elif letter.lower() in guessed:
                index = guessed.index(letter.lower())
                word.append(guessed[index])
            elif letter.isalpha():
                word.append(colored('-', 'magenta'))
            else:
                word.append(letter)
        game.append(''.join(word))
    win = True
    for word in game:
        if colored('-', 'magenta') in word:
            win = False

    if  not correct:
        print('Sorry that is incorrect')
        strikes += 'X'
    else:
        print('That was correct')
    if len(strikes) > 5:
        print('Sorry you lose :-(')
        lose = True

    return game, correct, strikes, win, lose



    # playRounds(answer, game)


def playRounds(answer, game):
    win = False
    lose = False
    guessed = []
    strikes = ''
    while not win and not lose:
        strikes, game, win, lose = playRound(answer, game, strikes, win, lose, guessed)

        print('\n')
        if win:
            print('You win great job!')



def playRound(answer, game, strikes, win, lose, guessed):
    correct = False
    print('\n')
    print(' '.join(game))
    print('Letters Guessed: ' , guessed)
    print('Strikes: ' , colored(strikes, 'red'))
    guess = input('Please enter a letter or type quit: ')
    if guess == 'quit':
        lose = True
    elif len(guess) != 1:
        print(colored('Please enter one letter', 'yellow'))
    elif guess in guessed:
        print(colored('You already guessed that letter', 'yellow'))
    else:
        guessed.append(guess)
        game, correct, strikes, win, lose = check(answer, strikes, win,lose, guessed)

    return strikes, game, win, lose






def main():
    wants_to_play = True
    playgame()
    while wants_to_play:
        play = input('Would you like to play again? y/n: ')
        if str(play) == 'y':
            playgame()
        else:
            break


if __name__ == '__main__':
    main()
