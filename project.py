from pathlib import Path
import random
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk

try:
    import pygame
except ImportError:
    pygame = None


class RockPaperScissorsGame:
    OPTIONS = ("rock", "paper", "scissors")
    EMOJIS = {
        "rock": "✊",
        "paper": "✋",
        "scissors": "✌️",
    }

    def __init__(self):
        self.base_dir = Path(__file__).resolve().parent

        self.window = tk.Tk()
        self.window.title("Rock, Paper, Scissors Game")
        self.window.minsize(450, 350)
        self.window.protocol("WM_DELETE_WINDOW", self.close_game)

        self.player_name = "Player"
        self.computer_name = "Computer"
        self.user_score = 0
        self.computer_score = 0
        self.computers_defeated = 0
        self.tournament_mode = False
        self.sound_muted = tk.BooleanVar(value=False)
        self.game_over_window = None
        self.welcome_screen = None

        self.images = {}
        self.sounds = {}

        self.user_choice_label = None
        self.computer_choice_label = None
        self.result_label = None
        self.score_label = None
        self.countdown_label = None
        self.rock_button = None
        self.paper_button = None
        self.scissors_button = None

        self.init_sounds()
        self.create_menu()
        self.setup_ui()
        self.bind_keys()
        self.show_welcome_screen()

    def asset_path(self, filename):
        return self.base_dir / filename

    def init_sounds(self):
        if pygame is None:
            return

        try:
            pygame.mixer.init()
            click_sound = pygame.mixer.Sound(str(self.asset_path("click.wav")))
        except Exception:
            return

        for option in self.OPTIONS:
            self.sounds[option] = click_sound

    def create_menu(self):
        menu_bar = tk.Menu(self.window)
        self.window.config(menu=menu_bar)

        game_menu = tk.Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(label="Menu", menu=game_menu)

        game_menu.add_command(label="New Game", command=self.new_game)
        game_menu.add_command(label="Tournament Mode", command=self.start_tournament_from_menu)
        game_menu.add_checkbutton(
            label="Mute Sound",
            variable=self.sound_muted,
        )
        game_menu.add_separator()
        game_menu.add_command(label="Exit", command=self.close_game)

    def setup_ui(self):
        self.load_images()

        choice_frame = tk.Frame(self.window)
        result_frame = tk.Frame(self.window)
        score_frame = tk.Frame(self.window)
        button_frame = tk.Frame(self.window)

        self.user_choice_label = tk.Label(choice_frame, text="", font=("Arial", 11))
        self.computer_choice_label = tk.Label(choice_frame, text="Computer's Choice:", font=("Arial", 11))
        self.result_label = tk.Label(result_frame, text="", font=("Arial", 14, "bold"))
        self.score_label = tk.Label(score_frame, text="Score: Player - 0 | Computer - 0", font=("Arial", 12))
        self.countdown_label = tk.Label(self.window, text="", font=("Arial", 12, "bold"))

        self.user_choice_label.pack(side=tk.LEFT, padx=10)
        self.computer_choice_label.pack(side=tk.RIGHT, padx=10)
        self.result_label.pack()
        self.score_label.pack()

        self.rock_button = self.create_choice_button(button_frame, "rock")
        self.paper_button = self.create_choice_button(button_frame, "paper")
        self.scissors_button = self.create_choice_button(button_frame, "scissors")

        self.rock_button.pack(side=tk.LEFT, padx=10)
        self.paper_button.pack(side=tk.LEFT, padx=10)
        self.scissors_button.pack(side=tk.LEFT, padx=10)

        choice_frame.pack(pady=15)
        result_frame.pack(pady=10)
        score_frame.pack(pady=10)
        button_frame.pack(pady=15)
        self.countdown_label.pack(pady=10)

    def load_images(self):
        try:
            resample_filter = Image.Resampling.LANCZOS
        except AttributeError:
            resample_filter = Image.LANCZOS

        desired_size = (100, 100)

        for option in self.OPTIONS:
            filename = f"{option}.png"
            path = self.asset_path(filename)

            try:
                image = Image.open(path).resize(desired_size, resample_filter)
                self.images[option] = ImageTk.PhotoImage(image)
            except FileNotFoundError:
                messagebox.showerror("Missing Image", f"Could not find {filename}.")
                self.window.destroy()
                raise
            except Exception as error:
                messagebox.showerror("Image Error", f"Could not load {filename}:\n{error}")
                self.window.destroy()
                raise

    def create_choice_button(self, parent, choice):
        return tk.Button(
            parent,
            image=self.images[choice],
            text=choice.capitalize(),
            compound=tk.TOP,
            command=lambda: self.choose_option(choice),
            borderwidth=2,
            padx=5,
            pady=5,
        )

    def bind_keys(self):
        self.window.bind("r", lambda event: self.choose_option_from_keyboard("rock"))
        self.window.bind("p", lambda event: self.choose_option_from_keyboard("paper"))
        self.window.bind("s", lambda event: self.choose_option_from_keyboard("scissors"))

    def show_welcome_screen(self):
        self.window.withdraw()

        self.welcome_screen = tk.Toplevel(self.window)
        self.welcome_screen.title("Welcome")
        self.welcome_screen.minsize(350, 200)
        self.welcome_screen.protocol("WM_DELETE_WINDOW", self.close_game)

        tk.Label(
            self.welcome_screen,
            text="Welcome to Rock, Paper, Scissors!",
            font=("Arial", 14, "bold"),
        ).pack(pady=10)

        tk.Label(self.welcome_screen, text="Enter Your Name:").pack()
        name_entry = tk.Entry(self.welcome_screen)
        name_entry.pack(pady=5)
        name_entry.focus_set()

        tk.Button(
            self.welcome_screen,
            text="Start Normal Game Mode",
            command=lambda: self.start_game(name_entry.get()),
        ).pack(pady=5)

        tk.Button(
            self.welcome_screen,
            text="Start Tournament Game Mode",
            command=lambda: self.start_tournament_mode(name_entry.get()),
        ).pack(pady=5)

        self.welcome_screen.bind("<Return>", lambda event: self.start_game(name_entry.get()))

    def update_player_name(self, name):
        self.player_name = name.strip() or "Player"

    def start_game(self, name):
        self.update_player_name(name)
        self.tournament_mode = False
        self.computer_name = "Computer"
        self.computers_defeated = 0
        self.reset_scores()
        self.close_welcome_screen()
        self.show_game_screen()
        self.update_ui("", "", "")
        self.countdown()

    def start_tournament_mode(self, name):
        self.update_player_name(name)
        self.tournament_mode = True
        self.computer_name = "Computer 1"
        self.computers_defeated = 0
        self.reset_scores()
        self.close_welcome_screen()
        self.show_game_screen()
        self.update_ui("", "", "Defeat 3 computers to win the tournament!")
        self.countdown()

    def close_welcome_screen(self):
        if self.welcome_screen is not None:
            self.welcome_screen.destroy()
            self.welcome_screen = None

    def show_game_screen(self):
        self.window.deiconify()

    def set_choice_buttons_state(self, state):
        for button in (self.rock_button, self.paper_button, self.scissors_button):
            if button is not None:
                button.config(state=state)

    def countdown(self, seconds=3):
        self.set_choice_buttons_state(tk.DISABLED)

        def tick(remaining):
            if remaining > 0:
                suffix = "second" if remaining == 1 else "seconds"
                self.countdown_label.config(text=f"Game starting in {remaining} {suffix}...")
                self.window.after(1000, tick, remaining - 1)
            else:
                self.countdown_label.config(text="")
                self.set_choice_buttons_state(tk.NORMAL)

        tick(seconds)

    def choose_option_from_keyboard(self, choice):
        if self.rock_button is None or self.rock_button["state"] != tk.NORMAL:
            return
        self.choose_option(choice)

    def choose_option(self, user_choice):
        computer_choice = random.choice(self.OPTIONS)
        result = self.determine_winner(user_choice, computer_choice)
        self.play_sound(user_choice)
        self.update_ui(user_choice, computer_choice, result)

        if self.tournament_mode:
            self.check_tournament_progress()
        else:
            self.check_normal_game_progress()

    def determine_winner(self, user_choice, computer_choice):
        if user_choice == computer_choice:
            return "It's a tie!"

        user_wins = (
            (user_choice == "rock" and computer_choice == "scissors") or
            (user_choice == "paper" and computer_choice == "rock") or
            (user_choice == "scissors" and computer_choice == "paper")
        )

        if user_wins:
            self.user_score += 1
            return "You win this round!"

        self.computer_score += 1
        return "You lose this round!"

    def check_normal_game_progress(self):
        if self.user_score == 5:
            self.show_game_finish_screen(True)
        elif self.computer_score == 5:
            self.show_game_finish_screen(False)

    def check_tournament_progress(self):
        if self.user_score == 2:
            self.computers_defeated += 1

            if self.computers_defeated >= 3:
                self.show_tournament_result(True)
                return

            self.computer_name = f"Computer {self.computers_defeated + 1}"
            self.reset_scores()
            self.update_ui("", "", f"You defeated a computer! Next opponent: {self.computer_name}")
            self.countdown()

        elif self.computer_score == 2:
            self.show_tournament_result(False)

    def play_sound(self, choice):
        if self.sound_muted.get():
            return

        sound = self.sounds.get(choice)
        if sound:
            sound.play()

    def update_ui(self, user_choice, computer_choice, result):
        user_emoji = self.get_emoji(user_choice)
        computer_emoji = self.get_emoji(computer_choice)

        self.user_choice_label.config(
            text=f"{self.player_name}'s Choice: {user_choice.capitalize()} {user_emoji}" if user_choice else f"{self.player_name}'s Choice:"
        )
        self.computer_choice_label.config(
            text=f"{self.computer_name}'s Choice: {computer_choice.capitalize()} {computer_emoji}" if computer_choice else f"{self.computer_name}'s Choice:"
        )
        self.result_label.config(text=result)
        self.score_label.config(
            text=f"Score: {self.player_name} - {self.user_score} | {self.computer_name} - {self.computer_score}"
        )

    def get_emoji(self, choice):
        return self.EMOJIS.get(choice, "")

    def reset_scores(self):
        self.user_score = 0
        self.computer_score = 0

    def reset_game(self):
        self.reset_scores()
        self.computer_name = "Computer 1" if self.tournament_mode else "Computer"
        self.computers_defeated = 0
        self.update_ui("", "", "")
        self.set_choice_buttons_state(tk.NORMAL)

    def new_game(self):
        self.tournament_mode = False
        self.computer_name = "Computer"
        self.reset_game()
        self.countdown()

    def start_tournament_from_menu(self):
        self.tournament_mode = True
        self.computer_name = "Computer 1"
        self.reset_game()
        self.update_ui("", "", "Defeat 3 computers to win the tournament!")
        self.countdown()

    def show_game_finish_screen(self, user_wins):
        self.set_choice_buttons_state(tk.DISABLED)

        if user_wins:
            message = f"{self.player_name} wins the game!"
        else:
            message = "Computer wins the game!"

        self.show_end_window("Game Over", message, include_tournament_button=True)

    def show_tournament_result(self, user_won):
        self.set_choice_buttons_state(tk.DISABLED)

        if user_won:
            message = "You won the tournament! Congratulations!"
        else:
            message = "You lost the tournament. Better luck next time!"

        self.show_end_window("Tournament Over", message, include_tournament_button=True)

    def show_end_window(self, title, message, include_tournament_button=False):
        if self.game_over_window is not None:
            self.game_over_window.destroy()

        self.game_over_window = tk.Toplevel(self.window)
        self.game_over_window.title(title)
        self.game_over_window.transient(self.window)
        self.game_over_window.grab_set()
        self.game_over_window.protocol("WM_DELETE_WINDOW", self.close_game)

        tk.Label(self.game_over_window, text=message, font=("Arial", 13, "bold")).pack(pady=10)

        tk.Button(
            self.game_over_window,
            text="Play Normal Game",
            command=self.restart_normal_from_end_window,
        ).pack(pady=5)

        if include_tournament_button:
            tk.Button(
                self.game_over_window,
                text="Play Tournament",
                command=self.restart_tournament_from_end_window,
            ).pack(pady=5)

        tk.Button(
            self.game_over_window,
            text="Leave Game",
            command=self.close_game,
        ).pack(pady=5)

    def close_end_window(self):
        if self.game_over_window is not None:
            self.game_over_window.destroy()
            self.game_over_window = None

    def restart_normal_from_end_window(self):
        self.close_end_window()
        self.tournament_mode = False
        self.computer_name = "Computer"
        self.reset_game()
        self.countdown()

    def restart_tournament_from_end_window(self):
        self.close_end_window()
        self.tournament_mode = True
        self.computer_name = "Computer 1"
        self.reset_game()
        self.update_ui("", "", "Defeat 3 computers to win the tournament!")
        self.countdown()

    def close_game(self):
        try:
            if pygame is not None:
                pygame.mixer.quit()
        except Exception:
            pass

        self.window.destroy()

    def run(self):
        self.window.mainloop()


if __name__ == "__main__":
    game = RockPaperScissorsGame()
    game.run()
