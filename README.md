# super_pong

## Installation

1. **Clone the repository:**
   ```sh
   git clone git@github.com:nebyu08/super_pong.git
   cd super_pong
   ```

2. **Create and activate a Python virtual environment using uv:**
   ```sh
   uv venv my_env
   source my_env/bin/activate
   ```

3. **Install dependencies with uv:**
   ```sh
   uv pip install pygame
   ```

Only `pygame` is required. All game assets (images and sounds) are included in the repository.

## How to Play

- Run the game:
  ```sh
  python main.py
  ```

- **Controls:**
  - Use arrow keys to move the canon (spacecraft) left, right, up, and down.
  - Click the left mouse button to shoot bullets.
  - Try to hit the falling blue balls before they reach the bottom.
  - Each hit increases your score; missed balls decrease your score.
  - If your score is negative, the screen border flashes red.

- **Objective:**  
  Destroy as many balls as possible and keep your score positive!
