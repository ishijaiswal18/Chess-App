import chessEngine
import chess
import time
import pygame as py


"""Variables"""
WIDTH = HEIGHT = 512  # width and height of the chess board
DIMENSION = 8  # the dimensions of the chess board
SQ_SIZE = HEIGHT // DIMENSION  # the size of each of the squares in the board
MAX_FPS = 15  # FPS for animations
IMAGES = {}  # images for the chess pieces
colors = [py.Color("white"), py.Color("maroon")]
PADDING = 10  # padding between the piece and the sqaure
PIECES = ['white_r', 'white_n', 'white_b', 'white_q', 'white_k', 'white_p',
              'black_r', 'black_n', 'black_b', 'black_q', 'black_k', 'black_p']


def takeUserInput(screen):
    """Takes the user input"""
    # background color of the screen
    # screen.fill(py.Color("#E6E6FA"))

    # set the background image to the screen
    py.display.set_caption("Chess")
    bg = py.image.load("image.jpg")

    
    # set the background image to the screen
    screen.blit(bg, (0.2*WIDTH, 0))

    


    #  draw the input box
    inputBox = py.draw.rect(screen, py.Color("white"), (0.1*WIDTH, 0.4*HEIGHT, 0.8*WIDTH, 0.2*HEIGHT))
    
    #  draw the text
    font = py.font.SysFont("comicsansms", 20)
    text = font.render("Enter the color you want (Black / White) : ", True, py.Color("red"))
    screen.blit(text, (0.1*WIDTH, 0.4*HEIGHT))
    
    # create submit button
    submit = py.draw.rect(screen, py.Color("green"), (0.4*WIDTH, 0.7*HEIGHT, 0.2*WIDTH, 0.07*HEIGHT))
    text = font.render("Submit", True, py.Color("black"))
    screen.blit(text, (0.42*WIDTH, 0.7*HEIGHT))
    
    # set the box to be active
    active = False
    userInput = ""
    running = True

    #  get the user input
    color = "white"
    border = "white"
    while running:

        # scroll through the events
        
        for e in py.event.get():

            # if the user quits
            if e.type == py.QUIT:
                running = False
                return

            # if the user clicks
            if e.type == py.MOUSEBUTTONDOWN:

                if e.button == 1:
                    #  get the mouse position
                    pos = py.mouse.get_pos()

                    #  check if the mouse is in the submit button
                    if submit.collidepoint(pos):
                        running = False
                        break
                    
                    # check if the mouse is in the input box
                    if inputBox.collidepoint(pos):
                        # make a cursor appear
                        # py.mouse.set_visible(False)
                        # highlight the box with a blue color and set the active variable to true
                        
                        color = "#E6E6FA"
                        border = "green"
                        active = True
                    else:
                        color = "white"
                        border = "white"
                        active = False
            
            # if the user types
            if e.type == py.KEYDOWN:

                # if the user types a letter
                if active:

                    # if the user types a enter key
                    if e.key == py.K_RETURN:
                        running = False
                        break

                    # if the user types a backspace key
                    elif e.key == py.K_BACKSPACE:
                        userInput = userInput[:-1]

                    # if the user types a letter
                    else:
                        userInput += e.unicode

        # draw the input box
        py.draw.rect(screen, py.Color(color), inputBox)

        # draw border of the input box
        py.draw.rect(screen, py.Color(border), inputBox, 2)

        #  draw the text
        font = py.font.SysFont("comicsansms", 20)
        text = font.render("Enter the color you want (Black / White) : ", True, py.Color("red"))
        screen.blit(text, (0.1*WIDTH, 0.4*HEIGHT))

        # draw the text
        text2 = font.render(userInput, True, py.Color("black"))

        # draw the text
        screen.blit(text2, (0.1*WIDTH, 0.5*HEIGHT))

        # if active is true, draw the cursor
        if active:
            py.draw.rect(screen, py.Color("black"), (0.112*WIDTH + len(userInput) * 7 , 0.51*HEIGHT, 2, 20))


        # update the screen
        py.display.update()

    # return the user input
    return userInput

def loadImages():
    '''
    Load images for the chess pieces
    '''

    for p in PIECES:
        IMAGES[p] = py.transform.scale(py.image.load("images/" + p + ".png"), (SQ_SIZE - 10, SQ_SIZE - 10))


def drawPieces(screen):
    """Draws the pieces on the board"""
    myBoard = [i.split() for i in str(game.board).split('\n')]
    for i in range(DIMENSION):
        for j in range(DIMENSION):
            
            if myBoard[i][j] != '.':
                
                piece = myBoard[i][j]
                img = None

                # if the piece is in lowercase, it is black
                if piece.islower():
                    img = IMAGES['black_' + piece.lower()]
                else:
                    img = IMAGES['white_' + piece.lower()]
                    
                screen.blit(img, (j * SQ_SIZE + PADDING/2, i * SQ_SIZE + PADDING/2))

