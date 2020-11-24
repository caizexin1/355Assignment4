import pygame
import sys
import traceback
import copy
from pygame.locals import *

# Initialize color
bg = (200, 220, 255)
board = (50, 50, 50)
button = (50, 50, 50)

# Initialize the menu
def menu_init(screen):
    screen.fill(bg)
    img = pygame.image.load("gomoku_example.jpg").convert_alpha()
    img2 = pygame.transform.scale(img, (563, 563))
    screen.blit(img2, (0, 0))

    pygame.draw.rect(screen, button, [700, 220, 140, 60], 3)
    pygame.draw.rect(screen, button, [700, 320, 140, 60], 3)
    pygame.draw.rect(screen, button, [700, 420, 140, 60], 3)

    m_font = pygame.font.Font(None, 40)
    l_font = pygame.font.Font(None, 60)
    text1 = m_font.render("Play", True, button)
    text2 = m_font.render("Help", True, button)
    text3 = m_font.render("Quit", True, button)
    screen.blit(text1, (735, 240))
    screen.blit(text2, (735, 340))
    screen.blit(text3, (735, 440))

    text4 = l_font.render("Gomoku", True, button)
    screen.blit(text4, (680, 80))

# Show the game introduction and rules
def help(screen):
    screen.fill(bg)
    # intro1 = "Gomoku, also called Five in a Row, is an abstract strategy board game."
    # intro2 = "It is traditionally played with Go pieces on a Go board."
    # intro3 = "- Wikipedia"
    # rule1 = "Player 1 uses a black stone, and player 2 uses a white stone to start the game with an empty board."
    # rule2 = "The black stone goes down first, and the white stone goes down second."
    # rule3 = "The player who first connects five stones into a line wins."
    img = pygame.image.load("rule_example.png").convert_alpha()
    screen.blit(img, (50, 100))

    pygame.draw.rect(screen, button, [240, 460, 140, 60], 3)
    pygame.draw.rect(screen, button, [600, 460, 140, 60], 3)

    s_font = pygame.font.Font(None, 25)
    m_font = pygame.font.Font(None, 40)
    text1 = m_font.render("Play", True, button)
    text3 = m_font.render("Quit", True, button)
    screen.blit(text1, (275, 480))
    screen.blit(text3, (635, 480))

    intro = m_font.render("Welcome to the introduction!", True, button)
    screen.blit(intro, (250, 20))
    intro1 = s_font.render("Gomoku, also called Five in a Row, is an abstract strategy board game.", True, button)
    screen.blit(intro1, (380, 100))
    intro2 = s_font.render("It is traditionally played with Go pieces on a Go board.", True, button)
    screen.blit(intro2, (380, 120))
    intro3 = s_font.render("- Wikipedia", True, button)
    screen.blit(intro3, (800, 150))
    how = s_font.render("How to play:", True, button)
    screen.blit(how, (380, 200))
    rule1 = s_font.render("1. Player 1 uses a black stone, and player 2 uses a white stone to", True, button)
    screen.blit(rule1, (380, 250))
    rule2 = s_font.render("start the game with an empty board.", True, button)
    screen.blit(rule2, (380, 270))
    rule3 = s_font.render("2. The black stone goes down first, and the white stone goes down second.", True, button)
    screen.blit(rule3, (380, 320))
    rule4 = s_font.render("3. The player who first connects five stones into a line wins.", True, button)
    screen.blit(rule4, (380, 370))

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    x, y = event.pos[0], event.pos[1]

                    # Start game
                    if 240 < x < 380 and 460 < y < 520:
                        game_init(screen)

                    # Quit
                    if 600 < x < 740 and 460 < y < 520:
                        pygame.quit()
                        sys.exit()

            pygame.display.update()

