# Gaming Narrator

In many videogames, the use of the mouse for controlling the camera is often used. On the other hand, the magnifier app which makes the elements on the screen appear larger, also makes use of the movement of the mouse to move around the screen. These two behaviors collide between each other if they wanna be performed simultaneously. In other words, while playing a videogame one is not able to use the magnifier app and move the mouse around the screen. 
This is the main reason why I wanted to build an application to help me read what's on the screen by using text-to-speech.

## Usage
When it comes to usage, this app can be used by everyone. However, people having some kind of visual imparement will benefit the most from using it. Furthurmore, this application could also serve as inspiration for encouraging game developers to include this kind of accessibility feature inside their games. 

## Application demo
In the following video it is shown how the application works:
1. It starts by scanning the content of the screen.
2. Once scanned, the user can switch between all detected text bounding boxes.
3. When the read out loud key is pressed the text inside the selected bounding box is read. 

https://user-images.githubusercontent.com/13052324/214283712-3282a405-70bc-4821-b365-ccd43e37dae7.mp4

> GPU use is recomended for much faster OCR inference time (Reading screen proces)

## Requirements & installation
### Requirements
- **OS**: Currently, the application is only available for Windows, since the majority of videogames are played in this OS. 

- **Suported languages**: English and Spaniash

- **Python version**: 3.9+
### Installation
- Run the `gaming_narrator.bat` and let the installation follow.

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

<ins>**REMEMBER:** The game you want to play must be set to **borderless**. Otherwise, the application will not work</ins>

Once all keys have been set, you can run the app in the background and start using it.

## Known issues (Work in progress)
- App sometimes crashes when display is loaded and clicking on the edges of the screen.
- This app would be ideal if it worked in real-time. The issue is that it exsits a trade-off between accuracy and speed. 

## Future work
- [x] More realistic TTS voices (on separate branch)
- [X] Windows installer version
- [ ] GUI
- [ ] Zooming into the detection while it's being read
- Speed up inferenceing:
  - [X] Pytorch 2.0 -- ***ABORTED**: `torch.compile` not supported on Windows yet.*
  - [ ] TensorRT ([source1](https://medium.com/@zergtant/accelerating-model-inference-with-tensorrt-tips-and-best-practices-for-pytorch-users-7cd4c30c97bc) + [source2](https://github.com/JaidedAI/EasyOCR/issues/786))
  - [ ] Alternative OCR [[1]](https://github.com/mindee/doctr) 
