# Importing necessary libraries
from pathlib import Path
import tkinter as tk
from PIL import Image, ImageTk # I used PIL (Python Image Library) because of uploading rock,paper,scissors images.
import random
try:
    import pygame # I used pygame for sound effects
except ImportError:
    pygame = None

BASE_DIR = Path(__file__).resolve().parent
sounds = {}

try:
    RESAMPLE_FILTER = Image.Resampling.LANCZOS
except AttributeError:
    RESAMPLE_FILTER = Image.LANCZOS


def asset_path(filename):
    return BASE_DIR / filename


def init_sounds():
    if pygame is None:
        return

    try:
        pygame.mixer.init()
        click_sound = pygame.mixer.Sound(str(asset_path("click.wav")))
    except Exception:
        return

    sounds.update({
        "rock": click_sound,
        "paper": click_sound,
        "scissors": click_sound,
    })

# To initialize global variables
user_score = 0
computer_score = 0
user_choice_label = None
computer_choice_label = None
result_label = None
score_label = None
rock_img = None
paper_img = None
scissors_img = None
players = []
computer_name = "Computer"
computers_defeated = 0

game_over_window = None

choice_frame = None
result_frame = None
score_frame = None
button_frame = None

countdown_label = None
rock_button = None
paper_button = None
scissors_button = None
player_name = ""
tournament_mode = False

# Function to display the welcome screen with game mode options,hides main window, creates a new window for welcome screen with buttons to start different game modes
def show_welcome_screen():
    global window, welcome_screen, player_name
    window.withdraw()
    welcome_screen = tk.Toplevel()
    welcome_screen.title("Welcome to Rock, Paper, Scissors Game")

    # To create and display welcome screen elements
    welcome_label = tk.Label(welcome_screen, text="Welcome to Rock, Paper, Scissors Game!")
    player_name_label = tk.Label(welcome_screen, text="Enter Your Name:")
    player_name_entry = tk.Entry(welcome_screen)
    start_game_button = tk.Button(welcome_screen, text="Start Normal Game Mode",
                                  command=lambda: start_game(player_name_entry.get()))
    tournament_mode_button = tk.Button(welcome_screen, text="Start Tournament Game Mode",
                                       command=lambda: start_tournament_mode(player_name_entry.get()))

    welcome_label.pack(pady=10)
    player_name_label.pack()
    player_name_entry.pack()
    start_game_button.pack()
    tournament_mode_button.pack()

# Function to start a normal game mode
def start_game(player_name):
    global welcome_screen, tournament_mode
    update_player_name(player_name)
    welcome_screen.destroy()  # Closes welcome screen, sets game mode to normal, shows game screen, and starts countdown
    tournament_mode = False
    show_game_screen()
    update_ui("", "", "")
    countdown()

# Function to start tournament game mode.Similar to "start_game" but sets the game mode to tournament
def start_tournament_mode(player_name):
    global welcome_screen, tournament_mode
    update_player_name(player_name)
    welcome_screen.destroy()
    tournament_mode = True
    show_game_screen()
    update_ui("", "", "")
    countdown()

# Function to update the player's name globally,sets the global player name variable.
def update_player_name(name):
    global player_name
    player_name = name.strip() or "Player"

# Function to show the main game screen,makes the main game window visible.
def show_game_screen():
    global window
    window.deiconify()

# Function to enable or disable the choice buttons together.
def set_choice_buttons_state(state):
    for button in (rock_button, paper_button, scissors_button):
        if button is not None:
            button.config(state=state)

# Function for displaying a countdown before starting the game.Performs a 3-second countdown, updates UI, and disables/enables buttons accordingly.
def countdown(seconds=3):
    set_choice_buttons_state(tk.DISABLED)

    def tick(remaining):
        if remaining > 0:
            suffix = "second" if remaining == 1 else "seconds"
            countdown_label.config(text=f"Game starting in {remaining} {suffix}...")
            window.after(1000, tick, remaining - 1)
            return

        countdown_label.config(text="")
        set_choice_buttons_state(tk.NORMAL)

    tick(seconds)

# Function to process player's choice and manage game logic.Handles player's choice, computer's choice, determines the winner, updates UI, and manages game progression.
def choose_option(user_choice):
    global user_score, computer_score, tournament_mode, player_name, computer_name, computers_defeated
    options = ['rock', 'paper', 'scissors']
    computer_choice = random.choice(options)
    result = determine_winner(user_choice, computer_choice)
    update_ui(user_choice, computer_choice, result)

    # To play the sound based on the user's choice
    play_sound_based_on_choice(user_choice)

    if tournament_mode:
        if user_score == 2:
            reset_scores()
            computers_defeated += 1
            if computers_defeated < 3:  # Continue with up to Computer 3
                computer_name = f"Computer {computers_defeated + 1}"
                update_ui("", "", f"You won, tournament continues with {computer_name}")
            else:
                show_tournament_result(True)  # User wins the tournament
                return
        elif computer_score == 2:
            show_tournament_result(False)  # User loses the tournament
            return
    else:
        # Checking for the end of the game in normal mode
        if user_score == 5:
            show_game_finish_screen(True)  # User wins
            return
        elif computer_score == 5:
            show_game_finish_screen(False)  # Computer wins
            return

