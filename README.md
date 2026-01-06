<h1>🐾 Desktop Pet (Pygame)</h1>

A customizable desktop pet made with Pygame!

You can easily add your own pets by dropping sprite files into the project—no code changes required.

<h1>✨ Features</h1>

Animated desktop pets

Easy sprite customization

Configurable size and animation speed

Simple file-based setup


<h1>📁How to add a Custom Pet</h1>


To add your own pet:

&emsp;Navigate to:
  
&emsp;&emsp;Assets/Sprites/
   
&emsp;Create a new folder with your pet’s name.

&emsp;Inside that folder, add:

&emsp;&emsp;A Sprites folder
  
&emsp;&emsp;A Configuration.txt file (Optional)

 &emsp;&emsp;A Speech.txt file (Optional)

 &emsp;&emsp;A Display.png image

&emsp;&emsp;A Walk folder

&emsp;&emsp;A Idle folder 

&emsp;&emsp;A Climb folder 

&emsp;&emsp;A Fall folder 

&emsp;Inside of walk, climb, fall, and idle folders add your animation images(see animation Rules below) 
  
&emsp;Even if you do not have an animation for them you must have at least one image in each
  


<h1>🎞️ Pet Requirements</h1>

&emsp;Your pet’s sprite folder must contain the following structure:
  
&emsp;&emsp;PetName/Sprites/Idle/1.png, 2.png....

&emsp;&emsp;PetName/Sprites/Walk/1.png, 2.png....

&emsp;&emsp;PetName/Sprites/Climb/1.png, 2.png....

&emsp;&emsp;PetName/Sprites/Fall/1.png, 2.png....

&emsp;&emsp;PetName/Configuration.txt 

&emsp;&emsp;PetName/Display.png

(Display.png is used to display the pet in the selection menu and is not required)



<h1>Animation Rules</h1>

Frames must be numbered starting at 1

Idle and walking animations are required

All frames should be the same size


  
<h1>⚙️ Configuration File</h1>

&emsp;You may include a Configuration.txt file if you want to change pet setings using command given below (recommended for non included pets)


&emsp;&emsp;&emsp;This file allows you to customize how your pet looks and animates.

&emsp;Command Format:

&emsp;&emsp;;cmd = value;

&emsp;Example:

&emsp;&emsp;;W = 100;


<h1>🛠️ Available Commands:</h1>

W  : Sets sprite width(pixels)
  
H  : Sets sprite height(pixels)
  
fps : Sets animation speed (fps)
  
speed : Sets pet speed

action : Directly coorelates to rare actions (talking, climbing, jumping)

notalk : Dissable pet speech (Don't set to a number)


<h1>🔧 Default Settings</h1>

If no configuration is provided, pets will use:

&emsp;Width: 100 pixels

&emsp;Height: 100 pixels

&emsp;FPS: 10

&emsp;speed: 1

&emsp;action: 1

<h1>⚙️ Speech File</h1>
&emsp;You may add speech files to any pet you want

&emsp;Similarly to commands any text you want your pet to "say" must be surrounded by two ;

&emsp;Example:

&emsp;&emsp;;Hello;

&emsp;This will make the pet have a chance to say Hello. You can have as many voice lies as you want

<h1>🔧 Default Settings</h1>

&emsp;If no speech is provided, the pet will choose from a list of three things on what it says(Hi, Hello, Play with me)


<h1>📚 Example Pet</h1>

For a complete working example, check out:

Assets/Sprites/CappyBara/


This folder demonstrates:

&emsp;Correct sprite structure

&emsp;Proper animation setup

&emsp;Example configuration commands
