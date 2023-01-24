# A screen reading tool for videogames

In many videogames, the use of the mouse for controlling the camera is often used. On the other hand, the magnifier app which makes the elements on the screen appear larger, also makes use of the movement of the mouse to move arround the screen. These two behaviours collide between each oder if they wanna be performed simultaniously. In other words, while playing a videogame one is not able to use the magnifier app and mouve the mouse around the screen. 
This is the main reason why I wanted to build an application to help me read what's on the screen by using text-to-speech.

## Usage
When it comes to usage, it can be used by everyone. However, people having some kind of visual imparement will benefit the most from using it. Furthurmore, this application could also serve as inspiration for encouraging game developers to include this kind of accessibility feature inside their games. 

## Application demo
In the following video it is shown how the application works:
1. It starts by scanning the content of the screen.
2. Once scanned, the user can switch between all detected text bounding boxes.
3. When the read out loud key is pressed the text inside the selected bounding box is read. 

https://user-images.githubusercontent.com/13052324/214283712-3282a405-70bc-4821-b365-ccd43e37dae7.mp4


## Requirements & installation
- **OS**: Currently, the application is only available for Windows, since the majority of videogames are played in this OS. 

- **Suported languages**: English and Spaniash

## How to use?
Frist and foremost, custom key bindings must be defined. To do so, edit the file `config/keys.json`. Here there's a description of what's the role of each key.
Keys descriptions:

`"CAPTURE":` This key will take a screenshot

`"SWITCH_FORWARD":` Move to the next detection 

 `"SWITCH_BACKWARD":` Move to previous detection
 
 `"REPEAT":` Repeat text at a slower pase 
 
 `"READ_OUT_LOUD":` Text-to-speech 
 
 `"QUIT":` Exit key. It will clear the screen aswell

> NOTE: Key binding names must be in the same language as your OS.

## Known issues (Work in progress)
- Fullscreen issues with some games.
- Sometimes while display is loaded, clicking on the top part of the screen, app crashes

## Future work
- [ ] Update documentation
- [ ] Key binder UI
- [ ] More realistic TTS voices
- [ ] Speeding up OCR
