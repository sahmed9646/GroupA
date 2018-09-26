
import getpass #import getpass to hide user input
import random

# Project imports
import console
import player

## -------------------------------------------------------------------------- ##
## RPS
## -------------------------------------------------------------------------- ##

"""
"""
def player_choice(player, choice):  # Register and shows the second player choice
    if choice == 1:
        print(player.name + " chose rock")
    elif choice == 2:
        print(player.name + " chose paper")
    else:
        print(player.name + " chose scissors")

"""
"""
def result(player0, player1, player0_choice, player1_choice):
    if player0_choice == player1_choice:
        print("Both Of Player Choose Same")
        return 0.5
    elif player0_choice == 1 and player1_choice == 3:
        print(player0.name + " win and can smash " + player1.name,)
        return 1
    elif player0_choice == 2 and player1_choice == 1:
        print(player0.name + " win and can cover " + player1.name,)
        return 1
    elif player0_choice == 3 and player1_choice == 2:
        print(player0.name + " win and can cut " + player1.name,)
        return 1
    elif player1_choice == 1 and player0_choice == 3:
        print(player1.name + " win and can smash " + player0.name,)
        return 0
    elif player1_choice == 2 and player0_choice == 1:
        print(player1.name + " win and can cover " + player0.name,)
        return 0
    else:
        print(player1.name + " win and can cut " + player0.name, )
        return 0

"""
"""
def getChoice(player):
    done = False
    choiceNum = 1
    while not done:
        choice = getpass.getpass(player.name + " please make a choice: ")
        if choice.lower() == "q":
            exit()
        try:
            choiceNum = int(choice)
            if choiceNum not in range(1,4):
                console.write("Only numbers 1-3 are accepted")
            else:
                done = True
        except:
            console.write("Only numbers 1-3 are accepted")
    return choiceNum

"""
"""
def playRPS(player0, player1):
    # Return a random number if both players are ai
    if player0.difficulty != player.PlayerDifficulty.HUMAN and player1.difficulty != player.PlayerDifficulty.HUMAN:
        return random.choice([1, 0])

    # Print alternatives
    console.write(console.coloredText("[1] Rock", console.BLUE))
    console.write(console.coloredText("[2] Paper", console.GREEN))
    console.write(console.coloredText("[3] Scissor", console.RED))
    console.write(console.coloredText("[q] Scissor", console.MAGENTA))

    # Let players0 make their choice
    if player0.difficulty == player.PlayerDifficulty.HUMAN:
        choicePlayer0 = getChoice(player0)
    else:
        choicePlayer0 = random.choice([1,2,3])

    # Let players0 make their choice
    if player1.difficulty == player.PlayerDifficulty.HUMAN:
        choicePlayer1 = getChoice(player1)
    else:
        choicePlayer1 = random.choice([1,2,3])

    # Present choices
    player_choice(player0, choicePlayer0)
    player_choice(player1, choicePlayer1)

    # Return the result
    r = result(player0, player1, choicePlayer0, choicePlayer1)
    if r == 0.5:
        return playRPS(player0, player1)
    return r
