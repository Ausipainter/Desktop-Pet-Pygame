import subprocess
import sys

def install_package(package_name):
    print(f"Installing {package_name}...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", package_name])
    print(f"{package_name} installed!")
try:
    import pygame
except ImportError:
    install_package('pygame')
    import pygame
try:
    import win32gui
except ImportError:
    install_package('pywin32')
import win32gui
import win32con
import ctypes
import threading
import time
import os
import random
MAINDIR = os.path.dirname(__file__)
ASSETSDIR = os.path.join(MAINDIR,"Assets")
CONFIGDIR = os.path.join(ASSETSDIR,"Config")
SPRITESDIR = os.path.join(ASSETSDIR,"Sprites")
sprites = os.listdir(SPRITESDIR)
screen = pygame.display.set_mode((400,700))
WIDTH = 400
HEIGHT = 700
pygame.display.set_caption("Configuration")
print(len(sprites))
print(sprites)

script_path = os.path.join(MAINDIR,"Pet.py")


selectPet = 0



background_img = pygame.transform.scale(pygame.image.load(os.path.join(CONFIGDIR,"Background.png")), (WIDTH,HEIGHT))
background_rect = background_img.get_rect()
rightArrow_img = pygame.transform.scale(pygame.image.load(os.path.join(CONFIGDIR,"Arrow.png")), (100,100))
rightArrow_rect = rightArrow_img.get_rect(topleft=(240,270))
leftArrow_img = pygame.transform.flip(pygame.transform.scale(pygame.image.load(os.path.join(CONFIGDIR,"Arrow.png")), (100,100)),True, False)
leftArrow_rect = leftArrow_img.get_rect(topleft =  (60,270))
petWindow_img = pygame.transform.scale(pygame.image.load(os.path.join(CONFIGDIR,"Pet.png")), (360,230))
select_img = pygame.transform.scale(pygame.image.load(os.path.join(CONFIGDIR,"Select.png")), (300,80))
select_rect = select_img.get_rect(topleft=(50,430))

clock = pygame.time.Clock()
running = True
pet_process = False
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            


        if event.type == pygame.MOUSEBUTTONDOWN:
            mousex, mousey =event.pos 
            mousepos = event.pos 
            if select_rect.collidepoint(mousepos):
                if pet_process:
                    pet_process.kill()
               
                print("opened")
                pet_process = subprocess.Popen(['python', script_path])
            if rightArrow_rect.collidepoint(mousepos):
                if selectPet == len(sprites) - 1:
                    
                    selectPet = 0
                else:
                    selectPet += 1
            if leftArrow_rect.collidepoint(mousepos):
                if selectPet == 0:
                    
                    
                    selectPet = len(sprites) - 1
                    
                else:
                    selectPet -= 1                
                
            

    screen.blit(background_img, (0,0))
    screen.blit(rightArrow_img,(240,270))
    screen.blit(leftArrow_img,(60,270))
    screen.blit(petWindow_img,(20,20))
    screen.blit(select_img,(50,430))
    current_sprite = pygame.image.load(os.path.join(os.path.join(SPRITESDIR, sprites[selectPet]), "Display.png"))


    display_height = 210


    original_width = current_sprite.get_width()
    original_height = current_sprite.get_height()
    scale_factor = display_height / original_height
    new_width = int(original_width * scale_factor)
    new_height = display_height


    current_sprite = pygame.transform.scale(current_sprite, (new_width, new_height))


    display_x = 20 + (360 - new_width) // 2 
    display_y = 20 + (230 - new_height) // 2 
    screen.blit(current_sprite, (display_x, display_y))
    
    pygame.display.flip()
    clock.tick(60)
    

         
if pet_process:
    pet_process.kill()
pygame.quit()
