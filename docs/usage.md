# Getting Started
## Requirements & installation
### Requirements
- **OS**: Primarly Windows, but not tested on Linux or Mac OS

- **Suported languages**: English and Spaniash

- **Python version**: 3.9+
  
> [!IMPORTANT]
> GPU is recomended for faster inference times.

### Installation
Run the `installation.bat` and let the installation follow.

## How to use?
First and foremost, watch the demo video on the README to get an introduction on how the app works. Once watched you would've noticed that the app has 2 modes, regional and SnQ:

1. Regional: By using the mouse, define a region of the screen to be scanned. Once scanned, you can interact with the detected regions and choose one to be read out loud.
2. SnQ (Small and Quick): When triggered, reads the clossest text element from the mouse point.  

Before running the application, set your prefered key bindings by editing `/config/keys.json/` file.

> [!NOTE]
> Key binding names must be in the same language as your OS.

> [!IMPORTANT]
> If you plan on using the narrator while playing videogames, make sure that the game is set to borderless window.

Finally, start the app by running the `run.bat` file

## Known issues (Work in progress)
> [!WARNING]
> App still in development, issues can ocurr frequently 

**Bug list**
- [ ] When using the app while gaming, it can ocurr that the language from the keybaord changes during execution and therefore keyboard input stops working
  
## Future work
TODOs are defined [here](https://github.com/arcb01/gaming-narrator/blob/main/docs/todos.md)


