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

pygame.init()

WINDOW = pygame.display.set_mode((0, 0), pygame.NOFRAME)
WIDTH, HEIGHT = WINDOW.get_size()
pygame.display.set_caption("Transparent Overlay")

MAINDIR = os.path.dirname(__file__)
ASSETSDIR = os.path.join(MAINDIR,"Assets")
SPRITEDIR = os.path.join(ASSETSDIR, "Sprites")
EXTRADIR = os.path.join(ASSETSDIR,"Extra")
CONFIGDIR = os.path.join(ASSETSDIR,"Config")

comtxt = os.path.join(CONFIGDIR,"Coms.txt")
hwnd = pygame.display.get_wm_info()["window"]
ctypes.windll.user32.SetWindowLongW(hwnd, -20, ctypes.windll.user32.GetWindowLongW(hwnd, -20) | 0x80000)
transparency_color = (2, 0, 0)
color_key = (transparency_color[2] << 16) | (transparency_color[1] << 8) | transparency_color[0]
ctypes.windll.user32.SetLayeredWindowAttributes(hwnd, color_key, 0, 0x00000001)
sprites = os.listdir(SPRITEDIR)

print(f"Window created: {WIDTH}x{HEIGHT}")
print(f"Window handle: {hwnd}")

talk_list = ["Hello"]
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
STATES = ["walkr","walkl"]
RARESTATES = ["talk","jump","climb"]

bomb_img = pygame.image.load(os.path.join(EXTRADIR,"Explosion.png"))
bomb_img = pygame.transform.scale(bomb_img,(300, 300))
bomb_throw = pygame.image.load(os.path.join(EXTRADIR,"Bomb.png"))
bomb_throw = pygame.transform.scale(bomb_throw,(100,100))
splat_img = pygame.image.load(os.path.join(EXTRADIR, "Splat.png"))
speech_img = pygame.image.load(os.path.join(EXTRADIR,"Speech.png"))
red = ((100,100,100))
speech_img = pygame.transform.scale(speech_img,(WIDTH/15, WIDTH/15))
font = pygame.font.SysFont(None, 50)


bombs = []

class bomb:
    def __init__(self,x,y,vx,vy,timer,power):
        self.x = x
        self.y =y 
        self.vx = vx
        self.vy = vy
        self.timer = timer
        self.power = power 


    def update_pos(self):
      
        self.vy += 0.4
        
        self.x += self.vx
        self.y += self.vy
        
 
        if self.x > WIDTH - 100:
            self.x = WIDTH - 100
            self.vx = -self.vx / 2
        if self.x < 0:
            self.x = 0
            self.vx = -self.vx / 2
        
       
        if self.y >= HEIGHT - 100:
            self.y = HEIGHT - 100
            self.vy = 0
def create_bomb(power, vx,vy,timer,x=None, y=None):
  
    if x is None:
        x = random.randint(50, WIDTH - 50)
    if y is None:
        y = random.randint(0, 200)
    

    
    return bomb(x, y, vx, vy, timer, power)
def update_bombs():
    bombs_to_remove = []
    
    for bomb in bombs:
        if bomb.timer <= 0:
            add_explosion(bomb.x, bomb.y, 100)
            bombs_to_remove.append(bomb)
        
        bomb.timer -= 1
        bomb.update_pos()
        WINDOW.blit(bomb_throw, (bomb.x, bomb.y))
    for bomb in bombs_to_remove:
        bombs.remove(bomb)
        


def read_pet_lines(sprite_folder):
    speech_path = os.path.join(SPRITEDIR,sprite_folder,"Speech.txt")
    default_speech =["Hello","Hi","Play With Me"]
    speech_list = []
    if not os.path.exists(speech_path):
        return default_speech
    try:
        with open(speech_path, 'r') as f:
            content = f.read()
        import re
        speech = re.findall(';([^;]+);', content)
        return speech

    except Exception as e:
        print(f"Error reading speech for {sprite_folder}: {e}")
        return default_speech       
        

def read_size_config(sprite_folder):
    config_path = os.path.join(SPRITEDIR, sprite_folder, "Configuration.txt")  # Fixed indentation
    default_config = {"W": 100, "H": 100, "fps": 10, "speed": 1, "action" : 1, "talk" : True} 
    
    if not os.path.exists(config_path):
        return default_config
    
    try:
        with open(config_path, 'r') as f:
            content = f.read()
        import re
        commands = re.findall(r';([^;]+);', content)
        
        config = default_config.copy()
        for command in commands:
            command = command.strip()
            if '=' in command:
                key, value = command.split('=', 1)
                key = key.strip().lower()
                value = value.strip()
                
                if key == 'w':
                    config['W'] = int(value)
                elif key == 'h':
                    config['H'] = int(value)
                elif key == 'fps':
                    config['fps'] = int(value)
                elif key == 'speed':
                    config['speed'] = float(value)
                elif key == 'action':
                    config['action'] = float(value)
                elif key == 'notalk':
                    config['talk'] = False
        
        return config
    except Exception as e:
        print(f"Error reading config for {sprite_folder}: {e}")
        return default_config