# Draw a board
def draw_board(screen):
    screen.fill(bg)
    img = pygame.image.load("board_background.jpg").convert_alpha()
    img_board = pygame.transform.scale(img, (560, 560))
    screen.blit(img_board, (0, 0))
    # Checkerboard line
    for i in range(15):
        pygame.draw.line(screen, board, (40 * i + 3, 3), (40 * i + 3, 563))
        pygame.draw.line(screen, board, (3, 40 * i + 3), (563, 40 * i + 3))
    # Sideline
    pygame.draw.line(screen, board, (0, 0), (563, 0), 5)
    pygame.draw.line(screen, board, (0, 0), (0, 563), 5)
    pygame.draw.line(screen, board, (560, 0), (560, 563), 5)
    pygame.draw.line(screen, board, (0, 560), (560, 560), 5)

    # Point
    pygame.draw.circle(screen, board, (123, 123), 6)
    pygame.draw.circle(screen, board, (123, 443), 6)
    pygame.draw.circle(screen, board, (443, 123), 6)
    pygame.draw.circle(screen, board, (443, 443), 6)
    pygame.draw.circle(screen, board, (283, 283), 6)

    # Regret, Replay and Quit
    pygame.draw.rect(screen, button, [700, 220, 140, 60], 3)
    pygame.draw.rect(screen, button, [700, 320, 140, 60], 3)
    pygame.draw.rect(screen, button, [700, 420, 140, 60], 3)

    m_font = pygame.font.Font(None, 40)
    text1 = m_font.render("Regret", True, button)
    text2 = m_font.render("Replay", True, button)
    text3 = m_font.render("Quit", True, button)
    screen.blit(text1, (725, 240))
    screen.blit(text2, (725, 340))
    screen.blit(text3, (735, 440))


# Draw the stone, 1 = black and 2 = white
def draw_stone(x, y, screen, color):
    if color == 1:
        Black_stone = pygame.image.load("black_stone.png").convert_alpha()
        screen.blit(Black_stone, (40 * x + 3 - 15, 40 * y + 3 - 15))
    if color == 2:
        White_stone = pygame.image.load("white_stone.png").convert_alpha()
        screen.blit(White_stone, (40 * x + 3 - 15, 40 * y + 3 - 15))


# Draw board by stone
def board_by_stone(map, screen):
    screen.fill(bg)
    draw_board(screen)
    for i in range(20):
        for j in range(20):
            draw_stone(i + 1, j + 1, screen, map[i][j])


# Store the list of boards
map = []
for i in range(20):
    map.append([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])


# Empty map
def clear():
    global map
    for i in range(20):
        for j in range(20):
            map[i][j] = 0


# Decide who wins
def win(i, j):
    k = map[i][j]
    p = []
    for a in range(20):
        p.append(0)
    for i3 in range(i - 4, i + 5):
        for j3 in range(j - 4, j + 5):
            if (map[i3][j3] == k and i3 - i == j3 - j and i3 <= i and j3 <= j):
                p[0] += 1
            if (map[i3][j3] == k and j3 == j and i3 <= i and j3 <= j):
                p[1] += 1
            if (map[i3][j3] == k and i3 == i and i3 <= i and j3 <= j):
                p[2] += 1
            if (map[i3][j3] == k and i3 - i == j3 - j and i3 >= i and j3 >= j):
                p[3] += 1
            if (map[i3][j3] == k and j3 == j and i3 >= i and j3 >= j):
                p[4] += 1
            if (map[i3][j3] == k and i3 == i and i3 >= i and j3 >= j):
                p[5] += 1
            if (map[i3][j3] == k and i - i3 == j3 - j and i3 <= i and j3 >= j):
                p[6] += 1
            if (map[i3][j3] == k and i3 - i == j - j3 and i3 >= i and j3 <= j):
                p[7] += 1
            if (map[i3][j3] == k and j - j3 == i - i3 and i3 <= i + 1 and i3 >= i - 3 and j3 <= j + 1 and j3 >= j - 3):
                p[8] += 1
            if (map[i3][j3] == k and j == j3 and i3 <= i + 1 and i3 >= i - 3 and j3 <= j + 1 and j3 >= j - 3):
                p[9] += 1
            if (map[i3][j3] == k and i == i3 and i3 <= i + 1 and i3 >= i - 3 and j3 <= j + 1 and j3 >= j - 3):
                p[10] += 1
            if (map[i3][j3] == k and j - j3 == i - i3 and i3 >= i - 1 and i3 <= i + 3 and j3 >= j - 1 and j3 <= j + 3):
                p[11] += 1
            if (map[i3][j3] == k and j == j3 and i3 >= i - 1 and i3 <= i + 3 and j3 >= j - 1 and j3 <= j + 3):
                p[12] += 1
            if (map[i3][j3] == k and i == i3 and i3 >= i - 1 and i3 <= i + 3 and j3 >= j - 1 and j3 <= j + 3):
                p[13] += 1

    for b in range(14):
        if p[b] == 5:
            return True
    return False


