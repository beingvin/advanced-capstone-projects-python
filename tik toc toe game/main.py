
print("welcome to 'Tic Tac Toe' game \n")

####### ------------------------>>>>>   Global verialbles   <<<<<------------------------ #######

# Will hold our game board data
startBoard = [ "-", "-", "-",
                "-", "-", "-",
                "-", "-", "-" ]

# Lets us know if the game is over yet
gameStillOn = True

# Tells us who the winner is
winner = None

# Tells us who the current player is (X goes first)
currentPlayer = "X"

####### ------------------------>>>>>   Game Functions   <<<<<------------------------ #######

# Play a game of tic tac toe
def playGame():
    
    # Show the initial game board
    displayBoard()

    # Loop until the game stops (winner or tie)
    while gameStillOn :

        # Handle a turn
        handleTurn(currentPlayer)

        # check if the game is over 
        checkIfGameOver()

        # change to the other player
        changePlayer()

    # display game over 
    if winner == "X" or winner == "O":
        print(f'winner is "{winner}"')
    elif winner == None:
        print("Game is tie")
     


# Show the initial game board
def displayBoard ():
    print(f"\n{startBoard[0]} | {startBoard[1]} | {startBoard[2]} ")
    print(f"{startBoard[3]} | {startBoard[4]} | {startBoard[5]} ")
    print(f"{startBoard[6]} | {startBoard[7]} | {startBoard[8]}\n ")


# hadle a single turn of an arbitrary player 
def handleTurn(player):

    # Get position from player
    print(f"player {player}'s turn")
    position = input("choose a position from 1-9 : ")

    # Whatever the user inputs, make sure it is a valid input, and the spot is open
    inputValid = False

    while not inputValid:

        # Make sure the input is valid
        while position not in ["1","2","3","4","5","6","7","8","9"]:
            position = input("\nChoose a position from 1-9 : ")

        # Get correct index in our board list
        position = int(position) - 1

        # Then also make sure the spot is available on the board
        if startBoard[position] == "-":
            inputValid = True
        else:
            print("\nInvalid move !, try again !")

    # Put the game piece on the board
    startBoard[position]= player

    # Show the game board
    displayBoard()

# Check if the game is over
def checkIfGameOver ():
    checkForWinner()
    checkForTie()

# Check to see if somebody has won
def checkForWinner ():
    # global variable 
    global winner

    # check rows
    rowWinner = checkRows()    
    # check columns
    columnWinner = checkColumns()
    # check diagonals
    diagonalWinner = checkDiagonals()
    
    # Get the winner
    if rowWinner:
        winner = rowWinner
    elif columnWinner:
        winner = columnWinner
    elif diagonalWinner:
        winner = diagonalWinner
    else:
        winner = None
    return

# Check the rows for a win
def checkRows ():
      # global variable 
    global gameStillOn

    # check if any of the rows have all the same value (and is not empty)
    row1 = startBoard[0] == startBoard[1] == startBoard[2] != "-"
    row2 = startBoard[3] == startBoard[4] == startBoard[5] != "-"
    row3 = startBoard[6] == startBoard[7] == startBoard[8] != "-"

    # if any row does have a match , flag that there is a win 
    if row1 or row2 or row3:
        gameStillOn = False
    # return the winner 
    if row1:
        return startBoard[0]
    elif row2:
        return startBoard[3]
    elif row3:
        return startBoard[6]

    return

# Check the columns for a win
def checkColumns ():
    # global variable 
    global gameStillOn

    # check if any of the rows have all the same value (and is not empty)
    column1 = startBoard[0] == startBoard[3] == startBoard[6] != "-"
    column2 = startBoard[1] == startBoard[4] == startBoard[7] != "-"
    column3 = startBoard[2] == startBoard[5] == startBoard[8] != "-"

    # if any row does have a match , flag that there is a win 
    if column1 or column2 or column3:
        gameStillOn = False
    # return the winner 
    if column1:
        return startBoard[0]
    elif column2:
        return startBoard[1]
    elif column3:
        return startBoard[2]

    return

# Check the diagonals for a win
def checkDiagonals ():
    # global variable 
    global gameStillOn

    # check if any of the rows have all the same value (and is not empty)
    diagonal1 = startBoard[0] == startBoard[4] == startBoard[8] != "-"
    diagonal2 = startBoard[6] == startBoard[4] == startBoard[2] != "-"

    # if any row does have a match , flag that there is a win 
    if diagonal1 or diagonal2:
        gameStillOn = False
    # return the winner 
    if diagonal1:
        return startBoard[0]
    elif diagonal2:
        return startBoard[6]
 
    return

# Check if there is a tie
def checkForTie ():
     # global variable 
    global gameStillOn
    
    # If board is full
    if "-" not in startBoard:
        gameStillOn= False 
    return 

# change the current player from X to O, or O to X
def  changePlayer ():
    # global variable 
    global currentPlayer

    # if the current player was "X" then change it to "O"
    if currentPlayer == "X":
        currentPlayer = "O"
    # if the current player was "O" then change it to "X"
    elif currentPlayer == "O":
        currentPlayer = "X"
    
    return


####### ------------------------>>>>>   Start Execution    <<<<<------------------------ #######

# Play a game of tic tac toe
playGame()