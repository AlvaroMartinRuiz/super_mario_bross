# 2D Super Mario Bros Clone

![Python](https://img.shields.io/badge/Language-Python-FFD43B?style=for-the-badge&logo=python&logoColor=blue)
![GameDev](https://img.shields.io/badge/Game-Development-purple?style=for-the-badge)

This repository contains a fully functional 2D clone of **Super Mario Bros**, engineered entirely in Python. It was developed as a collaborative programming project to demonstrate Object-Oriented Programming (OOP) architectures and game loop mechanics.

## 📖 Overview

We built the core elements of the original classic game from scratch. The codebase heavily utilizes custom class inheritances to manage the complex interactions between Mario, enemies, and the interactive environment.

### Project Features
* **Custom Physics & Collisions**: Dedicated gravity handling and exact collision mapping between Sprites.
* **OOP Architecture**: 
  - `mario.py`: Handles player states (Small, Super, Fire), velocity, and animation loops.
  - `board.py`: Controls the camera panning, rendering logic, and level boundary generation.
  - `enemies.py` (Goomba, Koopa Troopa): AI movement and exact death-state handling.
* **Interactive Environment**: Breakable blocks, Question blocks, Coins, Green pipes, and Power-ups (Mushrooms & Fire Flowers).

## 🗂️ Project Structure

* `main.py`: The entry point and main application loop.
* `REPORT_MARIO.pdf`: The comprehensive technical report unpacking the architecture, class diagrams, and design patterns utilized to build the game.
* `/assets`: Contains all the 8-bit sprites and visual elements.
* Domain classes: Dozens of isolated python classes modeling exact elements (e.g., `cloud.py`, `flag.py`, `green_pipes.py`).

## 🚀 How to Play

1. **Clone the repo**:
   ```bash
   git clone https://github.com/AlvaroMartinRuiz/super_mario_bross.git
   ```
2. **Setup your environment**: Ensure you have Python 3 and the necessary graphical libraries installed (like `pygame` if utilized).
3. **Run the game**:
   ```bash
   python main.py
   ```
4. Check out `REPORT_MARIO.pdf` for a detailed technical breakdown!