# Function to display the game finish screen
def show_game_finish_screen(user_wins):
    global game_over_window, player_name, user_score, computer_score
    game_over_window = tk.Toplevel(window)
    game_over_window.title("Game Over")

    # To reset scores
    user_score = 0
    computer_score = 0

    if user_wins:
        finish_label_text = f"{player_name} Wins!" if not tournament_mode else "You won the tournament! Congratulations!"
    else:
        finish_label_text = "Computer Wins!" if not tournament_mode else "You lost the tournament. Better luck next time!"

    finish_label = tk.Label(game_over_window, text=finish_label_text)
    finish_label.pack()

    # To provide buttons to play again or exit
    play_again_button = tk.Button(game_over_window, text="Play Again", command=lambda: reset_game(game_over_window))
    leave_button = tk.Button(game_over_window, text="Leave Game", command=close_game)
    play_again_button.pack()
    leave_button.pack()

# Function to close the game.Closes the game over window and main game window.
def close_game():
    game_over_window.destroy()
    window.destroy()

# Function to start the tournament mode from the menu
def start_tournament_mode_from_menu():
    global tournament_mode, user_score, computer_score, computer_name, computers_defeated
    tournament_mode = True
    user_score = 0
    computer_score = 0
    computer_name = "Computer"
    computers_defeated = 0
    reset_game(None)  # Resetting the game to start the tournament
    show_game_screen()  # Showing the game screen if it's not already visible
    update_ui("", "", "")  # Resetting the UI elements
    countdown()  # Starting the countdown

# Function to reset scores.
def reset_scores():
    global user_score, computer_score
    user_score = 0
    computer_score = 0

# Function for playing a sound based on the user's choice.
def play_sound_based_on_choice(user_choice):
    sound = sounds.get(user_choice)
    if sound:
        sound.play()

# Function to determine the winner of the tournament.Compares scores to determine the tournament winner.
def determine_winner(user, computer):
    global user_score, computer_score
    if user == computer:
        return "It's a tie!"
    elif (user == "rock" and computer == "scissors") or \
            (user == "paper" and computer == "rock") or \
            (user == "scissors" and computer == "paper"):
        user_score += 1
        return "You win!"
    else:
        computer_score += 1
        return "You lose!"

# Function to update the UI elements
def update_ui(user_choice, computer_choice, result):
    global user_choice_label, computer_choice_label, score_label, player_name, computer_name
    user_choice_label.config(text=f"{player_name}'s Choice: {user_choice} {get_emoji(user_choice)}")
    computer_choice_label.config(text=f"{computer_name}'s Choice: {computer_choice} {get_emoji(computer_choice)}")
    result_label.config(text=result)
    score_label.config(text=f"Score: {player_name} - {user_score} | {computer_name} - {computer_score}")

# Function to set up the UI elements
def setup_ui():
    global user_choice_label, computer_choice_label, result_label, score_label, rock_img, paper_img, scissors_img, countdown_label
    global choice_frame, result_frame, score_frame, button_frame, rock_button, paper_button, scissors_button
    global menu_bar, game_menu

    # To load and resize images for choices
    desired_size = (100, 100)
    rock_img = Image.open(asset_path("rock.png")).resize(desired_size, RESAMPLE_FILTER)
    rock_img = ImageTk.PhotoImage(rock_img)

    paper_img = Image.open(asset_path("paper.png")).resize(desired_size, RESAMPLE_FILTER)
    paper_img = ImageTk.PhotoImage(paper_img)

    scissors_img = Image.open(asset_path("scissors.png")).resize(desired_size, RESAMPLE_FILTER)
    scissors_img = ImageTk.PhotoImage(scissors_img)

    # To create frames for different UI components
    choice_frame = tk.Frame(window)
    result_frame = tk.Frame(window)
    score_frame = tk.Frame(window)
    button_frame = tk.Frame(window)

    # To create labels for user choice, computer choice, result, and score
    global user_choice_label, computer_choice_label, score_label
    user_choice_label = tk.Label(window, text="")
    computer_choice_label = tk.Label(window, text="Computer's Choice: ")
    result_label = tk.Label(window, text="")
    score_label = tk.Label(window, text="Score: User - 0 | Computer - 0")

    # To pack labels into respective frames
    user_choice_label.pack(in_=choice_frame, side=tk.LEFT)
    computer_choice_label.pack(in_=choice_frame, side=tk.RIGHT)
    result_label.pack(in_=result_frame)
    score_label.pack(in_=score_frame)

    # To create buttons for rock, paper, and scissors
    rock_button = create_image_button(rock_img, lambda: choose_option("rock"))
    paper_button = create_image_button(paper_img, lambda: choose_option("paper"))
    scissors_button = create_image_button(scissors_img, lambda: choose_option("scissors"))

    # To pack buttons into the button frame
    rock_button.pack(in_=button_frame, side=tk.LEFT)
    paper_button.pack(in_=button_frame, side=tk.LEFT)
    scissors_button.pack(in_=button_frame, side=tk.LEFT)

    # To pack frames into the main window
    choice_frame.pack(pady=10)
    result_frame.pack(pady=10)
    score_frame.pack(pady=10)
    button_frame.pack(pady=10)

    # To create and pack a countdown label
    countdown_label = tk.Label(window, text="")
    countdown_label.pack()

    # To add a "Tournament Mode" option to the game menu
    game_menu.add_command(label="Tournament Mode", command=start_tournament_mode_from_menu)

    # To create a new game menu
    menu_bar.delete("Menu")
    game_menu = tk.Menu(menu_bar, tearoff=0)
    game_menu.add_command(label="New Game", command=new_game)
    game_menu.add_command(label="Tournament Mode", command=start_tournament_mode_from_menu)
    game_menu.add_command(label="Exit", command=window.quit)

    # To add the new game menu to the menu bar
    menu_bar.add_cascade(label="Menu", menu=game_menu)
    window.config(menu=menu_bar)

