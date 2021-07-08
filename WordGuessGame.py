import random
from random import randint

INITIAL_GUESSES = 8
# Generate a list with a bunch of words
wordList = []
with open('usa.txt', 'r') as file:
    for line in file:
        for word in line.split():
            wordList.append(word)

guesses = INITIAL_GUESSES
word = wordList[randint(0, len(wordList) - 1)] # Pick a word from the word list
wordArr = []
blankArr = []
for letter in word: # Append word array with each letter
    wordArr.append(letter)
for i in range(len(word)): # Append the guessed array with dashes
    blankArr.append("-")
while True:
    print("The word is:", ''.join(blankArr[0:len(blankArr)]))
    guess = (input("Guess a letter: ")).lower() # Convert all guesses to lowercase
    correct = False
    if len(guess) > 1:
        correct = True
        print("Guess should only be a single character")
        continue
    for i in range(len(blankArr)):
        if wordArr[i] == guess:
            blankArr[i] = guess
            correct = True
    if not ("-" in ''.join(blankArr[0:len(blankArr)])):
        print("You win!")
        print("The word was", word)
        break
    if correct is False:
        guesses -= 1
        if guesses == 0:
            print("You lose")
            print("The word was", word)
            break
        print("That guess is incorrect, you have", str(guesses), "guess(es) left")
    else:
        print("That guess is correct, you have", str(guesses), "guess(es) left")