def read_selected_pets():

    selected_file = comtxt
    
    if not os.path.exists(selected_file):
        print("No selected pets file found. Creating all pets.")
        return None
    
    try:
        with open(selected_file, 'r') as f:
            
            selected_pets = [line.strip() for line in f.readlines() if line.strip()]
        
        if not selected_pets:
            print("Selected pets file is empty. Creating all pets.")
            return None
        
        print(f"Selected pets: {selected_pets}")
        return selected_pets
    except Exception as e:
        print(f"Error reading selected pets file: {e}")
        return None
class Desktop_Pet():
    def __init__(self, speed, pack_name, w, h,action_chance,speech, talk, animation_fps=10 ):
        self.name = pack_name
        self.w = w
        self.h = h
        self.talk = talk
        self.action_chance = action_chance
        self.animation_speed = max(1, int(60 / animation_fps))  
        self.frame_counter = 0
        self.speech = speech
        self.pack = os.path.join(SPRITEDIR, pack_name)
        self.idlepack = os.path.join(self.pack, "Idle")
        self.walkpack = os.path.join(self.pack, "Walk")
        self.climbpack = os.path.join(self.pack, "Climb")
        self.fallpack = os.path.join(self.pack, "Fall")
        self.extras = os.path.join(self.pack, "Extras")
        self.flipped = False
        self.possible_states = STATES.copy()
        self.possible_rare = RARESTATES.copy()
        self.img = pygame.image.load(os.path.join(self.idlepack, "1.png")).convert_alpha()
        self.img = pygame.transform.scale(self.img, (w, h))
        self.rare_animations = {}
        try:
            self.rareidlepack = os.path.join(self.pack,"Rare Idle")

        except:
            self.rareidlepack = None
        try:
            self.dead_img = pygame.image.load(os.path.join(self.extras, "Dead.png"))
            self.dead_img = pygame.transform.scale(self.dead_img, (w, h))
            self.dead = False
            self.has_dead_sprite = True
        except:
            self.has_dead_sprite = False
            self.dead = False
        try:
            self.bomb_img = pygame.image.load(os.path.join(self.extras, "Bomb.png"))
            self.bomb_img = pygame.transform.scale(self.bomb_img,(w,h))
            self.bomb = True
            self.possible_rare.append("bomb")
                                                   
        except:
            self.bomb = False
        
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
        self.actiondelay = False
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
        self.original = self.sprite
        self.rot = 0
        self.climb = False
        self.climb_images = []
        self.idle_images = []
        self.animationChoice = None
        files = sorted(
            [f for f in os.listdir(self.walkpack) if f.lower().endswith(('.png', '.jpg', '.jpeg'))],
            key=lambda x: int(''.join(filter(str.isdigit, x)) or 0)
        )
        for file in files:
            img_path = os.path.join(self.walkpack, file)
            img = pygame.image.load(img_path).convert_alpha()
            self.walk_images.append(img)
            
        files = sorted(
            [f for f in os.listdir(self.idlepack) if f.lower().endswith(('.png', '.jpg', '.jpeg'))],
            key=lambda x: int(''.join(filter(str.isdigit, x)) or 0)
        )
        for file in files:
            img_path = os.path.join(self.idlepack, file)
            img = pygame.image.load(img_path).convert_alpha()
            self.idle_images.append(img)

        files = sorted(
            [f for f in os.listdir(self.climbpack) if f.lower().endswith(('.png', '.jpg', '.jpeg'))],
            key=lambda x: int(''.join(filter(str.isdigit, x)) or 0)
        )
                
        for file in files:
            img_path = os.path.join(self.climbpack, file)
            img = pygame.image.load(img_path).convert_alpha()
            self.climb_images.append(img)

        files = sorted(
            [f for f in os.listdir(self.climbpack) if f.lower().endswith(('.png', '.jpg', '.jpeg'))],
            key=lambda x: int(''.join(filter(str.isdigit, x)) or 0)
        )
        self.fall_images = []
        for file in files:
            img_path = os.path.join(self.fallpack, file)
            img = pygame.image.load(img_path).convert_alpha()
            self.fall_images.append(img)
        if self.rareidlepack and os.path.exists(self.rareidlepack):
            for anim_name in os.listdir(self.rareidlepack):
                anim_path = os.path.join(self.rareidlepack, anim_name)
                if os.path.isdir(anim_path):
                   
                    files = sorted(
                        [f for f in os.listdir(anim_path) if f.lower().endswith(('.png', '.jpg', '.jpeg'))],
                        key=lambda x: int(''.join(filter(str.isdigit, x)) or 0)
                    )
                    images = []
                    for file in files:
                        img_path = os.path.join(anim_path, file)
                        img = pygame.image.load(img_path).convert_alpha()
                        images.append(img)
                    if images: 
                        self.rare_animations[anim_name] = images
        
        
        if not self.talk:
            
            self.possible_rare.remove('talk')

        if self.rare_animations != {}:
            self.possible_rare.append('rareidle')
            

        
    def draw(self):
        self.flipped = False
        if self.state == "none":
            if self.on_ground:
                self.frame_counter += 1
                if self.frame_counter % self.animation_speed == 0:
                    if len(self.idle_images) > 0:
                        self.current = (self.current + 1) % len(self.idle_images)
                        self.sprite = self.idle_images[self.current]
                    else:
                        self.sprite = self.img  
                else:

                    if len(self.idle_images) > 0 and self.current < len(self.idle_images):
                        self.sprite = self.idle_images[self.current]
                    else:
                        self.sprite = self.img
            else:
                if self.free:
                    if self.vy > 0:
                        
                    
                        self.frame_counter += 1
                        if self.frame_counter % self.animation_speed == 0:
                            if len(self.fall_images) > 0:
                                self.current = (self.current + 1) % len(self.fall_images)
                                self.sprite = self.fall_images[self.current]
                            else:
                                self.sprite = self.img
                    else:
                        self.sprite = self.img
                else:
                    self.sprite = self.img
    
        elif self.state == "walkl" or (self.x != self.targetx and self.targetx == 0):
            self.frame_counter += 1
            if self.frame_counter % self.animation_speed == 0:
                if len(self.walk_images) > 0:
                    self.current = (self.current + 1) % len(self.walk_images)
                    self.sprite = self.walk_images[self.current]
                else:
                    self.sprite = self.img
            else:
                if len(self.walk_images) > 0 and self.current < len(self.walk_images):
                    self.sprite = self.walk_images[self.current]
                else:
                    self.sprite = self.img
    
        elif self.state == "walkr" or (self.x != self.targetx and self.targetx == self.wallr):
            self.frame_counter += 1
            self.flipped = True
            if self.frame_counter % self.animation_speed == 0:
                if len(self.walk_images) > 0:
                    self.current = (self.current + 1) % len(self.walk_images)
                    self.sprite = self.walk_images[self.current]
                else:
                    self.sprite = pygame.transform.flip(self.img, True, False)
            else:
                if len(self.walk_images) > 0 and self.current < len(self.walk_images):
                    self.sprite = self.walk_images[self.current]
                   
                else:
                    self.sprite = self.img
                    
        elif self.state == "climb":
            if self.x >= self.wallr:
                self.flipped = True
            self.frame_counter += 1
            if self.frame_counter % self.animation_speed == 0:
                if len(self.climb_images) > 0:
                    self.current = (self.current + 1) % len(self.climb_images)
                    self.sprite = self.climb_images[self.current]
                else:
                    self.sprite = self.img
            else:
                if len(self.climb_images) > 0 and self.current < len(self.climb_images):
                    self.sprite = self.climb_images[self.current]
                else:
                    self.sprite = self.img
        elif self.state == "rareidle":
            if self.animationChoice is not None:
                self.animationChoice = random.choice(list(self.rare_animations.keys()))
                self.current = 0

                if self.animationChoice in self.rare_animations:
                        anim_frames = self.rare_animations[self.animationChoice]
                        if anim_frames:
                            self.frame_counter += 1
                            if self.frame_counter % self.animation_speed == 0:
                                self.current = (self.current + 1) % len(anim_frames)
                            
                            self.sprite = anim_frames[self.current]
                        else:
                            self.sprite = self.img
                else:
                    self.sprite = self.img
            
                
            
        if self.state == "dead":
            self.sprite = self.dead_img
        if self.state == "bomb":
            self.sprite = self.bomb_img
        
            
        self.sprite = pygame.transform.scale(self.sprite, (self.w, self.h))
        if self.flipped:
            self.sprite = pygame.transform.flip(self.sprite, True, False)
            
        WINDOW.blit(self.sprite, (self.x, self.y))
            
                

      
    def update_state(self):
       
        self.rect = self.sprite.get_rect(topleft=(self.x, self.y))
        
        if self.free:
            if self.state in ("none", "jump","dead"):
                if self.y < self.ground or self.state == "jump":
                    self.y += self.vy
                    self.vy += 0.4
                    
                
                if self.y >= self.ground and self.state != "jump": 
                    if self.vy >= 100:
                        if self.has_dead_sprite:
                            if self.dead == False:
                                self.dead = True
                            if self.dead:
                                add_splat(self.x,self.y)
                    self.y = self.ground  
                        
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
            if self.has_dead_sprite:
                if self.dead:
                    self.state = "dead"
                
            
            if self.state == "none":
                if self.delay_timer == 0:
                    self.delay = False
                if not self.delay:
                    
                    
                    if self.on_ground:
                        new_state = random.randint(1, 1000)
                        if new_state < (101*self.action_chance):
                            new_state = random.choice(self.possible_rare)
                            if new_state == "bomb":
                                new_state = random.choice(self.possible_rare)
                            
                            
                        else:
                            new_state = random.choice(self.possible_states)
                        self.state = new_state
                        self.random = random.randint(1,1000)
                        self.current = 0
                    
                else:
                    self.delay_timer -= 1
            
                
                
                
                    
                    
                    
            
        else:
            
            self.y = mousey - (self.height/2)
            self.x = mousex - (self.width/2)
            if not self.dead:
                self.state = "none"
            self.on_ground = False
            self.delay_timer = 240
            self.delay = True
            self.targetx = None
            self.targety = None
            self.current = 0
            self.climb = False
            actiondelay = False

            self.vx = 0
            self.vy = 0

        
            


    def reset_action(self):
        self.state = "none"
        self.delay = True
        self.current = 0
        self.targetx = None
        self.targety = None
        self.actiondelay = False
        self.delay_timer = 120
        self.climb = False
        self.jump_state = 0
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
                self.reset_action()
        elif self.state == "jump":
            if self.name == "CappyBara":
                
                self.sprite = pygame.transform.rotate(self.sprite,90)
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
                    self.reset_action()
        elif self.state == "climb":
            if not self.climb:
                choice = random.randint(1,2)

                if choice == 1:
                    self.climb = True
                    self.targety = random.randint(1,HEIGHT)
                    self.targetx = 0
                if choice == 2:
                    self.targety = random.randint(1,HEIGHT)
                    self.targetx = self.wallr
                    self.climb = True
            else:
                if self.x != self.targetx:
                    if self.targetx >= self.x and self.targetx == 0:
                        self.x = 0
                    elif self.targetx == 0:
                        self.x -= self.speed

                    elif self.targetx <= self.x and self.targetx == self.wallr:
                        self.x = self.wallr
                    elif self.targetx == self.wallr:
                        self.x  += self.speed

                else:
                    if self.y <= self.targety:

                        
                        self.y = self.targety
                    else:
                        self.y -= self.speed

            if self.y == self.targety and self.x == self.targetx:
                nexttarget = 2
                if self.delay and self.delay_timer <= 0:
                    nexttarget = 1

                if nexttarget == 1:
                    self.state = "none"
                    if self.targetx == 0:
                        self.vx = 5
                        self.vy = -5
                    if self.targetx == self.wallr:
                        self.vx = -5
                        self.vy = -5
                    self.targetx = None
                    self.targety = None
                    self.climb = False
                    self.delay_timer = 120
                    self.delay = True
                if nexttarget == 2:
                    if not self.delay:
                        
                    
                   
                        self.delay_timer = random.randint(60,120)
                        
                        self.delay = True
                    elif self.delay:
                        self.delay_timer -= 1

        elif self.state == "bomb":
            explode = False
            
            if self.actiondelay:
                self.delay_timer -= 1
                if self.delay_timer <= 0:
                    self.delay_timer = 0
                    self.actiondelay = False
                    explode = True
            elif not self.actiondelay:
                self.actiondelay = True
                self.delay_timer = 240
            if explode:

                explodey = -random.randint(10,30)
                    
                explode_dir = random.randint(1,2)
                if explode_dir == 1:
                    explodex = -random.randint(1,20)
                else:
                    explodex = random.randint(1,20)
                    
                bombs.append(create_bomb(
                        random.randint(1,500),
                        explodex,
                        explodey,
                        random.randint(1,90),
                        x=self.x,
                        y=self.y
                    ))
                
                
                self.reset_action()
        if self.state == "rareidle":
            if self.actiondelay:
                self.delay_timer -= 1
                if self.delay_timer <= 0:
                    self.delay_timer = 0
                    self.actiondelay = False
                    self.reset_action()
            elif not self.actiondelay:
                self.actiondelay = True
                self.delay_timer = 240
                
                
        if self.state == "talk":
            add_speech(self.x + self.width/2,self.y-self.height/4,(random.choice(self.speech)))
            self.state = "none"
            self.delay = True
            self.delay_timer = 120
            print("talk")
                
                        
                            
     
    
    def is_clicked(self, mousepos):
        """Check if clicking on non-transparent part of sprite"""
        if not self.rect.collidepoint(mousepos):
            return False
        
        local_x = mousepos[0] - self.rect.x
        local_y = mousepos[1] - self.rect.y
        
        if 0 <= local_x < self.mask.get_size()[0] and 0 <= local_y < self.mask.get_size()[1]:
            return self.mask.get_at((int(local_x), int(local_y)))
        return False
   
