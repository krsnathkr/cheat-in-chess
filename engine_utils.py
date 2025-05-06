
from __future__ import annotations
import os, chess, chess.engine, time
from functools import wraps
from config import STOCKFISH_PATH, STOCKFISH_THINK_TIME

_engine: chess.engine.SimpleEngine | None = None
_MAX_RETRIES = 3      # how many consecutive crashes we tolerate

def _launch() -> bool:
    global _engine
    try:
        if _engine:
            _engine.quit()
    except Exception:
        pass

    if not os.path.exists(STOCKFISH_PATH):
        print("Stockfish path not found →", STOCKFISH_PATH, flush=True)
        _engine = None
        return False

    try:
        _engine = chess.engine.SimpleEngine.popen_uci(STOCKFISH_PATH)
        print("Stockfish launched:", _engine.id.get('name', '?'), flush=True)
        return True
    except Exception as e:
        print("Stockfish failed to launch:", e, flush=True)
        _engine = None
        return False

_launch()

def _ensure_alive(func):
    @wraps(func)
    def wrapper(*args, **kw):
        retries = 0
        while retries <= _MAX_RETRIES:
            try:
                if _engine is None:
                    raise chess.engine.EngineTerminatedError
                return func(*args, **kw)
            except (chess.engine.EngineTerminatedError, OSError, BrokenPipeError):
                retries += 1
                print("Stockfish died – restarting …", f"(attempt {retries})", flush=True)
                if not _launch():
                    time.sleep(0.2)
        # after MAX_RETRIES it gives up
        return "Engine Crashed"
    return wrapper

@_ensure_alive
def get_best_move(fen: str,
                  think: float = STOCKFISH_THINK_TIME) -> str:
    try:
        board = chess.Board(fen)
    except ValueError:
        return "Invalid FEN"

    if board.is_game_over():
        return "Game Over"

    result = _engine.play(board, chess.engine.Limit(time=think))
    return result.move.uci()

def shutdown() -> None:
    try:
        if _engine:
            _engine.quit()
    except Exception:
        pass
