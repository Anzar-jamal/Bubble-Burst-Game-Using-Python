import cv2
import pygame
import numpy as np
import mediapipe as mp
import random

mp_draw = mp.solutions.drawing_utipipls
mp_draw_styles = mp.solutions.drawing_styles
mp_hands = mp.solutions.hands
hands = mp_hands.Hands()

width, height = 1000,700
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('Bubble Pop Game by Anzar')


background = pygame.image.load('BubbleGameBG.jpg').convert_alpha()
background = pygame.transform.scale(background, (width, height))

clock = pygame.time.Clock()


class IntroBubble(pygame.sprite.Sprite):
    def __init__(self, bubble, x, y, speed):
        pygame.sprite.Sprite.__init__(self, self.containers)
        self.image = pygame.image.load(bubble).convert_alpha()
        self.image = pygame.transform.scale(self.image, (100,100))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = speed

    def update(self, next_bubble_batch=None):
        screen.blit(self.image, self.rect)
        if self.rect.y <= 0:
            self.kill()

        elif self.rect.y <= height:
            self.rect.y -= self.speed





def intro_window(background):
    pygame.init()
    font = pygame.font.Font(None, 45)
    running = True
    game_over = False
    max_bubble_on_window = 15
    next_bubble_batch = 10
    pygame.time.set_timer(next_bubble_batch, 2000)

    all_bubble = pygame.sprite.Group()
    IntroBubbleSprite = pygame.sprite.Group()
    IntroBubble.containers = IntroBubbleSprite, all_bubble


    while running:

        for event in pygame.event.get():
            if event.dict.get('key') == 27:
                running = False

            elif event.type == pygame.KEYDOWN:
                running = False

            elif event.type == next_bubble_batch:
                for i in range(random.randint(2,3)):
                    IntroBubble('Bubble.png', random.randint(0,width), height, random.randint(1,4))

        if len(all_bubble) < max_bubble_on_window:
            for i in range(random.randint(1,3)):
                IntroBubble('Bubble.png', random.randint(0,width), height, random.randint(1,4))

        screen.blit(background,(0, 0))
        start_text = font.render('Enter any key to start the Game', True, (0,255,0), None)
        screen.blit(start_text, (width//2-220, height//2-100))

        IntroBubbleSprite.update()
        pygame.display.flip()



class MainWinBubble(pygame.sprite.Sprite):
    def __init__(self, bubble, x, y, speed):
        pygame.sprite.Sprite.__init__(self, self.containers)
        self.image = pygame.image.load(bubble).convert_alpha()
        self.image = pygame.transform.scale(self.image, (80,80))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = speed
        self.radius = 32

    def update(self, score, position):
        screen.blit(self.image, self.rect)
        if self.rect.y <= 0:
            self.speed = 0
            self.rect.y = 0


        elif self.rect.y <= height and self.speed != 0:
            self.rect.y -= self.speed
            mouse_position = pygame.mouse.get_pos()
            mouse_clicked = pygame.mouse.get_pressed()
            #if mouse_clicked[0] and self.rect.collidepoint(*mouse_position):
            if self.rect.collidepoint(*position):
                pop = pygame.image.load('BubbleBursted.png').convert_alpha()
                pop = pygame.transform.scale(pop, (135,100))
                self.image = pop
                #screen.blit(pop, (self.rect.x, self.rect.y))
                screen.blit(pop, position)
                score= score +10
                self.kill()
        return score

    def collide(self, all_bubble_list):
        collections = pygame.sprite.spritecollide(self, all_bubble_list, False, pygame.sprite.collide_circle)
        for each in collections:
            if each.speed ==0:
                self.speed =0




def get_frame(cap):
    success, frame = cap.read()
    frame = cv2.resize(frame, (width, height))
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    results = hands.process(frame)
    x1, y1 = 0, 0
    if results.multi_hand_landmarks:
        hand_landmarks = results.multi_hand_landmarks[0].landmark
        single_finger = hand_landmarks[8]
        x1, y1 = width - int(single_finger.x * width), int(single_finger.y * height)

        for hand_landmarks in results.multi_hand_landmarks:
            mp_draw.draw_landmarks(
                frame,
                hand_landmarks,
                mp_hands.HAND_CONNECTIONS,
                mp_draw_styles.get_default_hand_landmarks_style(),
                mp_draw_styles.get_default_hand_connections_style())


    frame = np.rot90(frame)
    frame = pygame.surfarray.make_surface(frame)
    return frame, (x1, y1)
def main_window(background):
    pygame.init()
    font = pygame.font.Font(None, 45)
    bubble_drop = 10
    pygame.time.set_timer(bubble_drop, 3000)
    high_score = 500
    score = 0
    game_over = False

    all_bubble_list = pygame.sprite.Group()
    all_sprites = pygame.sprite.Group()

    MainWinBubble.containers = all_sprites, all_bubble_list

    intro_window(background)

    cap = cv2.VideoCapture(0)

    while not game_over:
        for event in pygame.event.get():
            if event.dict.get('key') == 27:
                game_over = True

            elif event.type == bubble_drop:
                for i in range(random.randint(2,3)):
                    MainWinBubble('Bubble.png', random.randint(0, width), height, random.randint(1,4))

            elif score ==high_score:
                game_over = True

        frame, position = get_frame(cap)

        screen.blit(frame, (0,0))
        score_text = font.render(f'score: {score}', True, (0,255,255), None)
        screen.blit(score_text, (0,0))


        if not game_over:
            for bubble in all_bubble_list:
                score = bubble.update(score, position)

            for bubble in all_bubble_list:
                all_bubble_list.remove(bubble)
                bubble.collide(all_bubble_list)
                all_bubble_list.add(bubble)

        else:
            all_sprites.clear(screen, background)
            all_sprites.update(score)

        pygame.display.flip()
        #clock.tick(30)


if __name__ == '__main__' :
    main_window(background)