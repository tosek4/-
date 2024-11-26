import pygame
import random
import sys
from itertools import product
import time

# Initialize pygame
pygame.init()

# Game settings
TIMEOUT = 8  # seconds before game over if no button is pushed
BUTTONSIZE = 50
BUTTONGAPSIZE = 20
BOARD_SIZE = 5
SCREEN_WIDTH = 540
SCREEN_HEIGHT = 430
FPS = 30

# Colors
COLORS = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0)]  # Red, Green, Blue, Yellow
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
DARKGRAY = (169, 169, 169)
GRAY = (105, 105, 105)


# Pygame setup
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Color Fill Puzzle")
clock = pygame.time.Clock()
BASICFONT = pygame.font.Font(None, 36)  # Set up the font (36-point size)


# Initialize board
def create_board():
    board = [[None for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]

    # Fill the board ensuring no neighbors have the same color
    for row, col in product(range(BOARD_SIZE), repeat=2):
        available_colors = COLORS[:]
        if row > 0 and board[row - 1][col] in available_colors:
            available_colors.remove(board[row - 1][col])
        if col > 0 and board[row][col - 1] in available_colors:
            available_colors.remove(board[row][col - 1])
        board[row][col] = random.choice(available_colors)

    return board


# Draw the board on the screen
def draw_board(board, highlight=None):
    for row in range(BOARD_SIZE):
        for col in range(BOARD_SIZE):
            color = board[row][col]
            if highlight and (row, col) in highlight:
                color = (255, 255, 255)  # White when highlighted
            x = BUTTONGAPSIZE + col * (BUTTONSIZE + BUTTONGAPSIZE)
            y = BUTTONGAPSIZE + row * (BUTTONSIZE + BUTTONGAPSIZE)
            rect = pygame.Rect(x, y, BUTTONSIZE, BUTTONSIZE)
            pygame.draw.rect(screen, color, rect)
            pygame.draw.rect(screen, BLACK, rect, 2)


# Flash the sequence with animation effects
def flash_sequence(sequence, board):
    for (row, col) in sequence:
        pygame.time.wait(500)
        draw_board(board, highlight=[(row, col)])
        pygame.display.update()
        pygame.time.wait(500)
        draw_board(board)
        pygame.display.update()


# Check if player's input matches the sequence
def check_sequence(player_sequence, correct_sequence):
    return player_sequence == correct_sequence


# Get row and column from mouse click position
def get_row_col_from_mouse(x, y):
    for row in range(BOARD_SIZE):
        for col in range(BOARD_SIZE):
            btn_x = BUTTONGAPSIZE + col * (BUTTONSIZE + BUTTONGAPSIZE)
            btn_y = BUTTONGAPSIZE + row * (BUTTONSIZE + BUTTONGAPSIZE)
            if btn_x <= x <= btn_x + BUTTONSIZE and btn_y <= y <= btn_y + BUTTONSIZE:
                return row, col
    return None, None


# Draw the Reset Button
def draw_reset_button():
    reset_button = pygame.Rect(SCREEN_WIDTH - 120, SCREEN_HEIGHT - 60, 100, 50)
    pygame.draw.rect(screen, (255, 0, 0), reset_button)
    reset_text = BASICFONT.render("Reset", True, WHITE)
    screen.blit(reset_text, (SCREEN_WIDTH - 100, SCREEN_HEIGHT - 50))


# Handle Reset Button Click
def reset_game():
    global level, sequence, player_sequence, game_over, showing_sequence, start_time
    level = 1
    sequence = []
    player_sequence = []
    game_over = False
    showing_sequence = True
    start_time = time.time()  # Reset the timer


def main():
    global level, sequence, player_sequence, game_over, showing_sequence, start_time
    board = create_board()
    level = 1
    sequence = []
    player_sequence = []
    game_over = False
    showing_sequence = True
    start_time = time.time()  # Start time for timeout

    while True:
        screen.fill(GRAY)
        draw_board(board)

        # Display the current level
        level_text = BASICFONT.render(f"Level: {level}", True, DARKGRAY)
        screen.blit(level_text, (SCREEN_WIDTH - 105, 20))

        # Handle the game over condition
        if game_over:
            game_over_text = BASICFONT.render("Game Over!", True, (255, 0, 0))
            text_rect = game_over_text.get_rect(center=(SCREEN_WIDTH // 2.5, SCREEN_HEIGHT -25))
            screen.blit(game_over_text, text_rect)

        # Display Reset Button
        draw_reset_button()

        if showing_sequence:
            # Generate a new sequence for the current level
            new_step = (random.randint(0, BOARD_SIZE - 1), random.randint(0, BOARD_SIZE - 1))
            sequence.append(new_step)
            flash_sequence(sequence, board)
            player_sequence = []
            showing_sequence = False
            start_time = time.time()  # Reset the timer

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            elif event.type == pygame.MOUSEBUTTONDOWN and not game_over:
                x, y = pygame.mouse.get_pos()
                row, col = get_row_col_from_mouse(x, y)

                if row is not None and col is not None:
                    player_sequence.append((row, col))
                    start_time = time.time()  # Reset timer on player click

                    # Check the player's sequence input
                    if not sequence[:len(player_sequence)] == player_sequence:
                        game_over = True

                    elif len(player_sequence) == len(sequence):
                        incorrect_sequence = BASICFONT.render("Correct! Moving to the next level.", True, (255, 0, 0))
                        text_incorrect_sequence = incorrect_sequence.get_rect(
                            center=(SCREEN_WIDTH // 2.5, SCREEN_HEIGHT -25))


                        screen.blit(incorrect_sequence, text_incorrect_sequence)
                        print("Correct! Moving to the next level.")
                        level += 1
                        showing_sequence = True

            # Check for Reset button click
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                if SCREEN_WIDTH - 120 <= x <= SCREEN_WIDTH - 20 and SCREEN_HEIGHT - 60 <= y <= SCREEN_HEIGHT - 10:
                    reset_game()

        pygame.display.update()
        clock.tick(FPS)


if __name__ == "__main__":
    main()
