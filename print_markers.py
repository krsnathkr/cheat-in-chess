import cv2
import os

aruco_dict = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_4X4_50)

os.makedirs("aruco_tags", exist_ok=True)
for marker_id in [0, 1, 2, 3]:
    img = cv2.aruco.generateImageMarker(aruco_dict, marker_id, 400) 
    cv2.imwrite(f"aruco_tags/aruco_{marker_id}.png", img)

print("Done → check the aruco_tags folder.")
