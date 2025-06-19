# Quest of the White Coat

An add-on for Anki, built to make med school studying feel just a little more like an adventure.

This project is dedicated to my girlfriend Giuliana. I love you. 

## Table of Contents
- [What's This?](#whats-this)
- [What I Learned](#what-i-learned)
- [How It Works](#how-it-works)
- [Demo/Screen shots](https://github.com/willmccarten/MQuest/edit/main/README.md#demoscreen-shots)
- [How to Install](#how-to-install)
- [File Breakdown](#file-breakdown)
- [Final Thoughts](#final-thoughts)

## What's This?

Quest of the White Coat is a gamified add-on for Anki designed to gently reward progress and consistency. It was created to turn the grind of flashcards into a small journey with visual feedback, ranks, and celebrations.

This project started as a simple idea: what if there were just a little badge system to track Anki reviews like leveling up in a game? That thought turned into ranks, a home screen, progress bars, celebration animations, and eventually a full experience inside of Anki.

## What I Learned

This project was a first for a few things:

- My first time building an Anki add-on, which meant learning the quirks of Qt, PyQt6, and Anki’s architecture
- My first time making pixel art from scratch, including character sprites and animations.

It’s far from perfect, but I learned a ton — and more importantly, it works, and it feels good.

## How It Works

When you open Anki, the add-on shows a new home screen that tracks your progress through review XP:

- You gain XP as you complete cards.
- You rise through medical-themed ranks like “Spry Sophomore,” “Senior Gator,” and eventually “Dr. White Coat Champion.”
- Ranks come with badge icons and visual updates.
- When you level up, a short celebration plays — fireworks and a popup to mark your progress.
- There’s also a simple “Quest” log for encouragement.

Behind the scenes, your progress is tracked using local JSON files to keep things simple and portable.

## Demo/Screen shots

![image](https://github.com/user-attachments/assets/10b3943e-9d45-4350-9191-f5999841c5f5)
Home screen view. Contains welcome message, character sprite that moves in a repeating short animation, user's progress bar to the next level, their current level and the next level they're working to, then finally a button to open the badges pop up. 
(Note: the art and the level names very specifically tailored to my girlfriend)


![image](https://github.com/user-attachments/assets/aeb9ca41-e6c5-4af6-8f03-dfa81cfdb7d0)
View Badges popup window. On this window we can see rows of badges that represent the user's progress in finishing these Anki decks. As they complete the decks more and learn more of the content, they will "earn xp" to unlock the badge, and the subsequently rank up the badge. These badges and their ranks directly are responsible for the user's total level xp that is displayed on the home page. Here in this screen shot you can see that the user has all their badges unlocked, but some at different ranks than others. Two decks are totally complete of learning, seen by a full bar and the diamond tier badge icon displayed. 


## How to Install

1. Download the latest `MQuest.zip` (this is the `MQuest` folder zipped up).
2. Unzip it and rename the folder to exactly `MQuest`.
3. Move the `MQuest` folder into your Anki add-ons directory:
   - On macOS:  
     `~/Library/Application Support/Anki2/addons21/`
4. Restart Anki.
5. From the menu bar, go to Tools → Quest of the White Coat.

On first launch, you’ll get a welcome popup and start tracking XP based on your daily Anki use. No need to change anything else.

Note: Your Anki study data isn’t touched — this is all read-only from your existing progress. The add-on just tracks and celebrates your journey.

## File Breakdown

Here's a high-level view of what each piece does:

| File / Folder         | Purpose |
|----------------------|---------|
| `ui.py`              | Controls the UI and logic for the main home screen and popups |
| `badge_manager.py`   | Handles XP, rank calculation, and simple JSON persistence |
| `assets/`            | All pixel art assets — backgrounds, characters, and badges |
| `rank_config.json`   | The XP thresholds and rank names (editable) |
| `welcome_config.json`          | Tracks whether the welcome popup has already been shown |
| `manifest.json`      | Required by Anki to load the add-on |
| `README.md`          | You’re reading it |
| `LICENSE`            | Default open-source license (MIT) — feel free to use or remix with credit |

## Final Thoughts

This was a side project made for someone I care about, and also for myself — to stretch a little, learn a new system, and make something fun out of the everyday.

If you’re a med student using Anki daily and this gives you even a small moment of joy, that’s all it was meant to do.

— Will

