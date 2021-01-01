import pygame, sys, random,serial,time

arduino = serial.Serial("COM11", 9600, timeout=.1)
pygame.init()
clock = pygame.time.Clock()
spritcounter = 0
clicked_at = [0,0]
shoot = False #
shot = False # got hit


screen_width = 1500
screen_height = 1000
BG_x = 0
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_icon(pygame.image.load("twitter.png"))
pygame.display.set_caption("Duck Hunt")
BGImg = pygame.image.load("DuckBG.png")

current_time = pygame.time.get_ticks()
exit_time = current_time + 1000

flying = [pygame.image.load("Flying/frame-1.png"),pygame.image.load("Flying/frame-2.png"),pygame.image.load("Flying/frame-3.png"),pygame.image.load("Flying/frame-4.png"),pygame.image.load("Flying/frame-5.png"),pygame.image.load("Flying/frame-6.png"),pygame.image.load("Flying/frame-7.png"),pygame.image.load("Flying/frame-8.png")]
hit = [pygame.image.load("got hit/frame-1.png"),pygame.image.load("got hit/frame-2.png")]
bird_x = 0
bird_y = screen_height/2
bird_speed = 15
rand_y = random.randint(-100, 100)
reached = False

while True:

    screen.blit(BGImg, (0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                clicked_at[0] = event.pos[0]
                clicked_at[1] = event.pos[1]
                shoot = True
        if event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                shoot = False
                pass
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_DOWN:
                pass
            if event.key == pygame.K_SPACE:
                pass

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_DOWN:
                pass
            if event.key == pygame.K_SPACE:
                pass

    if shot != True:
        spritcounter += 1
        if spritcounter >= 7:
            spritcounter = 0

        if reached == True :
            rand_y = random.randrange(-0, 800)
            reached = False

        if bird_y >= rand_y and reached == False:
            bird_y -= 5
            if bird_y <= rand_y:
                reached = True
        elif bird_y <= rand_y and reached == False:
            bird_y += 5
            if bird_y >= rand_y:
                reached = True

        if bird_x < screen_width + 50:
            bird_x += bird_speed
        else:
            bird_x = -100
        screen.blit(pygame.transform.rotozoom(flying[spritcounter], 0, 0.1), (bird_x, bird_y))
    else:
        spritcounter += 1
        if spritcounter >= 1:
            spritcounter = 0
        if bird_y<=screen_height:
            bird_y += 20
        if bird_y>=screen_height:
            bird_x = -10
            bird_y = screen_height/2
            rand_y = random.randrange(-0, 800)
            shot = False
        screen.blit(pygame.transform.rotozoom(hit[spritcounter], -80, 0.1), (bird_x, bird_y))

    hitbox1 = (bird_x , bird_y , 130, 90)

    if bird_x <clicked_at[0] and clicked_at[0]<bird_x+130 and shoot == True:
        if bird_y < clicked_at[1] and clicked_at[1] < bird_y + 90:
            s = pygame.display.get_surface()
            screen.fill((0, 0, 0))
            s.fill(pygame.Color("white"), pygame.draw.rect(screen, (0, 0, 0), hitbox1, 1))

            shot = True
            pass


    while arduino.in_waiting:
        trig = int(float(arduino.readline().decode()))
        s = pygame.display.get_surface()
        screen.fill((0, 0, 0))
        s.fill(pygame.Color("white"), pygame.draw.rect(screen, (0, 0, 0), hitbox1, 1))

        shot = True
        pass

        """trig = int(float(arduino.readline().decode())*10)
        if trig == 1:
            shot=True"""


    pygame.display.flip()
    clock.tick(60)