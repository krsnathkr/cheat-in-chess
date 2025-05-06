import cv2, time, numpy as np
from ultralytics import YOLO
from config        import *
from detection     import detect_board_corners, detect_pieces, draw_text_with_outline
from fen_utils     import board_to_fen
from engine_utils  import get_best_move, shutdown
from voice_utils   import init_tts, speak_move
from ascii_board   import display as show_ascii_board


def main() -> None:
    tts         = init_tts()
    last_spoken = None

    piece_yolo  = YOLO(r"runs\detect\train3\weights\best.pt")


    cap = cv2.VideoCapture(1) # 1 is for OBS
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

    dst = np.array([[0, 0],
                    [BOARD_SIZE - 1, 0],
                    [BOARD_SIZE - 1, BOARD_SIZE - 1],
                    [0, BOARD_SIZE - 1]], np.float32)

    last_fen, best_move, last_time = None, "Calculating…", time.time()
    current_fen, board             = None, None

    while True:
        ok, frame = cap.read()
        if not ok:
            continue

        #detect corners of the board with aruco
        src = detect_board_corners(frame)
        if src is None:
            disp = cv2.resize(frame, (TARGET_DISPLAY_WIDTH, TARGET_DISPLAY_HEIGHT))
            cv2.putText(disp, "Searching for board…", (10, 30),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
            cv2.imshow("Camera", disp)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
            continue

        #wrap the board to a square and detect pieces
        H       = cv2.getPerspectiveTransform(src, dst)
        warped  = cv2.warpPerspective(frame, H, (BOARD_SIZE, BOARD_SIZE))
        board, overlay = detect_pieces(warped, piece_yolo)
        current_fen    = board_to_fen(board, "w")

        ## if the board has changed, get the best move from the engine
        if current_fen != last_fen:
            best_move = get_best_move(current_fen)
            if best_move not in {"Invalid FEN", "Game Over", "Engine Crashed"} and best_move != last_spoken:
                speak_move(tts, best_move)
                last_spoken = best_move

            show_ascii_board(board)          
            last_fen, last_time = current_fen, time.time()

        draw_text_with_outline(overlay, f"FEN: {current_fen}", (6, 16),
                               font=cv2.FONT_HERSHEY_PLAIN, scale=1.0,
                               color=(0, 255, 255))
        col = (0, 255, 0) if (time.time() - last_time) < 1 else (255, 255, 0)
        if best_move == "Game Over":
            col = (255, 0, 255)
        draw_text_with_outline(overlay, f"Best Move: {best_move}", (6, 40),
                               scale=0.7, color=col)

        cv2.imshow("Board",
                   cv2.resize(overlay, (TARGET_DISPLAY_WIDTH, TARGET_DISPLAY_HEIGHT)))
        cam = cv2.resize(frame, (TARGET_DISPLAY_WIDTH, TARGET_DISPLAY_HEIGHT))
        cv2.polylines(cam, [src.astype(int)], True, (0, 255, 0), 2)
        cv2.imshow("Camera", cam)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
    shutdown()
    if tts:
        tts.stop()


if __name__ == "__main__":
    main()
