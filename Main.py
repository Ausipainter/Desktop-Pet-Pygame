import subprocess
import sys
import os

def install_and_import(package_name, import_name=None):
    """Install a package and return True if successful"""
    if import_name is None:
        import_name = package_name
    
    try:
        __import__(import_name)
        return True
    except ImportError:
        print(f"\n{package_name} not found. Installing...")
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", package_name])
            print(f"✓ {package_name} installed successfully!")
            return True
        except subprocess.CalledProcessError as e:
            print(f"✗ Failed to install {package_name}: {e}")
            return False

# Install packages if needed
print("Checking required packages...")

pygame_ok = install_and_import('pygame')
pywin32_ok = True

if sys.platform == 'win32':
    pywin32_ok = install_and_import('pywin32', 'win32gui')

if not pygame_ok or not pywin32_ok:
    print("\n" + "="*60)
    print("ERROR: Failed to install required packages")
    print("="*60)
    print("\nPlease install manually:")
    if not pygame_ok:
        print("    pip install pygame")
    if not pywin32_ok:
        print("    pip install pywin32")
    print("="*60)
    input("\nPress Enter to exit...")
    sys.exit(1)

# Now import everything
import pygame
if sys.platform == 'win32':
    import win32gui
    import win32con
import ctypes
import threading
import time
import random

print("\n✓ All required packages loaded successfully!\n")

MAINDIR = os.path.dirname(os.path.abspath(__file__))
ASSETSDIR = os.path.join(MAINDIR, "Assets")
CONFIGDIR = os.path.join(ASSETSDIR, "Config")
comtxt = os.path.join(CONFIGDIR, "Coms.txt")

# Create directories if they don't exist
os.makedirs(CONFIGDIR, exist_ok=True)

with open(comtxt, 'w') as f:
    pass

SPRITESDIR = os.path.join(ASSETSDIR, "Sprites")

# Check if sprites directory exists
if not os.path.exists(SPRITESDIR):
    print(f"ERROR: Sprites directory not found at {SPRITESDIR}")
    input("Press Enter to exit...")
    sys.exit(1)

sprites = [s for s in os.listdir(SPRITESDIR) if os.path.isdir(os.path.join(SPRITESDIR, s))]
if not sprites:
    print(f"ERROR: No sprite folders found in {SPRITESDIR}")
    input("Press Enter to exit...")
    sys.exit(1)

pygame.init()
screen = pygame.display.set_mode((400, 700))
WIDTH = 400
HEIGHT = 700
pygame.display.set_caption("Configuration")
print(f"Found {len(sprites)} sprites: {sprites}\n")

script_path = os.path.join(MAINDIR, "Pet.py")

selectPet = 0

# Load images with error checking
try:
    background_img = pygame.transform.scale(
        pygame.image.load(os.path.join(CONFIGDIR, "Background.png")), 
        (WIDTH, HEIGHT)
    )
    background_rect = background_img.get_rect()
    
    rightArrow_img = pygame.transform.scale(
        pygame.image.load(os.path.join(CONFIGDIR, "Arrow.png")), 
        (100, 100)
    )
    rightArrow_rect = rightArrow_img.get_rect(topleft=(240, 270))
    
    leftArrow_img = pygame.transform.flip(
        pygame.transform.scale(
            pygame.image.load(os.path.join(CONFIGDIR, "Arrow.png")), 
            (100, 100)
        ), 
        True, False
    )
    leftArrow_rect = leftArrow_img.get_rect(topleft=(60, 270))
    
    petWindow_img = pygame.transform.scale(
        pygame.image.load(os.path.join(CONFIGDIR, "Pet.png")), 
        (360, 230)
    )
    
    select_img = pygame.transform.scale(
        pygame.image.load(os.path.join(CONFIGDIR, "Select.png")), 
        (300, 80)
    )
    select_rect = select_img.get_rect(topleft=(50, 430))
    
    print("✓ All configuration images loaded successfully!")
    
except pygame.error as e:
    print(f"\nERROR: Could not load config images: {e}")
    print(f"Make sure all required images are in: {CONFIGDIR}")
    print("\nRequired images:")
    print("  - Background.png")
    print("  - Arrow.png")
    print("  - Pet.png")
    print("  - Select.png")
    input("\nPress Enter to exit...")
    pygame.quit()
    sys.exit(1)

clock = pygame.time.Clock()
running = True
pet_process = None

print("\n✓ Configuration window is now running!")
print("Use the arrows to select a pet, then click the select button.\n")

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            mousepos = event.pos 
            
            if select_rect.collidepoint(mousepos):
                if pet_process:
                    print("Closing previous pet...")
                    try:
                        pet_process.kill()
                    except:
                        pass
               
                print(f"Launching pet: {sprites[selectPet]}...")
                try:
                    pet_process = subprocess.Popen([sys.executable, script_path])
                    
                    with open(comtxt, 'w') as f:
                        f.write(sprites[selectPet])
                    print("✓ Pet launched successfully!")
                except Exception as e:
                    print(f"✗ Error launching pet: {e}")
                    
            if rightArrow_rect.collidepoint(mousepos):
                if selectPet == len(sprites) - 1:
                    selectPet = 0
                else:
                    selectPet += 1
                print(f"Selected: {sprites[selectPet]}")
                    
            if leftArrow_rect.collidepoint(mousepos):
                if selectPet == 0:
                    selectPet = len(sprites) - 1
                else:
                    selectPet -= 1
                print(f"Selected: {sprites[selectPet]}")

    screen.blit(background_img, (0, 0))
    screen.blit(rightArrow_img, (240, 270))
    screen.blit(leftArrow_img, (60, 270))
    screen.blit(petWindow_img, (20, 20))
    screen.blit(select_img, (50, 430))
    
    try:
        current_sprite_path = os.path.join(SPRITESDIR, sprites[selectPet], "Display.png")
        if os.path.exists(current_sprite_path):
            current_sprite = pygame.image.load(current_sprite_path)

            display_height = 210
            original_width = current_sprite.get_width()
            original_height = current_sprite.get_height()
            
            if original_height > 0:
                scale_factor = display_height / original_height
                new_width = int(original_width * scale_factor)
                new_height = display_height

                current_sprite = pygame.transform.scale(current_sprite, (new_width, new_height))

                display_x = 20 + (360 - new_width) // 2 
                display_y = 20 + (230 - new_height) // 2 
                screen.blit(current_sprite, (display_x, display_y))
        else:
            # Draw a placeholder if Display.png is missing
            font = pygame.font.Font(None, 36)
            text = font.render("No Preview", True, (255, 255, 255))
            text_rect = text.get_rect(center=(200, 135))
            screen.blit(text, text_rect)
            
    except Exception as e:
        print(f"Error loading sprite {sprites[selectPet]}: {e}")
    
    pygame.display.flip()
    clock.tick(60)

print("\nClosing configuration window...")
if pet_process:
    print("Stopping pet process...")
    try:
        pet_process.kill()
    except:
        pass
pygame.quit()
print("Goodbye!")
