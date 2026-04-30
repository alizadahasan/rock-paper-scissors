# Rock, Paper, Scissors Game

## Introduction

Welcome to the **Rock, Paper, Scissors** game! This game allows you to play the classic Rock, Paper, Scissors against the computer. Make your choice, and see if you can outsmart the computer to win the game.

---

## Setup

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Tkinter is also required to run the GUI. Some Python installations include it by default; others may require a separate install.

## Run

```bash
python project.py
```

## Test

```bash
python -m unittest discover
```

---

## Game Rules

- You can choose between three options: **Rock**, **Paper**, or **Scissors**.
- The computer will select its choice randomly.
- The winner of each round is determined based on the classic Rock, Paper, Scissors rules:
  - **Rock beats Scissors**
  - **Scissors beats Paper**
  - **Paper beats Rock**
- The game continues until either you or the computer reaches a score of 5 for **Normal Game Mode**.
- In **Tournament Game Mode**, the player must defeat three opponents to win the tournament.

---

## Features

### 1. **Game Modes:**

- **Normal Mode**: 
  - The game runs in a standard mode where the player competes against the computer.
  - The first player to reach a score of 5 wins the game.
  
- **Tournament Mode**: 
  - A special mode where the player competes against different computer opponents.
  - The player must defeat three opponents to win the tournament.

---

### 2. **User Interface:**

- **Welcome Screen**: 
  - Players are greeted with a welcome screen where they can enter their name and choose between normal and tournament modes.

- **Game Screen**: 
  - After entering the name, players are presented with the main game screen containing buttons for **Rock**, **Paper**, and **Scissors**, as well as labels to display choices, results, and the current score.

- **Countdown**: 
  - A countdown timer is displayed before the game starts, providing a visual cue for the player.

- **Choices**:
  - Click on the image buttons representing **Rock**, **Paper**, or **Scissors** to make your choice.

- **Score**:
  - The score is displayed at the bottom, showing the number of rounds won by you and the computer.

- **Result**: 
  - The result of each round (Win, Lose, or Tie) is displayed after making a choice.

---

### 3. **Game Over Screen:**

- When the game or tournament ends, a **Game Over** screen is displayed, showing the winner and providing options to play again or exit the game.

---

### 4. **Menu Options:**

- The game includes a menu bar with options such as starting a new game, entering tournament mode, and exiting the game.

---

## Enjoy the Game

Have fun playing the **Rock, Paper, Scissors** game! Test your strategy and see if you can beat the computer. Good luck!

---

**Developed by**: Hasan Alizada
