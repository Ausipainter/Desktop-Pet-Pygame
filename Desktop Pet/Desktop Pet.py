
import pygame
import ctypes
import threading
import time
import win32gui
import win32con
import os
import random
# Initialize Pygame
pygame.init()

# Create fullscreen window
WINDOW = pygame.display.set_mode((0, 0), pygame.NOFRAME)
WIDTH, HEIGHT = WINDOW.get_size()
pygame.display.set_caption("Transparent Overlay")

MAINDIR = os.path.dirname(__file__)
SPRITEDIR = os.path.join(MAINDIR, "Sprites")



# Get window handle
hwnd = pygame.display.get_wm_info()["window"]

# Make window layered
ctypes.windll.user32.SetWindowLongW(hwnd, -20, ctypes.windll.user32.GetWindowLongW(hwnd, -20) | 0x80000)

# Use color-key transparency
transparency_color = (2, 0, 0)
color_key = (transparency_color[2] << 16) | (transparency_color[1] << 8) | transparency_color[0]
ctypes.windll.user32.SetLayeredWindowAttributes(hwnd, color_key, 0, 0x00000001)

# Don't make window click-through - we need to receive clicks on the sprite
# The layered window with color key will handle transparency visually

print(f"Window created: {WIDTH}x{HEIGHT}")
print(f"Window handle: {hwnd}")

# Thread to keep window on top
def keep_on_top():
    while True:
        try:
            win32gui.SetWindowPos(hwnd, win32con.HWND_TOPMOST, 0, 0, 0, 0, win32con.SWP_NOSIZE | win32con.SWP_NOMOVE)
            time.sleep(0.1)
        except:
            pass

top_thread = threading.Thread(target=keep_on_top, daemon=True)
top_thread.start()

petList = []
STATES = ["none","jump","walkl","walkr"]
 

