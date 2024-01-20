# Getting Started
## Requirements & installation
### Requirements
- **OS**: Primarly Windows, but not tested on Linux or Mac OS

- **Suported languages**: English and Spaniash

- **Python version**: `3.9.12`

### Installation
```python
# Create new environment
python -m venv .env

# Activate environment
.\.env\Scripts\Activate.ps1

# Install setup.py
python setup.py install

# Install GUI componentes (visit issue for more info)
python -m pip install PyQt5
```
## How to use?
First and foremost, watch the demo video on the README to get an introduction on how the app works. Once watched you would've noticed that the app has 2 modes, regional and SnQ:

1. Regional: By using the mouse, define a region of the screen to be scanned. Once scanned, you can interact with the detected regions and choose one to be read out loud.
2. SnQ (Small and Quick): When triggered, reads the clossest text element from the mouse point.  

> [!NOTE]
> 1. Key binding names must be in the same language as your OS. 
> 2. GPU is not required but is recomended for reducing inference times.

> [!IMPORTANT]
> If you plan on using the narrator while playing videogames, make sure that the game is set to borderless window.

Finally, start the app by running:
```python
gnarrator
```

For launching **Region mode**: Press `ALT + A + 1` and then draw a region to scan.
For launching **SnQ mode**: Point the mouse to the closest desired element and then press `ALT + A + 2`

## Known issues (Work in progress)
> [!WARNING]
> App still in development, issues can ocurr frequently  
> Visit [issues](https://github.com/arcb01/g-narrator/issues) for more information
  
## Future work
TODOs are defined [here](https://github.com/arcb01/gaming-narrator/blob/main/docs/todos.md)


