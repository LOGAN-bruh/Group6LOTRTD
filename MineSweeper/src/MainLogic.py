
import pygame
import sys
import random

# Minesweeper using pygame
# Save as main.py and run: python main.py

TILE = 28
MARGIN = 20
ROWS = 16
COLS = 16
MINES = 40
WIDTH = COLS * TILE + MARGIN * 2
HEIGHT = ROWS * TILE + MARGIN * 2 + 40  # extra for status bar
FPS = 30

# Colors
BG = (200, 200, 200)
GRID = (160, 160, 160)
COVER = (100, 100, 100)
REVEALED = (220, 220, 220)
FLAG = (220, 80, 80)
MINE = (0, 0, 0)
TEXT_COLORS = {
    1: (25, 60, 200),
    2: (25, 150, 25),
    3: (200, 25, 25),
    4: (100, 25, 200),
    5: (150, 50, 20),
    6: (30, 150, 150),
    7: (30, 30, 30),
    8: (100, 100, 100),
}

def neighbors(r, c):
    for dr in (-1, 0, 1):
        for dc in (-1, 0, 1):
            if dr == 0 and dc == 0:
                continue
            nr, nc = r + dr, c + dc
            if 0 <= nr < ROWS and 0 <= nc < COLS:
                yield nr, nc

def generate_mines(first_r, first_c, mines_count):
    positions = [(r, c) for r in range(ROWS) for c in range(COLS)
                 if not (r == first_r and c == first_c)]
    mines = set(random.sample(positions, mines_count))
    counts = [[0]*COLS for _ in range(ROWS)]
    for r, c in mines:
        for nr, nc in neighbors(r, c):
            counts[nr][nc] += 1
    return mines, counts

def flood_reveal(r, c, revealed, mines, counts):
    stack = [(r, c)]
    while stack:
        cr, cc = stack.pop()
        if revealed[cr][cc]:
            continue
        revealed[cr][cc] = True
        if counts[cr][cc] == 0:
            for nr, nc in neighbors(cr, cc):
                if not revealed[nr][nc] and (nr, nc) not in mines:
                    stack.append((nr, nc))

def draw_board(screen, font, mines, counts, revealed, flagged, game_over, win):
    screen.fill(BG)
    # status bar
    status = "Win!" if win else ("Game Over" if game_over else "Mines: {}".format(MINES - sum(sum(row) for row in flagged)))
    status_surf = font.render(status, True, (0,0,0))
    screen.blit(status_surf, (MARGIN, MARGIN // 2))
    for r in range(ROWS):
        for c in range(COLS):
            x = MARGIN + c * TILE
            y = MARGIN + 40 + r * TILE
            rect = pygame.Rect(x, y, TILE-1, TILE-1)
            if revealed[r][c]:
                pygame.draw.rect(screen, REVEALED, rect)
                if (r, c) in mines:
                    pygame.draw.circle(screen, MINE, rect.center, TILE//3)
                else:
                    cnt = counts[r][c]
                    if cnt > 0:
                        txt = font.render(str(cnt), True, TEXT_COLORS.get(cnt, (0,0,0)))
                        txt_rect = txt.get_rect(center=rect.center)
                        screen.blit(txt, txt_rect)
            else:
                pygame.draw.rect(screen, COVER, rect)
                if flagged[r][c]:
                    pygame.draw.circle(screen, FLAG, rect.center, TILE//3)
    pygame.display.flip()

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Minesweeper")
    clock = pygame.time.Clock()
    font = pygame.font.SysFont(None, 24)

    # game state
    mines = set()
    counts = [[0]*COLS for _ in range(ROWS)]
    revealed = [[False]*COLS for _ in range(ROWS)]
    flagged = [[False]*COLS for _ in range(ROWS)]
    started = False
    game_over = False
    win = False

    def reset():
        nonlocal mines, counts, revealed, flagged, started, game_over, win
        mines = set()
        counts = [[0]*COLS for _ in range(ROWS)]
        revealed = [[False]*COLS for _ in range(ROWS)]
        flagged = [[False]*COLS for _ in range(ROWS)]
        started = False
        game_over = False
        win = False

    reset()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    reset()
            if event.type == pygame.MOUSEBUTTONDOWN and not game_over and not win:
                mx, my = event.pos
                # convert to grid
                gx = mx - MARGIN
                gy = my - MARGIN - 40
                if 0 <= gx < COLS * TILE and 0 <= gy < ROWS * TILE:
                    c = gx // TILE
                    r = gy // TILE
                    if event.button == 1:  # left
                        if not started:
                            mines, counts = generate_mines(r, c, MINES)
                            started = True
                        if flagged[r][c] or revealed[r][c]:
                            # if revealed and number, click chording: reveal neighbors if flags match
                            if revealed[r][c] and counts[r][c] > 0:
                                fcount = sum(1 for nr, nc in neighbors(r, c) if flagged[nr][nc])
                                if fcount == counts[r][c]:
                                    for nr, nc in neighbors(r, c):
                                        if not flagged[nr][nc] and not revealed[nr][nc]:
                                            if (nr, nc) in mines:
                                                game_over = True
                                            else:
                                                flood_reveal(nr, nc, revealed, mines, counts)
                            continue
                        if (r, c) in mines:
                            # reveal all mines
                            for mr, mc in mines:
                                revealed[mr][mc] = True
                            game_over = True
                        else:
                            flood_reveal(r, c, revealed, mines, counts)
                    elif event.button == 3:  # right: flag
                        if not revealed[r][c]:
                            flagged[r][c] = not flagged[r][c]
            if event.type == pygame.MOUSEBUTTONDOWN and (game_over or win):
                # click anywhere to reset
                reset()

        # check win
        if not game_over and started:
            revealed_count = sum(sum(1 for c in range(COLS) if revealed[r][c]) for r in range(ROWS))
            if revealed_count == ROWS * COLS - MINES:
                win = True
                # reveal mines as flagged
                for mr, mc in mines:
                    flagged[mr][mc] = True

        draw_board(screen, font, mines, counts, revealed, flagged, game_over, win)
        clock.tick(FPS)

if __name__ == "__main__":
    main()
