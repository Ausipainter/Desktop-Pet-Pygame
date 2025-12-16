🐾 Desktop Pet (Pygame)
A customizable desktop pet made with Pygame!
You can easily add your own pets by dropping sprite files into the project—no code changes required.

✨ Features
Animated desktop pets

Easy sprite customization

Configurable size and animation speed

Simple file-based setup


📁How to add a Custom Pet


To add your own pet:

  Navigate to:
  
   Assets/Sprites/
   
Create a new folder with your pet’s name.

Inside that folder, add:
  A Sprites folder
  A Configuration.txt file


🎞️ Sprite Requirements

  Your pet’s sprite folder must contain the following structure:
  
PetName/
├── Sprites/
│   ├── idle/
│   │   ├── 1.png
│   │   ├── 2.png
│   │   └── ...
│   ├── walk/
│   │   ├── 1.png
│   │   ├── 2.png
│   │   └── ...
├── Configuration.txt

Animation Rules

Frames must be numbered starting at 1

Idle and walking animations are required

All frames should be the same size


  
⚙️ Configuration File

Each pet must include a Configuration.txt file.
This file allows you to customize how your pet looks and animates.

Command Format:
  ;cmd = value;

Example:
  ;W = 100;


🛠️ Available Commands:
  W   Sets sprite width(pixels)
  H   Sets sprite height(pixels)
  fps Sets animation speed (fps)
  


🔧 Default Settings

If no configuration is provided, pets will use:

Width: 100 pixels

Height: 100 pixels

FPS: 10



📚 Example Pet

For a complete working example, check out:

Assets/Sprites/CappyBara/


This folder demonstrates:

Correct sprite structure

Proper animation setup

Example configuration commands
