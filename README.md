<h1>🐾 Desktop Pet (Pygame)</h1>

A customizable desktop pet made with Pygame!

You can easily add your own pets by dropping sprite files into the project—no code changes required.

✨ Features

>Animated desktop pets
>
>Easy sprite customization
>
>Configurable size and animation speed
>
>Simple file-based setup


📁How to add a Custom Pet


To add your own pet:

&emsp;&emsp;Navigate to:
  
&emsp;&emsp;&emsp;Assets/Sprites/
   
&emsp;&emsp;Create a new folder with your pet’s name.

&emsp;&emsp;Inside that folder, add:

&emsp;&emsp;&emsp; A Sprites folder
  
&emsp;&emsp;&emsp;A Configuration.txt file

 &emsp;&emsp;&emsp;A Display.png image

&emsp;&emsp;&emsp;A Walk folder

&emsp;&emsp;&emsp;A Idle folder 

&emsp;&emsp;Inside of walk and idle folders add your animation images(see animation Rules below) 
  
&emsp;&emsp;Even if you do not have an animation for them you must have at least one image in each
  


🎞️ Sprite Requirements

&emsp;Your pet’s sprite folder must contain the following structure:
  
&emsp;&emsp;PetName/Sprites/idle/1.png, 2.png....

&emsp;&emsp;&emsp;PetName/Sprites/walk/1.png, 2.png....

&emsp;&emsp;&emsp;PetName/Configuration.txt 

&emsp;&emsp;&emsp;PetName/Display.png

(Display.png is used to display the pet in the selection menu)



Animation Rules

&emsp;&emsp;Frames must be numbered starting at 1

&emsp;&emsp;Idle and walking animations are required

&emsp;&emsp;All frames should be the same size


  
⚙️ Configuration File

&emsp;Each pet must include a Configuration.txt file.

&emsp;&emsp;&emsp;This file allows you to customize how your pet looks and animates.

&emsp;&emsp;Command Format:

  &emsp;&emsp;&emsp;;cmd = value;

&emsp;&emsp;Example:

  &emsp;&emsp;&emsp;;W = 100;


🛠️ Available Commands:

 &emsp;&emsp;W   Sets sprite width(pixels)
  
  &emsp;&emsp;H   Sets sprite height(pixels)
  
 &emsp;&emsp;fps Sets animation speed (fps)
  


🔧 Default Settings

If no configuration is provided, pets will use:

&emsp;&emsp;Width: 100 pixels

&emsp;&emsp;Height: 100 pixels

&emsp;&emsp;FPS: 10



📚 Example Pet

For a complete working example, check out:

Assets/Sprites/CappyBara/


This folder demonstrates:

&emsp;&emsp;Correct sprite structure

&emsp;&emsp;Proper animation setup

&emsp;&emsp;Example configuration commands
