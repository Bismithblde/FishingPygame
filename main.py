import pygame
import random
pygame.init()

width, height = 1600, 900
bg = pygame.transform.scale(pygame.image.load("background.png"), (width, height))
fisherman = pygame.transform.scale(pygame.image.load("Fisherman.png"), (width // 20, height // 11))
fisherman_flipped = pygame.transform.flip(fisherman, True, False)
display = pygame.display.set_mode((width, height))
pygame.display.set_caption("game")
walkingVel = 10
jumpVel = 20  # Increase the jump velocity for a higher jump
direction = "right"  # initialize direction to right
jumped = False
floated = False
gravity = 1
fishList = []
greenFish = pygame.transform.scale(pygame.image.load("greenFish.png"), (width//20, height//20))
greenFish = pygame.transform.rotate(greenFish, 90)
fishVel = 35
fishGravity = 1
def drawWindow(fisher):
    display.blit(bg, (0, 0))
    display.blit(fisherman, (fisher.x, fisher.y))

    for i, fishes in enumerate(fishList):
        fishes.updateMovement(i)
        fishes.collide(fisher, i)
        display.blit(greenFish, (fishes.rect.x, fishes.rect.y))
    pygame.display.update()
def handleMovement(fisher, keys, ground):
    global fisherman
    global fisherman_flipped
    global direction

    if keys[pygame.K_a]:
        fisher.x -= walkingVel
        direction = "left"
    if keys[pygame.K_d]:
        fisher.x += walkingVel
        direction = "right"

    # Flip the sprite image based on direction
    if direction == "left":
        fisherman = fisherman_flipped
    else:
        fisherman = pygame.transform.flip(fisherman_flipped, True, False)

def jump(fisherSprite, clock, keys, groundHeight):
    global jumped
    global jumpVel
    global gravity

    if keys[pygame.K_SPACE] and not jumped:
        jumped = True
        jumpVel = -jumpVel

    if jumped: # If fisherSprite has jumped

        fisherSprite.y += jumpVel
        jumpVel += gravity

        if fisherSprite.y >= groundHeight:
            fisherSprite.y = groundHeight
            jumped = False
            jumpVel = 20



class Fish(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, fishJumped, fishVel, groundHeight, hasJumped):
        super().__init__()
        self.width = width
        self.height = height
        self.fishJumped = fishJumped
        self.image = fisherman
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.fishVel = fishVel
        self.groundHeight = groundHeight
        self.hasJumped = hasJumped

    def updateMovement(self, index):

        self.index = index
        if not self.fishJumped:
            self.fishVel = -self.fishVel
            self.fishJumped = True
        if self.fishJumped:

            self.rect.y += self.fishVel
            if self.fishVel < 0:
                self.fishVel += fishGravity
            if self.fishVel >= 0:
                self.fishVel += 0.5
        if self.fishVel == 30:
            self.hasJumped = True

            if self.rect.y >= self.groundHeight + 100 and self.hasJumped:
                print(self.hasJumped)
                fishList.pop(index)
                self.fishJumped = False
                self.fishVel = 30

    def collide(self, fisher, index):
        self.fisher = fisher
        self.index = index
        if self.rect.colliderect(fisher):
            fishList.pop(index)




def makeFishes(groundHeight):
    if random.randint(1, 100) == 9:

        fish = Fish(random.randint(0, width), (height/1.355) + 300, greenFish.get_width(), greenFish.get_height(), False, fishVel, groundHeight, False)
        fishList.append(fish)
def main():
    clock = pygame.time.Clock()
    fisherSprite = pygame.Rect(width / 2 / 2, height / 1.355, width / 20, height / 11)
    groundHeight = fisherSprite.y

    global jumped
    while True:
        clock.tick(60)
        keys = pygame.key.get_pressed()
        handleMovement(fisherSprite, keys, groundHeight)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        jump(fisherSprite, clock, keys, groundHeight)
        makeFishes(groundHeight)
        drawWindow(fisherSprite)

main()
