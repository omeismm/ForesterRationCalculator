# ForesterRationCalculator
A script that calculates the most profitable combination of leaves and food to forester's rations.

Two versions available:  
1. **Command-line version** (`main.py`) - Simple terminal output  
2. **Web browser version** (`app.py`) - Full UI

# Requirements
python 3.6+

requests library for python.

pandas library for python.

flask library for python. (only if you want to run the web browser version with a ui)

# Make a virtual environment containing packages (recommended, otherwise install packages normally)
```
python -m venv myenv

myenv\Scripts\activate
```
For command-line version only:
```
pip install requests pandas
```
For web version:
```
pip install requests pandas flask 
```


# Run (Command-line Version)
```
python commandline/main.py
```

# Run (Web Version)
```
python backend/app.py
```
# TODO whenever I'm bored
- make a github pages version to remove the setup process
- add icons and links to the wiki for all items
