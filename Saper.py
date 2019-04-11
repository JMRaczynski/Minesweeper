import pygame
from random import randrange
from pygame.locals import *
from time import time
pygame.init()

GAPSIZE = 2
BGCOL = (92, 20, 236)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
WHITE = (255, 255, 255)
CBUTTONCOL = (200, 200, 200)
BUTTONCOL = (150, 150, 150)
FWIDTH = 22
FHEIGHT = 22
BOXSIZE = 30
GRIDSIZE = 8
NUMOFMINES = int(GRIDSIZE ** 2 * 0.16)
SCRWIDTH = BOXSIZE * GRIDSIZE + 260
SCRHEIGHT = SCRWIDTH
FONT = pygame.font.SysFont('Calibri', 16, True, False)
GOFONT =  pygame.font.SysFont('Calibri', 44, False, False)

size = (SCRHEIGHT, SCRWIDTH)
screen = pygame.display.set_mode(size)
pygame.display.set_caption("SAPER")

## FIELD STRUCTURE: TOPLEFTX, TOPLEFT Y, ISTHEREMINE, NEIGHBOURING MINES, REVEALED: 0 = NOT 1 = YES 2 = MINE 3 = ?


def restartbutton():
    pygame.draw.rect(screen, RED, [195, 45, 110, 60])
    pygame.draw.rect(screen, CBUTTONCOL, [200, 50, 100, 50])
    capt = FONT.render('Restart', True, BLACK)
    cencoords = fcenter(195, 45, 110, 60)
    captrect = capt.get_rect()
    captrect.centerx, captrect.centery = cencoords[0], cencoords[1]
    screen.blit(capt, captrect)


def restart():
    global fields, done, failed, won, timePassed
    done, failed, won = False, False, False
    screen.fill(BGCOL)
    defhor = center(SCRWIDTH, GAPSIZE, GRIDSIZE, FWIDTH)
    defver = center(SCRHEIGHT, GAPSIZE, GRIDSIZE, FHEIGHT)
    pygame.draw.rect(screen, BLACK,
                     [defhor, defver, FWIDTH * GRIDSIZE + GAPSIZE * (GRIDSIZE + 1), FHEIGHT * GRIDSIZE + GAPSIZE * (GRIDSIZE + 1)])
    defhor += GAPSIZE
    defver += GAPSIZE
    restartbutton()
    horpos = defhor
    verpos = defver
    fields = [[[0, 0, False, 0, 0] for i in range(GRIDSIZE)] for j in range(GRIDSIZE)]
    for i in range(GRIDSIZE):
        for j in range(GRIDSIZE):
            fields[i][j][0], fields[i][j][1] = horpos, verpos
            pygame.draw.rect(screen, BUTTONCOL, [horpos, verpos, FWIDTH, FHEIGHT])
            horpos += FWIDTH + GAPSIZE
        horpos = defhor
        verpos += FHEIGHT + GAPSIZE
    placemines(fields)
    countmines(fields)
    timePassed = time()


def center(ssize, gap, num, fsize):
    return int((ssize - (num * fsize + gap * num)) / 2)


def fcenter(x, y, w, h):
    return x + w / 2, y + h / 2


def drawMineorNumber(field):
    pygame.draw.rect(screen, CBUTTONCOL, [field[0], field[1], FWIDTH, FHEIGHT])
    half = int(FWIDTH / 2)
    quarter = int(FWIDTH / 4)
    eighth = int(FWIDTH / 8)
    left = field[0]
    top = field[1]
    if not field[2] and field[3] != 0:
        number = FONT.render(str(field[3]), True, BLACK)
        cencoords = fcenter(left, top, FWIDTH, FHEIGHT)
        numrect = number.get_rect()
        numrect.centerx, numrect.centery = cencoords[0], cencoords[1]
        screen.blit(number, numrect)
    elif field[2]:
        pygame.draw.circle(screen, BLACK, (left + half, top + half), quarter)
        pygame.draw.circle(screen, WHITE, (left + half, top + half), eighth)
        pygame.draw.line(screen, BLACK, (left + eighth, top + half),
                         (left + half + quarter + eighth, top + half))
        pygame.draw.line(screen, BLACK, (left + half, top + eighth),
                         (left + half, top + half + quarter + eighth))
        pygame.draw.line(screen, BLACK, (left + quarter, top + quarter),
                         (left + half + quarter, top + half + quarter))
        pygame.draw.line(screen, BLACK, (left + quarter, top + half + quarter),
                         (left + half + quarter, top + quarter))
    field[4] = 1


