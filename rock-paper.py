import tkinter as tk
import random

# ---------- Colors (matching the screenshot) ----------
BG_COLOR = "#E6E6FA"      # light lavender background
DARK_MAROON = "#5B0E2D"   # dark maroon text/borders
BTN_MAROON = "#5B0E2D"    # play again button color
CARD_WHITE = "#FFFFFF"

CHOICES = ["rock", "paper", "scissors"]
ICONS = {"rock": "✊", "paper": "✋", "scissors": "✌️"}

TIME_LIMIT = 7  # seconds


class RPSGame(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Rock Paper Scissors")
        self.configure(bg=BG_COLOR)
        self.geometry("740x740")
        self.resizable(False, False)

        self.player_score = 0
        self.computer_score = 0
        self.time_left = TIME_LIMIT
        self.timer_id = None
        self.round_over = False

        self._build_ui()
        self._start_timer()

    # ---------------- UI BUILD ----------------
    def _build_ui(self):
        # Title
        tk.Label(
            self, text="Rock Paper Scissors", font=("Arial", 36, "bold"),
            fg=DARK_MAROON, bg=BG_COLOR
        ).pack(pady=(30, 20))

        # Score row
        score_frame = tk.Frame(self, bg=BG_COLOR)
        score_frame.pack(pady=10)

        self.player_label = tk.Label(
            score_frame, text=f"Player: {self.player_score}",
            font=("Arial", 18), fg=DARK_MAROON, bg=BG_COLOR,
            highlightbackground=DARK_MAROON, highlightthickness=2,
            padx=20, pady=8
        )
        self.player_label.grid(row=0, column=0, padx=15)

        self.computer_label = tk.Label(
            score_frame, text=f"Computer: {self.computer_score}",
            font=("Arial", 18), fg=DARK_MAROON, bg=BG_COLOR,
            highlightbackground=DARK_MAROON, highlightthickness=2,
            padx=20, pady=8
        )
        self.computer_label.grid(row=0, column=1, padx=15)

        # Choice cards
        cards_frame = tk.Frame(self, bg=BG_COLOR)
        cards_frame.pack(pady=30)

        self.card_buttons = {}
        for i, choice in enumerate(CHOICES):
            btn = tk.Button(
                cards_frame, text=ICONS[choice], font=("Arial", 48),
                fg=DARK_MAROON, bg=CARD_WHITE,
                highlightbackground=DARK_MAROON, highlightthickness=2,
                width=4, height=2, bd=0, relief="flat",
                activebackground="#f0f0f0",
                command=lambda c=choice: self.play(c)
            )
            btn.grid(row=0, column=i, padx=15)
            self.card_buttons[choice] = btn

        # Status text
        self.status_label = tk.Label(
            self, text="Choose your weapon!", font=("Arial", 22),
            fg=DARK_MAROON, bg=BG_COLOR
        )
        self.status_label.pack(pady=(20, 5))

        # Timer text
        self.timer_label = tk.Label(
            self, text=f"Time left: {self.time_left}s", font=("Arial", 20),
            fg=DARK_MAROON, bg=BG_COLOR
        )
        self.timer_label.pack(pady=5)

        # Play again button
        self.play_again_btn = tk.Button(
            self, text="Play Again", font=("Arial", 16, "bold"),
            fg="white", bg=BTN_MAROON, activebackground="#7a1740",
            bd=0, padx=25, pady=12, command=self.reset_round
        )
        self.play_again_btn.pack(pady=30)

    # ---------------- TIMER ----------------
    def _start_timer(self):
        self.time_left = TIME_LIMIT
        self.round_over = False
        self.timer_label.config(text=f"Time left: {self.time_left}s")
        self._tick()

    def _tick(self):
        if self.round_over:
            return
        if self.time_left <= 0:
            # Time's up -> auto pick random for player
            self.play(random.choice(CHOICES), timed_out=True)
            return
        self.timer_label.config(text=f"Time left: {self.time_left}s")
        self.time_left -= 1
        self.timer_id = self.after(1000, self._tick)

    def _stop_timer(self):
        if self.timer_id is not None:
            self.after_cancel(self.timer_id)
            self.timer_id = None

    # ---------------- GAME LOGIC ----------------
    def play(self, player_choice, timed_out=False):
        if self.round_over:
            return
        self.round_over = True
        self._stop_timer()

        computer_choice = random.choice(CHOICES)
        result = self._decide(player_choice, computer_choice)

        prefix = "Time's up! " if timed_out else ""
        if result == "win":
            self.player_score += 1
            msg = f"{prefix}You chose {ICONS[player_choice]} vs {ICONS[computer_choice]} — You win!"
        elif result == "lose":
            self.computer_score += 1
            msg = f"{prefix}You chose {ICONS[player_choice]} vs {ICONS[computer_choice]} — You lose!"
        else:
            msg = f"{prefix}You chose {ICONS[player_choice]} vs {ICONS[computer_choice]} — It's a tie!"

        self.player_label.config(text=f"Player: {self.player_score}")
        self.computer_label.config(text=f"Computer: {self.computer_score}")
        self.status_label.config(text=msg)
        self.timer_label.config(text="Round over")

    @staticmethod
    def _decide(player, computer):
        if player == computer:
            return "tie"
        beats = {"rock": "scissors", "paper": "rock", "scissors": "paper"}
        if beats[player] == computer:
            return "win"
        return "lose"

    def reset_round(self):
        self.status_label.config(text="Choose your weapon!")
        self._start_timer()


if __name__ == "__main__":
    app = RPSGame()
    app.mainloop()