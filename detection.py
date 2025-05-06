import cv2, numpy as np
from ultralytics import YOLO
from config import *


def draw_text_with_outline(img, text, org,
                           font=cv2.FONT_HERSHEY_SIMPLEX,
                           scale=0.55, color=(255,255,255),
                           thickness=1, outline=(0,0,0),
                           outline_th=3):
    (w, h), base = cv2.getTextSize(text, font, scale, thickness)
    cv2.rectangle(img, (org[0]-2, org[1]-h-2), (org[0]+w+2, org[1]+base+2),
                  (0,0,0), -1, cv2.LINE_AA)
    cv2.putText(img, text, org, font, scale, outline, outline_th, cv2.LINE_AA)
    cv2.putText(img, text, org, font, scale, color,   thickness, cv2.LINE_AA)

def row_col_to_chess_notation(r:int,c:int)->str:
    return f"{chr(ord('a')+c)}{8-r}"

#aruco marker detection
def detect_board_corners(frame:np.ndarray):
    gray   = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    params = cv2.aruco.DetectorParameters()
    params.cornerRefinementMethod = cv2.aruco.CORNER_REFINE_SUBPIX
    corners, ids, _ = cv2.aruco.detectMarkers(gray, ARUCO_DICT, parameters=params)
    if ids is None:                          # nothing found
        return None
    id_idx = {int(i[0]): k for k,i in enumerate(ids)}
    if not all(t in id_idx for t in ID2POS): # need all 4 tags
        return None

    INNER = {0:2, 1:3, 2:0, 3:1}             # index of inner corner for each tag
    ordered = np.zeros((4,2), np.float32)    # TL,TR,BR,BL
    for tag,slot in ID2POS.items():
        idx = INNER[tag]
        ordered[slot] = corners[id_idx[tag]][0][idx]
    return ordered

#piece detection
def detect_pieces(board_img:np.ndarray, yolo:YOLO):
    overlay   = board_img.copy()
    board_arr = [["." for _ in range(8)] for _ in range(8)]

    for box in yolo(board_img, verbose=False)[0].boxes:
        x1,y1,x2,y2 = box.xyxy[0].cpu().numpy()
        cx,cy       = (x1+x2)/2, (y1+y2)/2
        row,col     = int(cy//SQUARE_PX), int(cx//SQUARE_PX)
        row = max(0,min(7,row));  col = max(0,min(7,col))

        label = yolo.names[int(box.cls[0])]
        code  = PIECE_CODE.get(label.replace("-","_"))
        if code:
            board_arr[row][col] = code

        cv2.rectangle(overlay,(int(x1),int(y1)),(int(x2),int(y2)),(0,255,0),2)
        txt = f"{label} {float(box.conf[0]):.2f}  {row_col_to_chess_notation(row,col)}"
        draw_text_with_outline(overlay, txt, (int(x1), int(y1)-6), scale=0.48)
    return board_arr, overlay