def drawHighlight(screen, pos, color):
    """Draws the highlight on the square"""
    s = py.Surface((SQ_SIZE, SQ_SIZE))
    s.set_alpha(200)
    s.fill(py.Color(color))
    screen.blit(s, (pos[0] * SQ_SIZE, pos[1] * SQ_SIZE))

   

def drawHighlights(screen, sqaure_selected):

    if len(sqaure_selected) != 2:
        return

    """Draws the highlights on the squares"""
    for i in range(DIMENSION):
        for j in range(DIMENSION):
            
            moveStart = sqaure_selected[0] + (7 - sqaure_selected[1])*8 # the starting position of the move
            moveEnd = (i + (7 - j)*8) # the ending position of the move




            if game.board.is_legal(chess.Move(moveStart, moveEnd)):
                drawHighlight(screen, (i, j), color="green")
    
    drawHighlight(screen, sqaure_selected, color="red")

def drawBoard(screen):
    """Draws the chess board"""
    for i in range(DIMENSION):
        for j in range(DIMENSION):
            py.draw.rect(screen, colors[(i + j) % 2], (j * SQ_SIZE, i * SQ_SIZE, SQ_SIZE, SQ_SIZE))

def startGame():
    """Starts the game"""
    global game
    game = chessEngine.chessEngine()

    
    # draw the board
    py.init()
    clock = py.time.Clock()
    screen = py.display.set_mode((WIDTH, HEIGHT))
    humanPlayer = takeUserInput(screen)[0].lower()
    running = True
    square_selected = ()  # keeps track of the last selected square
    player_clicks = []  # keeps track of player clicks (two tuples)
    valid_moves = []
    loadImages()
    game_over = False
    
    move_cnt = 0

    if humanPlayer == 'b':
        game.makeMove()
        move_cnt += 1
    

    while running:

        for e in py.event.get():
            if e.type == py.QUIT:
                running = False

            if e.type == py.MOUSEBUTTONDOWN:
                
                if e.button == 1:
                    pos = py.mouse.get_pos()
                    i = pos[0] // SQ_SIZE
                    j = pos[1] // SQ_SIZE
                    
                    if square_selected == (i, j):
                        square_selected = ()
                        player_clicks = []
                    else:
                        square_selected = (i, j)
                        player_clicks.append(square_selected)
                    

                    if len(player_clicks) == 2  and (humanPlayer == 'b' and move_cnt%2 == 1 or humanPlayer == 'w' and move_cnt%2 == 0):
                        
                        moveStart = player_clicks[0][0] + (7 - player_clicks[0][1])*8 # the starting position of the move
                        moveEnd = player_clicks[1][0] + (7 - player_clicks[1][1])*8 # the ending position of the move

                        if game.board.is_legal(chess.Move(moveStart, moveEnd)):
                            game.board.push(chess.Move(moveStart, moveEnd))
                            
                            # print("last move" ,last_mv)
                            move_cnt += 1
                            # print("Move: ", move_cnt)
                        else:
                            print("Illegal move ", chess.Move(moveStart, moveEnd))

                        player_clicks = []
                        square_selected = ()
        if move_cnt > 0:

            last_mv = (game.board.peek().to_square%8 , 7 - game.board.peek().to_square//8 )

        if not (humanPlayer == 'b' and move_cnt%2 == 1 or humanPlayer == 'w' and move_cnt%2 == 0):

            drawBoard(screen)
            drawHighlights(screen, square_selected)
            drawHighlight(screen, last_mv, color="yellow")
            drawPieces(screen)
            py.display.update()

            game.makeMove()
            # print("pc move", mv)
            move_cnt += 1
            
            #  convert mv to a tuple
            # last_mv = (mv.to_square//8 + 1, mv.to_square%8 + 1)
            # print("updtaed Move: ", mv)
            # drawHighlight(screen, mv, color="red")
            # py.display.update()
        # time.sleep(1) 
        # print("move ---- > ", game.board.peek().to_square)
        if move_cnt > 0:
            last_mv = (game.board.peek().to_square%8 , 7 - game.board.peek().to_square//8 )
        # print("last move" ,last_mv)
        # time.sleep(0.4)
        
        # py.display.update()
        drawBoard(screen)
        drawHighlights(screen, square_selected)
        if move_cnt > 0:
            drawHighlight(screen, last_mv, color="yellow")
        drawPieces(screen)

        if game.isCheckmate() != 0:
            running = False
            game_over = True
            winner = game.isCheckmate()
            print("Checkmate")
            if winner > 0:
                print("Black wins")
            else:
                print("White wins")

            break

        if game.isStalemate() != 0:
            running = False
            game_over = True
            winner = game.isStalemate()
            print("Stalemate")
            if winner > 0:
                print("Black wins")
            else:
                print("White wins")
            
            break

        # pause the screen until the user clicks
        # Update the screen with what we've drawn.
        py.display.update()
        clock.tick(MAX_FPS)
        py.display.flip()

if __name__ == "__main__":
    startGame()