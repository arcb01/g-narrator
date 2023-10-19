# Getting Started
## Requirements & installation
### Requirements
- **OS**: Currently, the application is only available for Windows, since the majority of videogames are played in this OS. 

- **Suported languages**: English and Spaniash

- **Python version**: 3.9+
### Installation
- Run the `run.bat` and let the installation follow.

## How to use?
Frist and foremost, custom key bindings must be defined. To do so, edit the file `config/keys.json`. Here there's a description of what's the role of each key.
Keys descriptions:

`"CAPTURE":` This key will take a screenshot

`"SWITCH_FORWARD":` Move to the next detection 

 `"SWITCH_BACKWARD":` Move to previous detection
 
 `"REPEAT":` Repeat text at a slower pase 
 
 `"READ_OUT_LOUD":` Text-to-speech 
 
 `"QUIT":` Exit key. It will clear the screen aswell

> [!NOTE]
> Key binding names must be in the same language as your OS.

Once all keys have been set, you can run the app in the background and start using it.

> [!IMPORTANT]
Remember that the game you want to play must be set to **borderless**. Otherwise, the application will not work</ins>

## Known issues (Work in progress)
> [!WARNING]
> - In cases when GPU is not available, inference times are really slow.
> - App sometimes crashes when display is loaded and clicking on the edges of the screen.
  
## Future work
*Ranked by priority*
- [x] Installation script
- [x] Running script
- [x] Regional Reading feature
- Improve TTS
  - [x] Elevenlabs
  - [ ] Hugging Face TTS model
- [ ] Narrator does not shut up when pressing esc
- [ ] `__main__.py`?
- [ ] Logging
- [ ] Zooming feature: e.g zoom into the detection while it's being read
- [ ] Mouse key bindings
- Asthetics
  - [ ] Better looking reading screen (Translucenty)
  - [ ] Improve coloring and sizing
- Testing (github actions)
  - [ ] Improve linting score
  - [ ] Add more tests
  - [ ] Improve pytest coverage score
  - [ ] Add workflow for installation script
- [ ] Windows installer version (.msi)
- [ ] Docker image
- [ ] GUI
  - [ ] Key binder
- [ ] AI features
- [ ] Add new demo video