# Function to create a button with an image
def create_image_button(image, command):
    return tk.Button(window, image=image, command=command, borderwidth=0)

# Function to start a new game
def new_game():
    global tournament_mode
    tournament_mode = False  # Setting the game to normal mode
    reset_game(None)  # Reset the game
    update_ui("", "", "")  # Updating UI to reflect the reset

# Function to reset the game
def reset_game(finish_screen):
    global user_score, computer_score, players, computer_name, computers_defeated
    user_score = 0
    computer_score = 0
    computer_name = "Computer"
    computers_defeated = 0
    players = []
    user_choice_label.config(text="")
    computer_choice_label.config(text="Computer's Choice: ")
    result_label.config(text="")
    score_label.config(text=f"Score: {player_name} - 0 | Computer - 0")
    if finish_screen:
        finish_screen.destroy()

# Function to show the tournament result
def show_tournament_result():
    global players
    winner = determine_winner_tournament(players[0], players[1])
    players = []
    reset_game(None)
    show_game_finish_screen()

# Function to show the tournament result with an option to start a new tournament or normal game mode
def show_tournament_result(user_won):
    global game_over_window
    game_over_window = tk.Toplevel(window)
    game_over_window.title("Tournament Over")

    if user_won:
        finish_label_text = "You won the tournament! Congratulations!"
    else:
        finish_label_text = "You lost the tournament. Better luck next time!"

    finish_label = tk.Label(game_over_window, text=finish_label_text)
    finish_label.pack()

    # New Tournament button
    new_tournament_button = tk.Button(game_over_window, text="New Tournament", command=start_new_tournament)
    new_tournament_button.pack()

    # Normal Game Mode button
    normal_game_mode_button = tk.Button(game_over_window, text="Normal Game Mode", command=start_normal_game_mode)
    normal_game_mode_button.pack()

    leave_game_button = tk.Button(game_over_window, text="Leave Game", command=close_game)
    leave_game_button.pack()

# Function to close the game
def close_game():
    game_over_window.destroy()
    window.destroy()

# Function to start a new tournament
def start_new_tournament():
    global tournament_mode
    tournament_mode = True
    reset_game(game_over_window)  # Resetting the game to start the tournament
    update_ui("", "", "")  # Updating UI to reflect the reset
    countdown()  # Starting the countdown

# Function to start normal game
def start_normal_game_mode():
    global tournament_mode
    tournament_mode = False
    reset_game(game_over_window)  # Resetting the game to start normal mode
    update_ui("", "", "")  # Updating UI to reflect the reset
    countdown()  # Starting the countdown

# Function to determine the winner of the tournament.
def determine_winner_tournament(player1, player2):
    global user_score, computer_score
    if player1 == player_name:
        if user_score > computer_score:
            return player1
        else:
            return player2
    else:
        if computer_score > user_score:
            return player2
        else:
            return player1

# Function to get emoji representation of a choice
def get_emoji(choice):
    emojis = {
        'rock': '✊',
        'paper': '✋',
        'scissors': '✌️',
    }
    return emojis.get(choice, '')

# Tkinter window initialization and configuration.
window = tk.Tk()
window.title("Rock, Paper, Scissors Game")
window.minsize(400, 300)

#Sets up the main window with title, size, and menu bar.
# Menu bar setup
menu_bar = tk.Menu(window)
window.config(menu=menu_bar)

# Game menu setup
game_menu = tk.Menu(menu_bar, tearoff=0)
menu_bar.add_cascade(label="Menu", menu=game_menu)
game_menu.add_command(label="New Game", command=new_game)
game_menu.add_separator()
game_menu.add_command(label="Exit", command=window.quit)

# UI setup and welcome screen display.Calls setup_ui and show_welcome_screen functions to initialize the UI and show the welcome screen.
init_sounds()
setup_ui()
show_welcome_screen()

# Tkinter event loop.Starts the main loop to keep the application running.
window.mainloop()
