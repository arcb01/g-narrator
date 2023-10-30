# Getting Started
## Requirements & installation
### Requirements
- **OS**: Primarly Windows, but not tested on Linux or Mac OS

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

> [!IMPORTANT]
> Key binding names must be in the same language as your OS.

Once all keys have been set, you can run the app in the background and start using it.

> [!IMPORTANT]
Remember that the game you want to play must be set to **borderless**. Otherwise, the application will not work</ins>

## Known issues (Work in progress)
> [!WARNING]
> - When GPU is not available, inference times are really slow.
> - TTS does not shut up after pressing `esc` while reading a long phrase
> - In region mode, define a minimum region if not enough pixels are selected
> - Sometimes can ocurr that the language from the keybaord changes and therefore keyboard input stops working
> - If you click the window while narrator is reading the program crashes
  
## Future work
TODOs are defined [here](https://github.com/arcb01/gaming-narrator/blob/main/docs/todos.md)