selected_pets = read_selected_pets()
for sprite_folder in sprites:
    sprite_path = os.path.join(SPRITEDIR, sprite_folder)
    if os.path.isdir(sprite_path):
        if selected_pets is None or sprite_folder in selected_pets:
            try:
                config = read_size_config(sprite_folder)
                phrase = read_pet_lines(sprite_folder)
                pet = Desktop_Pet(
                    speed=config['speed'],
                    pack_name=sprite_folder,
                    w=config['W'],
                    h=config['H'],
                    animation_fps=config['fps'],
                    action_chance=config['action'],
                    speech = phrase,
                    talk = config['talk']
                )
                print(f"Created pet: {sprite_folder} (Size: {config['W']}x{config['H']}, FPS: {config['fps']})")
            except Exception as e:
                print(f"Failed to create pet for {sprite_folder}: {e}")
        else:
            print(f"Skipped pet: {sprite_folder} (not selected)")
def check_click(mousepos):
    for pet in petList:
        if pet.is_clicked(mousepos):
            pet.free = False
            return
        else:
            pet.free = True
splatList = []
def add_splat(x,y):
    
    x -= (WIDTH/20)
    y -= (HEIGHT/20)
    
    
    
    splatList.append((x,y))
    print(splatList)

def draw_splat():
    for splat in splatList:
        x, y = splat
        WINDOW.blit(splat_img,(x,y))