# Draw text to screen
def draw_text(str, screen, size):
    # Cover
    pygame.draw.rect(screen, bg, [680, 80, 1000, 80])
    # Text
    m_font = pygame.font.Font(None, size)
    m_text = m_font.render(str, True, button)
    # Position of text
    screen.blit(m_text, (680, 80))
    pygame.display.flip()

# Control the order of play
t = True

# Still playing
playing = True

# Initialize the game
def game_init(screen):
    global t, map, playing, maps, r, h
    # New game
    clear()

    # For regret
    map2 = copy.deepcopy(map)
    maps = [map2]

    # Initialize game
    draw_board(screen)
    pygame.display.flip()
    clock = pygame.time.Clock()
    while True:
        if playing:
            if t:
                color = 1
                draw_text('Black Play', screen, 50)
            else:
                color = 2
                draw_text('White Play', screen, 50)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            elif event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    x, y = event.pos[0], event.pos[1]
                    for i in range(13):
                        for j in range(13):
                            if i * 40 + 3 + 20 < x < i * 40 + 3 + 60 and j * 40 + 3 + 20 < y < j * 40 + 3 + 60 and not \
                                    map[i][j] and playing:
                                # Place stones
                                draw_stone(i + 1, j + 1, screen, color)

                                # Record the position of stone
                                map[i][j] = color

                                # Store map
                                map3 = copy.deepcopy(map)
                                maps.append(map3)

                                # One player win
                                if win(i, j):
                                    if t:
                                        draw_text('Black Win!', screen, 50)
                                    else:
                                        draw_text('White Win!', screen, 50)

                                    # Cannot place stones after win
                                    playing = False
                                pygame.display.flip()
                                t = not t
                    # Replay
                    if 700 < x < 840 and 320 < y < 380:
                        playing = True
                        game_init(screen)

                    # Quit
                    elif 700 < x < 840 and 420 < y < 480:
                        pygame.quit()
                        sys.exit()

                    # Regret
                    elif 700 < x < 840 and 220 < y < 280 and len(maps) != 1:
                        del maps[len(maps) - 1]
                        map = copy.deepcopy(maps[len(maps) - 1])
                        t = not t
                        board_by_stone(map, screen)

        clock.tick(60)

def main():
    pygame.init()
    pygame.mixer.init()

    # Screen
    screen = pygame.display.set_mode([1000, 563])

    # Name of screen
    pygame.display.set_caption("Gomoku - Made by Zexin Cai")

    menu_init(screen)

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    x, y = event.pos[0], event.pos[1]

                    # Start game
                    if 700 < x < 840 and 220 < y < 280:
                        game_init(screen)

                    # Help
                    if 700 < x < 840 and 320 < y < 380:
                        help(screen)

                    # Quit
                    if 700 < x < 840 and 420 < y < 480:
                        pygame.quit()
                        sys.exit()

            pygame.display.update()

if __name__ == "__main__":
    try:
        main()
    except SystemExit:
        pass
    except:
        traceback.print_exc()
        pygame.quit()
        input()