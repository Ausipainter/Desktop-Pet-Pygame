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
screen = pygame.display.set_mode((400,700))
WIDTH = 400
HEIGHT = 700
pygame.display.set_caption("Configuration")


script_path = os.path.join(MAINDIR,"Pet.py")




background_img = pygame.transform.scale(pygame.image.load(os.path.join(CONFIGDIR,"Background.png")), (WIDTH,HEIGHT))
background_rect = background_img.get_rect()
rightArrow_img = pygame.transform.scale(pygame.image.load(os.path.join(CONFIGDIR,"Arrow.png")), (100,100))
rightArrow_rect = rightArrow_img.get_rect()
leftArrow_img = pygame.transform.flip(pygame.transform.scale(pygame.image.load(os.path.join(CONFIGDIR,"Arrow.png")), (100,100)),True, False)
leftArrow_rect = leftArrow_img.get_rect()
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
                
            

    screen.blit(background_img, (0,0))
    screen.blit(rightArrow_img,(240,270))
    screen.blit(leftArrow_img,(60,270))
    screen.blit(petWindow_img,(20,20))
    screen.blit(select_img,(50,430))
    pygame.display.flip()
    clock.tick(60)
    

         
if pet_process:
    pet_process.kill()
pygame.quit()