class Desktop_Pet():
    def __init__(self,speed,pack_name,count,w,h):

        self.w = w
        self.h = h
        
        self.frame_counter = count
        self.pack = os.path.join(SPRITEDIR,pack_name)
        self.idlepack = os.path.join(self.pack,"Idle")
        self.walkpack = os.path.join(self.pack, "Walk")
        self.img = pygame.image.load(os.path.join(self.idlepack,"1.png")).convert_alpha()
        self.img = pygame.transform.scale(self.img,(w,h))
        
        self.mask = pygame.mask.from_surface(self.img)
        self.sprite = self.img
        self.width = self.img.get_width()
        self.height = self.img.get_height()
        
        self.x = 0
        self.y = 0
        self.vx = 10
        self.vy = 0
        self.free = True
        self.rect = self.sprite.get_rect()
        petList.append(self)

        self.state = "none"
        self.on_ground = False
        self.random = 1
        self.targetx = None
        self.targety = None
        self.delay = False
        self.delay_timer = 2000
        self.speed = speed
        self.current = 0
        self.walk_images = []
        self.ground = HEIGHT - self.height
        self.wallr = WIDTH - self.width
        self.jump_state = 0 
        
        self.idle_images = []
        files = sorted(
            [f for f in os.listdir(self.walkpack) if f.lower().endswith(('.png','.jpg','.jpeg'))],
            key = lambda x: int(''.join(filter(str.isdigit, x)) or 0)
            )
        for file in files:
            img_path = os.path.join(self.walkpack, file)
            img = pygame.image.load(img_path).convert_alpha()
            self.walk_images.append(img)
            
        files = sorted(
            [f for f in os.listdir(self.idlepack) if f.lower().endswith(('.png','.jpg','.jpeg'))],
            key = lambda x: int(''.join(filter(str.isdigit, x)) or 0)
            )
        for file in files:
            img_path = os.path.join(self.idlepack, file)
            img = pygame.image.load(img_path).convert_alpha()
            self.idle_images.append(img)

        
        

        
        
    def draw(self):
        if self.state == "none":
            if self.on_ground:
                
                self.frame_counter += 1
                if self.frame_counter % 5 == 0:  
                    self.current = (self.current + 1) % len(self.idle_images)
                self.sprite = self.idle_images[self.current]
            else:
                self.sprite = self.img

        elif self.state == "walkl":
            self.frame_counter += 1
            if self.frame_counter % 5 == 0:  
                self.current = (self.current + 1) % len(self.walk_images)
            self.sprite = self.walk_images[self.current]

        elif self.state == "walkr":
            self.frame_counter += 1
            if self.frame_counter % 5 == 0:  
                self.current = (self.current + 1) % len(self.walk_images)
            self.sprite = pygame.transform.flip(self.walk_images[self.current], True, False)

        self.sprite = pygame.transform.scale(self.sprite,(self.w,self.h))
        
            
            
        
        WINDOW.blit(self.sprite, (self.x, self.y))
            
                

      
    def update_state(self):
       
        self.rect = self.sprite.get_rect(topleft=(self.x, self.y))
        
        if self.free:
            if self.state in ("none", "jump"):
                if self.y < self.ground or self.state == "jump":
                    self.y += self.vy
                    self.vy += 0.4
                elif self.y != self.ground:
                    self.y = self.ground
                    if not self.state == "jump":
                        self.vy = 0
                
                
                self.x += self.vx
                if self.x > self.wallr:
                    self.x = self.wallr
                    self.vx = -self.vx / 2
                if self.x < 0:
                    self.x = 0
                    self.vx = -self.vx / 2
                    
                if self.vx > 0:
                    self.vx -= 0.01
                    if self.on_ground:
                        self.vx -= self.vx/20
                elif self.vx < 0:
                    self.vx += 0.01
                    if  self.on_ground:
                        self.vx -= self.vx/20
                else:
                    self.vx = 0

            if self.y >= self.ground:
                self.on_ground = True

            else:
                self.on_ground = False

            if self.state == "none":
                if self.delay_timer == 0:
                    self.delay = False
                if not self.delay:
                    
                    if self.on_ground:
                        new_state = random.randint(1, 1000)
                        if new_state < 101:
                            new_state = "jump"
                        elif new_state < 551:
                            new_state = "walkl"
                        else:
                            new_state = "walkr"
                        if new_state != "none":
                            self.current = 0
                        self.state = new_state
                        self.random = random.randint(1,1000)
                    
                else:
                    self.delay_timer -= 1
            
                
                
                
                    
                    
                    
            
        else:
            
            self.y = mousey - (self.height/2)
            self.x = mousex - (self.width/2)
            self.state = "none"
            self.on_ground = False
            self.delay_timer = 240
            self.delay = True
            self.targetx = None
            self.targety = None
            self.current = 0

            self.vx = 0
            self.vy = 0

        
            


            
    def action(self):
        if self.state == "none":
            return
        if self.state == "walkl":
            if self.targetx is None:
                self.targetx = self.x - self.random
            if self.targetx <= 0:
                self.targetx = 0 
            
            self.x -= self.speed
            self.vx = 0
            if self.x <= self.targetx:
                    self.x = self.targetx
                    self.state = "none"
                    self.targetx = None
                    self.delay_timer = 120
                    self.delay = True
                    self.current = 0
                    return
        elif self.state == "walkr":
            if self.targetx is None:
                self.targetx = self.x + self.random
            if self.targetx >= WIDTH - self.width:
                self.targetx = WIDTH - self.width
            self.x += self.speed
            self.vx = 0
            
            if self.x >= self.targetx:
                self.x = self.targetx
                self.state = "none"
                self.targetx = None
                self.delay_timer = 120
                self.delay = True
                self.current = 0
        elif self.state == "jump":
            if self.jump_state == 0:
                if random.randint(1,2) == 2:
                    self.vx = random.randint(1,20)
                    self.vy = -random.randint(1,20)
                    
                    
                else:
                    self.vx = -random.randint(1,20)
                    self.vy = -random.randint(1,20) 
                    
                print("jump")
                

                self.jump_state = 1

            elif self.jump_state == 1:
                if self.on_ground:
                    self.jump_state = 0
                    self.state = "none"
                    self.delay_timer = 120
                    self.delay = True
                    self.current = 0


            
                    
                
                
            

            
        
                    
            
            
            
    
    def is_clicked(self, mousepos):
        """Check if clicking on non-transparent part of sprite"""
        if not self.rect.collidepoint(mousepos):
            return False
        
        local_x = mousepos[0] - self.rect.x
        local_y = mousepos[1] - self.rect.y
        
        if 0 <= local_x < self.mask.get_size()[0] and 0 <= local_y < self.mask.get_size()[1]:
            return self.mask.get_at((int(local_x), int(local_y)))
        return False
   


###slime = Desktop_Pet(86,65,1,"Slime",10)
llama = Desktop_Pet(1,"LLama", 6,100,100)
##man = Desktop_Pet(1,"Man",4,100,100)


def check_click(mousepos):
    for pet in petList:
        if pet.is_clicked(mousepos):
            pet.free = False
            return

# Clock for FPS
clock = pygame.time.Clock()
FPS = 60

print("Window running. Press ESC to exit.")

running = True
mousex, mousey = 0, 0

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
    
        if event.type == pygame.MOUSEBUTTONDOWN:
            mousex, mousey = pygame.mouse.get_pos()
            check_click((mousex, mousey))
        elif event.type == pygame.MOUSEBUTTONUP:
            for pet in petList:
                pet.free = True
        
        if event.type == pygame.MOUSEMOTION:
            dx, dy = event.rel
            mousex, mousey = pygame.mouse.get_pos()
            for desktoppet in petList:
                if not desktoppet.free:
                    desktoppet.vx, desktoppet.vy = dx, dy
 
    WINDOW.fill((2, 0, 0))
    for i in petList:
        i.update_state()
        i.draw()
        i.action()
    
    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()


