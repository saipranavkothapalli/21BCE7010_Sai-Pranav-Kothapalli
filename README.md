# 5x5 Grid Chess Game
Done by **Sai Pranav Kothapalli** - **21BCE7010**

Turn-based chess-like game with a server-client architecture, utilising web-sockets for real-time communication and a web-based user interface. This project is a multiplayer game built on a 5x5 grid where two players control characters with different movement abilities. The game includes Pawns, Hero1, and Hero2, each with specific movement rules and combat mechanics.
## Preview
<img width="1039" alt="Screenshot 2024-08-27 at 11 14 40 AM" src="https://github.com/user-attachments/assets/2abf84b8-0a03-4022-8276-98af013eec59">

## Demo Play
https://github.com/user-attachments/assets/5b57abb2-140f-4fab-9519-9981c043acec

## Game Rules

### Characters
- **Pawn (P)**:
  - Moves one step in any direction: Left (L), Right (R), Forward (F), or Backward (B).
- **Hero1 (H1)**:
  - Moves two steps in any direction: Left (L), Right (R), Forward (F), or Backward (B).
- **Hero2 (H2)**:
  - Moves two steps diagonally in any direction: Forward-Left (FL), Forward-Right (FR), Backward-Left (BL), or Backward-Right (BR).

### Setup
- Player 1's characters start on row 0:
  - `[A-P, A-P, A-H1, A-H2, A-P]`
- Player 2's characters start on row 4:
  - `[B-P, B-P, B-H1, B-H2, B-P]`

### Objective
- Players take turns to move their characters across the 5x5 board.
- The game state is updated after each move, and the opponent’s turn begins.
- The goal is to control the board and strategically position your characters.

## Project Structure

```plaintext
Chess
│
├── server.py                # Server-side logic (Flask and Socket.IO)
├── templates
    └── index.html           # Client-side code (HTML/CSS)     
