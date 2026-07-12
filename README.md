# CODSOFT_TASKSNO
I applied for an internship in web development recently . This repo contains all my works during the internship

# 📝 To-Do List App

A desktop to-do list application built with Python and PyQt5, designed from a custom Figma UI and translated into a fully functional app with persistent storage.

## ✨ Features

- **Custom UI design** — built entirely from a Figma mockup, including custom typography (Kapakana, Inria Serif, Indie Flower) and a hand-picked dark/gold color palette
- **Task management** — add, complete, and delete tasks
- **Smart sectioning** — tasks automatically sort into "Today" or "Workspace" based on their due date
- **Date & time pickers** — built-in calendar and clock widgets for setting due dates
- **Collapsible sections** — expand/collapse "Today" and "Workspace" sections
- **Persistent storage** — tasks are saved to a local JSON file and reload automatically on launch
- **Custom SVG icons** — settings, search, notifications, and collapse icons exported directly from Figma

## 🛠️ Tech Stack

- **Python 3**
- **PyQt5** — GUI framework
- **QSS (Qt Style Sheets)** — for theming, similar to CSS
- **JSON** — for local data persistence

  -----------------------------------------------------------------------------------------------------------------------------------------------------------------

#🦆 Duck Calculator

A fully functional desktop calculator built with Python and Tkinter, featuring a custom pixel-art UI designed in Figma, animated baby duck decorations, background music, and button click sound effects.



##Features


🧮 Full calculator functionality — addition, subtraction, multiplication, division, percentages, sign toggle, and decimals
🎨 Custom pixel-art interface designed in Figma and recreated pixel-by-pixel in Python
🦆 Animated baby duck GIFs decorating the calculator's border
🔤 Custom pixel font (Pixelify Sans) rendered directly with PIL for crisp, consistent text
🔊 Background music that plays on launch, plus a click sound effect on every button press
🖱️ Fully interactive — every button is clickable and responds with a "pressed" animation


##Preview



https://github.com/user-attachments/assets/c02c5f97-5ce9-4068-9f6d-a0ba1ce18c4b



##Tech Stack


**Python 3** — core language
**Tkinter** — GUI framework and canvas-based rendering
**Pillow (PIL)** — image processing, gradients, custom font rendering, GIF frame handling
**Pygame** — audio playback (background music + click sounds)



##Credits

**Design**: Created in Figma
**Font**: Pixelify Sans by Google Fonts
**Built as part of the CODSOFT internship task series**

---------------------------------------------------------------------------------------------------------------------------------------------------------------
# Rock Paper Scissors 🪨📄✂️

A desktop Rock Paper Scissors game built with **Python** and **Tkinter**, featuring a clean lavender-and-maroon UI, live score tracking, and a 7-second countdown timer per round.

<img width="800" height="834" alt="ScreenRecording2026-07-12135809-ezgif com-video-to-gif-converter" src="https://github.com/user-attachments/assets/1de03f59-f706-4545-8bf6-926412d47418" />


---

## ✨ Features

- **Three choices** — Rock ✊, Paper ✋, Scissors ✌️, shown as clickable cards
- **Live score tracking** — Player vs Computer scores update after every round
- **7-second countdown timer** — if time runs out, a random choice is auto-played for you
- **Instant results** — see your pick, the computer's pick, and the outcome (win/lose/tie)
- **Play Again** — resets the round and timer, scores carry over
- **Matches the original design** — lavender background, dark maroon accents, rounded cards

## 🛠️ Tech Stack

- **Python 3**
- **Tkinter** — built-in GUI framework (no extra installs needed)

## 🚀 Getting Started

### Prerequisites

- Python 3.8+ (Tkinter ships with most standard Python installs)



## 🎮 How to Play

1. Click Rock, Paper, or Scissors before the timer runs out.
2. The computer makes its choice at the same time.
3. The result and updated scores are shown instantly.
4. Click **Play Again** to start a new round.

------------------------------------------------------------------------------------------------------------------------------------------------------------------

# Password Generator

A desktop password generator built with Python and PyQt5. Generates strong random passwords with adjustable length and character composition, or lets you type and check your own password strength.

## Features

- **Characters mode** — generate a random password with sliders for total length, digit count, capital letter count, and symbol count
- **Words mode** — type your own password and see its strength evaluated live
- **Animated strength indicator** — a colored progress bar and an animal GIF mascot (mouse → sheep → tiger → bear → elephant) that changes based on password strength, each with a custom-font caption
- **Copy to clipboard** — one click via the Copy button
- **Custom styling** — QSS-driven UI matching the reference design (rounded sliders, pill-shaped buttons)

## Tech stack

- Python 3
- PyQt5 (GUI framework)
- `random` / `string` (password generation)


## How strength is scored

The app awards 25 points each for: length ≥ 8 characters, containing a digit, containing an uppercase letter, and containing a symbol — for a max score of 100. That score maps to one of 5 tiers (mouse → elephant), each with its own bar color and mascot.

## Credits

- Animal GIFs: sourced from free stock/sticker sites — check individual licenses before distributing or submitting this project, several require visible attribution.
- Caption font: Mochibop Demo (1001fonts) — confirm license terms (free vs. personal-use-only) before distribution.
- Design reference: TunnelBear Password Generator concept, Dribbble (by the TunnelBear team).

## Known limitations / next steps

- Words mode doesn't generate passphrases from a word list yet — it's currently just a free-text field with strength checking.
- "Use Password" button has no wired behavior yet — placeholder for future functionality (e.g. auto-copy + close, or hand-off to another field).
- Strength scoring is a simple 4-factor point system, not a full entropy-based calculation.
