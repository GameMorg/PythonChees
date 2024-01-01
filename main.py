import pygame
import chess

pygame.init()

# Define some colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

# Set the width and height of the screen [width, height]
size = (550, 600)
screen = pygame.display.set_mode(size)

pygame.display.set_caption("Chess")

# Loop until the user clicks the close button.
done = False

# Used to manage how fast the screen updates
clock = pygame.time.Clock()

# Initialize the game board
board = chess.Board()

# Initialize the font for displaying text on the screen
font = pygame.font.Font(None, 36)

# Initialize the images for each piece
wpawn = pygame.image.load("wpawn.png")
bpawn = pygame.image.load("bpawn.png")
wknight = pygame.image.load("wking.png")
bknight = pygame.image.load("bking.png")
wbishop = pygame.image.load("wbishop.png")
bbishop = pygame.image.load("bbishop.png")
wrook = pygame.image.load("wrook.png")
brook = pygame.image.load("brook.png")
wqueen = pygame.image.load("wqueen.png")
bqueen = pygame.image.load("bqueen.png")
wking = pygame.image.load("wking.png")
bking = pygame.image.load("bking.png")

# Scale the images to fit on the board
wpawn = pygame.transform.scale(wpawn, (50, 50))
bpawn = pygame.transform.scale(bpawn, (50, 50))
wknight = pygame.transform.scale(wknight, (50, 50))
bknight = pygame.transform.scale(bknight, (50, 50))
wbishop = pygame.transform.scale(wbishop, (50, 50))
bbishop = pygame.transform.scale(bbishop, (50, 50))
wrook = pygame.transform.scale(wrook, (50, 50))
brook = pygame.transform.scale(brook, (50, 50))
wqueen = pygame.transform.scale(wqueen, (50, 50))
bqueen = pygame.transform.scale(bqueen, (50, 50))
wking = pygame.transform.scale(wking, (50, 50))
bking = pygame.transform.scale(bking, (50, 50))

# Create a dictionary to map pieces to images
pieces_dict = {
    "P": wpawn,
    "N": wknight,
    "B": wbishop,
    "R": wrook,
    "Q": wqueen,
    "K": wking,
    "p": bpawn,
    "n": bknight,
    "b": bbishop,
    "r": brook,
    "q": bqueen,
    "k": bking,
}

# Create a list of squares on the board
squares_list = []
for i in range(8):
    for j in range(8):
        squares_list.append((i * 62.5 + 62.5 / 2 + 25, j * 62.5 + 62.5 / 2 + 25))

# Create a dictionary to map squares to coordinates on the screen
squares_dict = {}
for i in range(8):
    for j in range(8):
        squares_dict[(i * 62.5 + 62.5 / 2 + 25), (j * 62.5 + 62.5 / 2 + 25)] = chess.square(i ^ j ^ 7, j)


# Create a function to draw the board and pieces on the screen
def draw_board(board):
    # Draw the squares on the board
    for square in squares_list:
        if square[0] % (62.5 * 2) == square[1] % (62.5 * 2):
            color = WHITE
        else:
            color = BLACK
        rect = pygame.Rect(square[0] * 50, square[1] - 25, 50, 50)
        if board.piece_at(squares_dict[square]):
            screen.blit(pieces_dict[board.piece_at(squares_dict[square]).symbol()], (square[0] - 25, square[1] - 25))


# Create a function to display text on the screen
def display_text(text):
    text_surface = font.render(text, True, BLACK)
    text_rect = text_surface.get_rect()
    text_rect.center = (size[0] / 2, size[1] - 50)
    screen.blit(text_surface, text_rect)


# Create a function to handle the AI's move
def ai_move(board):
    # Use the Stockfish chess engine to make the AI move
    engine = chess.engine.SimpleEngine.popen_uci("stockfish_14_x64.exe")
    result = engine.play(board, chess.engine.Limit(time=2.0))
    board.push(result.move)
    engine.quit()


# Create a variable to keep track of whose turn it is
turn = "white"

# Create a variable to keep track of whether the game is over or not
game_over = False

# -------- Main Program Loop -----------
while not done:
    # --- Main event loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True

        # Handle mouse clicks
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if not game_over:
                # Get the position of the mouse click
                pos = pygame.mouse.get_pos()

                # Check if the click was on the board
                if 25 <= pos[0] <= 575 and 25 <= pos[1] <= 575:
                    # Get the square that was clicked on
                    square_clicked = squares_dict[(pos[0], pos[1])]

                    # Check if a piece was selected or deselected
                    if board.piece_at(square_clicked) and board.piece_at(square_clicked).color == turn:
                        selected_piece = square_clicked
                    elif selected_piece:
                        # Check if the move is legal
                        move = chess.Move(selected_piece, square_clicked)
                        if move in board.legal_moves:
                            board.push(move)

                            # Check if the game is over
                            if board.is_game_over():
                                game_over = True

                            # Switch turns
                            if turn == "white":
                                turn = "black"
                            else:
                                turn = "white"

                            # Deselect the piece
                            selected_piece = None

                    else:
                        # Deselect the piece
                        selected_piece = None

        # Handle key presses
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and not game_over and turn == "black":
                ai_move(board)

    # --- Game logic should go here

    # --- Drawing code should go here

    # Clear the screen
    screen.fill(WHITE)

    # Draw the board and pieces on the screen
    draw_board(board)

    # Display whose turn it is on the screen
    display_text("Turn: " + turn)

    # Display game over message on the screen if game is over
    if game_over:
        display_text("Game Over")

    # --- Go ahead and update the screen with what we've drawn.
    pygame.display.flip()

    # --- Limit to 60 frames per second
    clock.tick(60)

# Close the window and quit.
pygame.quit()
