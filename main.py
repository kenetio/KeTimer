import pygame
import time
import sys
from random import randint

pygame.init()

fps = 100

sc = pygame.display.set_mode((1000, 600))
pygame.display.set_caption("KeTimer")
clock = pygame.time.Clock()

font = pygame.font.Font('fonts/DroidSansMono.ttf', 84)
font2 = pygame.font.Font('fonts/DroidSansMono.ttf', 24)
font3 = pygame.font.Font('fonts/DroidSansMono.ttf', 18)
black = (18, 17, 19)
green = (0, 179, 0)
red = (214, 37, 21)
gray = (104, 109, 107)


delt = pygame.image.load('img/Delete.png')
delt = pygame.transform.scale(delt, ((delt.get_width()//3*2), (delt.get_height()//3*2)))

ic = pygame.image.load('img/icon.png')
pygame.display.set_icon(ic)

recfile = open('record.txt','r+')

def format(tim):
    tim = round(tim*100)
    mseconds = str(tim % 100)
    if int(mseconds) < 10:
        mseconds = "0" + mseconds
    seconds = str((tim % 6000) // 100)
    if int(seconds) < 10:
        seconds = "0" + seconds
    minuts = str(tim // 6000)
    if int(minuts) < 10:
        minuts = "0" + minuts
    return ((minuts + ":" + seconds + "." + mseconds))


def main():
    #переменные
    times = []
    img_times = []
    starttime = time.time()
    tim = 0
    s = "00:00.00"
    running = True
    timer_flag = False
    ready = False
    timercolor = black
    actext = "-"
    actext1 = "-"
    delrect = delt.get_rect(center=(500, 425))
    rectext = "-"
    rel = int(*recfile)/100
    if rel != 9999999999999999999999999999999.99:
        rectext = format(rel)
    pstrel = rel
    recfile.seek(0)
    recfile.truncate()
    print(rel)
    rotates = ["R", "D", "L", "U", "F", "B"]
    dops = ["", "'", "2"]
    skrambl = ""
    latest = rotates[randint(0, 5)]
    for i in range(randint(20, 22)):
        new = rotates[randint(0,5)]
        while new == latest:
            new = rotates[randint(0, 5)]
        latest = new
        skrambl += new + dops[randint(0, 2)] + " "
    sctext = font3.render(skrambl, True, gray)
    screct = sctext.get_rect(center = (500, 35))
    while running:
        clock.tick(fps)

        #клавиши

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                recfile.write(str(((rel) * 100) - ((rel) * 100) % 1)[0:-2])
                recfile.close()
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if timer_flag == False:
                        starttime = time.time()
                        #tim = 0
                        ready = True
                        timercolor = red
                    if timer_flag == True:
                        timer_flag = False
                        times.append(tim)
                        img_times.append(font2.render(format(tim), True, timercolor))
                        if len(img_times) > 12:
                            img_times.pop(0)
                        if rel > tim:
                            print(tim)
                            print(rel)
                            recfile.seek(0)
                            pstrel = rel
                            rel = tim
                            recfile.truncate()

                            rectext = format(rel)



                        skrambl = ""
                        latest = rotates[randint(0, 5)]
                        for i in range(randint(20, 22)):
                            new = rotates[randint(0, 5)]
                            while new == latest:
                                new = rotates[randint(0, 5)]
                            latest = new
                            skrambl += new + dops[randint(0, 2)] + " "
                        sctext = font3.render(skrambl, True, gray)
                        screct = sctext.get_rect(center=(500, 35))
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_SPACE:
                    if ready == True:
                        if tim >= 0.5:
                            starttime = time.time()
                            timer_flag = True
                        ready = False
                        timercolor = black
            elif event.type == pygame.MOUSEBUTTONDOWN:
                posx, posy = pygame.mouse.get_pos()
                if event.button == 1:
                    bx, by = delrect.bottomright
                    print(delrect.x, posx, bx, delrect.y, posy, by)
                    if (delrect.x < posx < bx) and (delrect.y < posy < by):
                        if ready == False and timer_flag == False and len(times):
                            tim = 0
                            s = "00:00.00"
                            if times[-1] == rel:
                                rel = pstrel
                            rectext = format(rel)      
                            times.pop(-1)
                            img_times.pop(-1)


        #создание картинок
        ac5 = font2.render(("AVG 5: " + actext), True, black)
        ac12 = font2.render(("AVG 12: " + actext1), True, black)
        rec = font2.render(("Record: " + rectext), True, black)
        timer = font.render(s, True, timercolor)

        #отрисовка
        sc.fill((247, 247, 242))
        sc.blit(timer, (300, 251))
        o = 0
        for i in img_times:
            sc.blit(i, (20, (20 + o * 30)))
            o += 1
        sc.blit(ac5, (20, 400))
        sc.blit(ac12, (20, 430))
        sc.blit(rec, (20, 460))
        if ready == False and timer_flag == False and (tim > 0 and not s == "00:00.00"):
            sc.blit(delt, delrect)
        sc.blit(sctext, screct)

        pygame.display.update()

        #обработка
        if ready == True:
            tim = time.time()-starttime
            if tim > 0.5:
                timercolor = green
        if timer_flag == True:
            tim = time.time()-starttime
            s = format(tim)
        actext = 0
        if len(times) < 5:
            actext = "-"
        else:
            actext = str(format((round((times[-1])*100) + round((times[-2])*100) + round((times[-3])*100) + round((times[-4])*100) + round((times[-5])*100))/500))
        actext1 = 0
        if len(times) < 12:
            actext1 = "-"
        else:
            for i in range(12):
                actext1 += round((times[-i])*100)
            actext1 = str(format(actext1/1200))




main()