def placemines(fields):
    placed = 0
    breaker = False
    while 1:
        for i in range(GRIDSIZE):
            for j in range(GRIDSIZE):
                if fields[i][j][2] == 0 and randrange(1, 10) == 7:
                    fields[i][j][2] = True
                    placed += 1
                if placed == NUMOFMINES:
                    breaker = True
                    break
            if breaker:
                break
        if breaker:
            break


def countmines(fields):
    for i in range(GRIDSIZE):
        for j in range(GRIDSIZE):
            for k in range(-1, 2, 1):
                for l in range(-1, 2, 1):
                    if not (k == 0 and l == 0):
                        if GRIDSIZE > i + k > -1 and GRIDSIZE > j + l > -1 and fields[i+k][j+l][2] == 1:
                            fields[i][j][3] += 1


def markmine(field):
    pygame.draw.rect(screen, BUTTONCOL, [field[0], field[1], FWIDTH, FHEIGHT])
    if field[4] == 0:
        mark = FONT.render('M', True, RED)
        field[4] = 2
    elif field[4] == 2:
        mark = FONT.render('?', True, BLACK)
        field[4] = 3
    else:
        mark = FONT.render('', True, RED)
        field[4] = 0
    cencoords = fcenter(field[0], field[1], FWIDTH, FHEIGHT)
    markrect = mark.get_rect()
    markrect.centerx, markrect.centery = cencoords[0], cencoords[1]
    screen.blit(mark, markrect)


def revealempty(fields, xind, yind):
    for i in range(-1, 2, 1):
        for j in range(-1, 2, 1):
            if not (i == 0 and j == 0):
                if GRIDSIZE > i + xind > -1 and GRIDSIZE > j + yind > -1 and fields[i + xind][j + yind][4] != 1:
                    drawMineorNumber(fields[i + xind][j + yind])
                    if fields[i + xind][j + yind][3] == 0:
                        revealempty(fields, i+xind, j+yind)


def fail():
    global failed
    failed = True
    capt = GOFONT.render('U LOST, RIP [*]', True, RED)
    captrect = capt.get_rect()
    captrect.centerx, captrect.centery = SCRWIDTH / 2, 4 * SCRHEIGHT / 5
    screen.blit(capt, captrect)


def win():
    global failed, timePassed
    won = True
    capt = GOFONT.render('U WON, TIME: ' + str(round(time() - timePassed)) + ' s', True, GREEN)
    captrect = capt.get_rect()
    captrect.centerx, captrect.centery = SCRWIDTH / 2, 4 * SCRHEIGHT / 5
    screen.blit(capt, captrect)


def checkifwin():
    counter = 0
    for i in fields:
        for j in i:
            if j[4] == 1:
                counter += 1
    if counter == GRIDSIZE ** 2 - NUMOFMINES:
        win()


def main():
    global fields, done, failed, won
    clock = pygame.time.Clock()
    restart()
    while not done:
        mouseclicked = False
        breaker = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            elif event.type == MOUSEBUTTONDOWN:
                mousex, mousey = event.pos
                button = event.button
                mouseclicked = True
        if mouseclicked:
            if button == 1:
                if 195 < mousex < 305 and 45 < mousey < 105:
                    restart()
                else:
                    if not (failed or won):
                        for i in fields:
                            for j in i:
                                if j[0] < mousex < (j[0] + FWIDTH) and j[1] < mousey < (j[1] + FHEIGHT) and j[4] == 0:
                                    if j[2]:
                                        for k in fields:
                                            for l in k:
                                                if l[2]:
                                                    drawMineorNumber(l)
                                        fail()
                                    else:
                                        drawMineorNumber(j)
                                        if j[3] == 0:
                                            revealempty(fields, fields.index(i), i.index(j))
                                    breaker = True
                                    break
                            if breaker:
                                break
                checkifwin()
            elif button == 3:
                for i in fields:
                    for j in i:
                        if j[0] < mousex < (j[0] + FWIDTH) and j[1] < mousey < (j[1] + FHEIGHT) and j[4] != 1:
                            markmine(j)
                            breaker = True
                            break
                    if breaker:
                        break
        pygame.display.flip()  # update'owanie okienka
        clock.tick(60)
    pygame.quit()


if __name__ == "__main__":
    main()