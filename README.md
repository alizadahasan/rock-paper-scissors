# Rock, Paper, Scissors Game

A Tkinter desktop game for playing Rock, Paper, Scissors against the computer. The game includes normal play, tournament mode, image buttons, sound effects, keyboard shortcuts, and a mute option.

## Requirements

- Python 3
- Tkinter
- Pillow
- pygame

Install the Python dependencies with:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Tkinter is required for the GUI. Some Python installations include it by default; others require installing it separately.

## Run

```bash
python project.py
```

## Test

```bash
python -m unittest discover
```

## Game Rules

- Rock beats Scissors.
- Scissors beats Paper.
- Paper beats Rock.
- Matching choices are a tie.
- Normal mode ends when either player reaches 5 points.
- Tournament mode requires the player to defeat 3 computer opponents.

## Controls

- Click the Rock, Paper, or Scissors image buttons.
- Press `R` for Rock.
- Press `P` for Paper.
- Press `S` for Scissors.

Keyboard shortcuts are disabled during countdowns and game-over dialogs.

## Menu

- **New Game**: resets to normal mode.
- **Tournament Mode**: starts tournament mode.
- **Mute Sound**: toggles sound effects on or off.
- **Exit**: closes the game.

## Project Structure

- `project.py`: main game code.
- `rock.png`, `paper.png`, `scissors.png`: choice button images.
- `click.wav`: click sound effect.
- `requirements.txt`: Python dependencies.
- `tests/`: unit tests for game logic.

## Notes

The game loads assets relative to `project.py`, so it can be started from outside the project directory. The module is also safe to import in tests without launching the GUI.

**Developed by**: Hasan Alizada
