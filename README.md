# Lgame ML
Training an AI for the L-game app (proof of concept and playing around with ML). Reinforcement learning with Q-table.

## Requirements
- Python 3.9.7
- Pytest 7.1.1
- NumPy 1.20.3

## How to run the implementation:
### Main program
- File: Lgame_main.py
- Run with `python3 Lgame_main.py`

### Tests
- File: Lgame_test.py
- Run with `pytest`

Information about pytest: https://docs.pytest.org/en/7.1.x/getting-started.html

## Classes
### The pieces
- Files: Lpiece.py, Npiece.py, GamePiece.py
### The game board
- File: Lgame.py

## More Information
This Lgame implementation is not finished and does not work properly yet.

The implementation uses a file with possible states. If something happens to the file it can be updated/recreated by running `python3 update_positions.py`.
