import pygame
import random
pygame.init()

screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
green = (0, 112, 0)

suits = ('C', 'D', 'H', 'S')
values = ('A', 'J', 'K', 'Q')
deck = []
hand = []

class card():
    def __init__(self, value, suit, image):
        self.value = value
        self.suit = suit
        self.image = image


for suit in suits:
    for i in range(2,10):
        img = pygame.image.load('cards/' + str(i) + suit + '.jpg')
        screen.blit(img, (0, 0))
        deck.append(card(str(i), suit, img))
    for value in values:
        img = pygame.image.load('cards/' + value + suit + '.jpg')
        deck.append(card(value, suit, img))

random.shuffle(deck)
hand = deck[0:13]

mainLoop = True

infoObject = pygame.display.Info()
x = infoObject.current_w
y = infoObject.current_h
height = int(y / 5)
width = int(x / 13)

while mainLoop:
    screen.fill(green)
    for card in hand:
        index = hand.index(card)
        img = pygame.transform.scale(card.image, (width, height))
        screen.blit(img, (width * index, y - height))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            mainLoop = False
    pygame.display.update()

pygame.quit()
