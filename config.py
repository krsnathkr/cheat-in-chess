import cv2

BOARD_SIZE              = 512                
SQUARE_PX               = BOARD_SIZE // 8
ARUCO_DICT              = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_4X4_50)
ID2POS                  = {0: 0, 1: 1, 2: 2, 3: 3}   # tag‑id → slot (TL, TR, BR, BL)

#fen settings
PIECE_CODE = {
    "white_pawn": "P",  "white_rook": "R",  "white_knight": "N",
    "white_bishop": "B","white_queen": "Q", "white_king": "K",
    "black_pawn": "p",  "black_rook": "r",  "black_knight": "n",
    "black_bishop": "b","black_queen": "q", "black_king": "k",
}

#display settings
TARGET_DISPLAY_WIDTH    = 960
TARGET_DISPLAY_HEIGHT   = 540

#stockfish settings
STOCKFISH_PATH          = r"D:\Code\Github\cheat-in-chess\stockfish-windows-x86-64-avx2\stockfish\stockfish-windows-x86-64-avx2.exe"
STOCKFISH_THINK_TIME    = 0.5 # seconds