explodeList = []
def add_explosion(x,y,w):
    x -= 150
    x += w/2
    y -= 150
    explodeList.append((x,y))
def draw_explosion():
    for explode in explodeList:
        x, y = explode
        WINDOW.blit(bomb_img,(x,y))
speechList = []
def add_speech(x,y,msg, duration = 120):
    speechList.append([str(msg),x,y,duration])



def draw_speech():
    for speech in speechList[:]:
        if speech[3] <= 0:
            speechList.remove(speech)
        else:
            speech[3] -= 1
    for speech in speechList[:]:
        text_surface = font.render(speech[0], True, ((0,0,0)))
        text_rect = text_surface.get_rect(center=(speech[1], speech[2]))
        WINDOW.blit(text_surface, text_rect)
        
 
            
clock = pygame.time.Clock()
FPS = 60

print("Window running. Press ESC to exit.")

running = True
mousex, mousey = 0, 0
hacker = []
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
            if event.key == pygame.K_h:
                hacker = []
                hacker.append('h')
            if event.key == pygame.K_a:
                if hacker == ['h']:
                    hacker = ['h','a']
            if event.key == pygame.K_c:
                if hacker == ['h','a']:
                    hacker = ['h','a','c']
            if event.key == pygame.K_k:
                if hacker == ['h','a','c']:
                    hacker = ['h','a','c','k']
                
                
    
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
    draw_explosion()
    for i in petList:
        if not i.free:
            if dy >= 50:
                if dy >= 100:
                    if i.has_dead_sprite:
                        
                        i.dead = True
        
       
        if i.dead and i.y >= i.ground and (i.vy >= 100 or (dy >=10 and not i.free)):
            add_splat(i.x, i.y)
        
        i.update_state()
        i.draw()
        i.action()


    if hacker == ['h','a','c','k']:
        answer = input("Enter Command")
    


        for pet in petList:
            if answer in pet.possible_states or answer in pet.possible_rare:
                pet.state = answer
                print(f"Set {pet.name} state to {answer}")
            else:
                print(f"Command {answer} is not a valid command for {pet.name}")
                
        
            
        
        hacker = []
        ##print(i.pack + " " + i.state)
    draw_speech() 
    draw_splat()
    update_bombs()
    pygame.display.flip()
    clock.tick(FPS)
    

pygame.quit()



