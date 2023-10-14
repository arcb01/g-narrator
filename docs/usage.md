# Getting Started
## Requirements & installation
### Requirements
- **OS**: Currently, the application is only available for Windows, since the majority of videogames are played in this OS. 

- **Suported languages**: English and Spaniash

- **Python version**: 3.9+
### Installation
- Run the `installation.bat` and let the installation follow.

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
- In cases when GPU is not available, inference times are really slow.
  
## Future work
- More realistic TTS voices
  - [x] Elevenlabs
  - [ ] Hugging Face TTS model
- Testing (github actions)
  - [ ] Improve linting score
  - [ ] Add more tests
  - [ ] Improve pytest coverage score
- [X] Windows installer version
- [ ] GUI
- [ ] AI features
- [ ] Zooming into the detection while it's being read
- [ ] Hover mode (for times when available)
