import pygame
from random import *
import os
import sys

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

# 시작 화면 - 시작 버튼
def first_screen():
    pygame.draw.rect(screen, WHITE, start)
    msg = game_font.render("START", True, BLACK)
    msg_rect = msg.get_rect(center=(640, 670))
    screen.blit(msg, msg_rect)

# 카드에 번호를 지정하는 함수
def card_setting():
    screen_x_margin = 30
    screen_y_margin = 30    
    card_width = 190
    card_height = 200
    card_x_margin = 16
    card_y_margin = 5
    a = [0,0,0,0,0,0,0,0,0]
    
    for i in range(3):
        for j in range(6):
            while True:
                num = randint(1, 9)
                if a[num-1] < 2:
                    a[num-1] += 1
                    break
                else:
                    continue

            center_x = screen_x_margin + ((card_width + card_x_margin) * j) + (card_width / 2)
            center_y = screen_y_margin + ((card_height + card_y_margin) * i) + (card_height / 2)

            card = pygame.Rect(0,0,card_width, card_height)
            card.center = (center_x, center_y)
            
            cards.append([card, num])
            print(cards)

    for i in cards:
        pygame.draw.rect(screen, GREEN, i[0])

# 게임 화면 - 카드 앞면을 잠시 공개 후 뒷면으로 세팅
def play_screen():
    global running
    show_cards()
    comp_card()
    if (len(cards))==0:
        screen.fill(BLACK)
        msg = game_font1.render("Game Clear", True, WHITE)
        msg_rect = msg.get_rect(center=(640, 360))
        screen.blit(msg, msg_rect)
        running = False

# 전체 카드 앞면을 보여주는 함수
def show_cards():
    global hidden
    elapsed_time = (pygame.time.get_ticks() - start_ticks) / 1000
    if elapsed_time < total_time:
        for i in cards:
            pygame.draw.rect(screen, GREEN, i[0])
            msg = game_font1.render(f"{i[1]}", True, BLACK)
            msg_rect = msg.get_rect(center=i[0].center)
            screen.blit(msg, msg_rect)

            timer = game_font.render("{}".format(int(total_time - elapsed_time + 1)), True, WHITE)
            timer_rect = timer.get_rect(center=(640,670))
            screen.blit(timer, timer_rect)
    else:
        hidden = True
        for i in cards:
            pygame.draw.rect(screen, GREEN, i[0])

# 클릭 처리 - 1. 시작 버튼 클릭 처리  2. 카드 클릭 처리
def update_screen(click_pos):
    global game_play, start_ticks
    if game_play:
        check_card(click_pos)
    elif start.collidepoint(click_pos):
        start_ticks = pygame.time.get_ticks()
        card_setting()
        game_play = True

# 클릭한 카드를 comp_cards 리스트로 이동
def check_card(click_pos):
    if hidden:
        for idx, i in enumerate(cards):
            if i[0].collidepoint(click_pos):
                del cards[idx]
                comp_cards.append(i)

# 클릭한 카드의 앞면을 보여주고 클릭한 카드들끼리 비교하는 함수
def comp_card():
    for i in comp_cards:
        pygame.draw.rect(screen, GREEN, i[0])
        msg = game_font1.render(f"{i[1]}", True, BLACK)
        msg_rect = msg.get_rect(center=i[0].center)
        screen.blit(msg, msg_rect)
    if len(comp_cards) == 2:
        if comp_cards[0][1] == comp_cards[1][1]:
            del comp_cards[1]
            del comp_cards[0]
        else:
            cards.append(comp_cards[0])
            cards.append(comp_cards[1])
            del comp_cards[1]
            del comp_cards[0]

pygame.init()
screen_width = 1280
screen_height = 720
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("CardFlip")
game_font = pygame.font.Font(resource_path("ARLRDBD.TTF"), 40)
game_font1 = pygame.font.Font(resource_path("ARLRDBD.TTF"), 90)

BLACK = (0,0,0)
WHITE = (255,255,255)
GREEN = (0, 255, 0)
game_play = False
start = pygame.Rect(570, 640, 140, 60)
cards = []
comp_cards = []
start_ticks = None
total_time = 10
hidden = False

running = True
while running:
    click_pos = None

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONUP:
            click_pos = pygame.mouse.get_pos()
            print(click_pos)

    screen.fill(BLACK)

    if game_play:
        play_screen()
    else:
        first_screen()
    
    if click_pos:
        update_screen(click_pos)

    pygame.display.update()
pygame.time.delay(2000)

pygame.quit()
