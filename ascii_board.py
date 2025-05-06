
from __future__ import annotations
import sys, os

# unicode symbols
UNICODE = {
    "K": "♔", "Q": "♕", "R": "♖", "B": "♗", "N": "♘", "P": "♙",
    "k": "♚", "q": "♛", "r": "♜", "b": "♝", "n": "♞", "p": "♟",
    ".": "·",  
}

FILES = "abcdefgh"

def _clear():
    if os.name == "nt":
        os.system("cls")
    else:
        sys.stdout.write("\033c")   # ANSI clear
        sys.stdout.flush()

# convert a row of the board to a string
def _row_to_string(row: list[str], rank: int) -> str:
    cells = " ".join(UNICODE.get(p, p) for p in row)
    return f"{rank} {cells} {rank}"

def board_to_ascii(board_arr: list[list[str]]) -> str:
    lines = [_row_to_string(board_arr[r], 8 - r) for r in range(8)]
    border = "  " + " ".join(FILES)
    return "\n".join([border, *lines, border])

def display(board_arr: list[list[str]]) -> None:
    _clear()
    print(board_to_ascii(board_arr), flush=True)
