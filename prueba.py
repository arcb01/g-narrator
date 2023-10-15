import numpy as np
from sklearn.neighbors import KDTree

nodes = np.array([(63, 15), (591, 15), (591, 43), (63, 43), (1713, 20), (1850, 20), (1850, 41), (1713, 41), (3083, 11), (3229, 11), (3229, 42), (3083, 42), (101, 71), (181, 71), (181, 89), (101, 89), (815, 71), (909, 71), (909, 98), (815, 98), (996, 68), (1089, 68), (1089, 95), (996, 95), (1176, 74), (1234, 74), (1234, 95), (1176, 95), (1352, 65), (1449, 65), (1449, 101), (1352, 101), (1535, 70), (1638, 70), (1638, 98), (1535, 98), (101, 111), (272, 111), (272, 132), (101, 132), (789, 111), (1212, 111), (1212, 169), (789, 169), (1832, 109), (2085, 109), (2085, 145), (1832, 145), (160, 149), (194, 149), (194, 167), (160, 167), (153, 178), (273, 178), (273, 264), (153, 264), (868, 196), (1395, 196), (1395, 312), (868, 312), (154, 278), (191, 278), (191, 299), (154, 299), (154, 310), (199, 310), (199, 331), (154, 331), (152, 342), (303, 342), (303, 796), (152, 796), (915, 339), (1464, 339), (1464, 422), (915, 422), (807, 399), (836, 399), (836, 420), (807, 420), (730, 673), (748, 673), (748, 694), (730, 694), (730, 740), (748, 740), (748, 793), (730, 793), (151, 810), (308, 810), (308, 1057), (151, 1057), (797, 958), (885, 958), (885, 976), (797, 976), (915, 958), (981, 958), (981, 976), (915, 976), (1012, 958), (1094, 958), (1094, 976), (1012, 976), (1125, 958), (1178, 958), (1178, 976), (1125, 976), (1208, 958), (1344, 958), (1344, 976), (1208, 976), (3258, 955), (3303, 955), (3303, 976), (3258, 976), (797, 992), (1926, 992), (1926, 1049), (797, 1049), (3176, 996), (3382, 996), (3382, 1187), (3176, 1187), (154, 1071), (302, 1071), (302, 1092), (154, 1092), (727, 1068), (748, 1068), (748, 1089), (727, 1089), (796, 1064), (2060, 1064), (2060, 1189), (796, 1189), (154, 1103), (221, 1103), (221, 1124), (154, 1124), (153, 1137), (233, 1137), (233, 1163), (153, 1163), (730, 1135), (748, 1135), (748, 1156), (730, 1156), (798, 1210), (3048, 1210), (3048, 1312), (798, 1312), 
(3076, 1264), (3099, 1264), (3099, 1282), (3076, 1282), (972, 1328), (1312, 1328), (1312, 1360), (972, 1360), (101, 1348), (175, 1348), (175, 1366), (101, 1366), (101, 1380), (181, 1380), (181, 1398), (101, 1398), (59, 1408), (721, 1408), (721, 1437), (59, 1437), (2607, 1408), (2798, 1408), (2798, 1434), (2607, 1434), (2831, 1412), (2946, 1412), (2946, 1433), (2831, 1433), (2992, 1412), (3223, 1412), (3223, 1433), 
(2992, 1433), (3245, 1408), (3377, 1408), (3377, 1434), (3245, 1434)]).reshape(-1, 2)

node = np.array((100, 100)).reshape(1, -1)

def eltree(node, nodes):
    neighbours = 3

    kdtree = KDTree(nodes)
    _, ind = kdtree.query(node, k=neighbours)   
    return ind.flatten()

def find_nearest_detections(mouse_pos):
    # Convert list of lists to list of tuples
    # det_rect = [tuple(p) for det in self.detections for p in det[0]]
    # Find the closest point of the detection (rectangle) to the mouse position
    
    indices_closest_points = eltree(mouse_pos, nodes)
    result = []
    for ind in indices_closest_points:
        print(type(ind))
        #result.append(det_rect[ind])


find_nearest_detections(node)

selected_candidates = [[1312 1096] 
                        [1312 1065] 
                        [1344  976]]
detections = [[[[63, 15], [591, 15], [591, 43], [63, 43]], 'File Edit Selection View Go Run Terminal Help'], [[[1713, 20], [1850, 20], [1850, 41], [1713, 41]], 'gaming-narrator'], [[[3083, 11], [3116, 11], [3116, 42], [3083, 42]], '0'], [[[3161, 11], [3229, 11], [3229, 42], [3161, 42]], '0 08'], [[[101, 71], [234, 71], [234, 92], [101, 92]], 'RUN AND DEBUG'], [[[461, 64], [632, 64], [632, 100], [461, 100]], 'No Configurations'], [[[816, 71], [909, 71], [909, 95], [816, 95]], 'apppy M'], [[[996, 74], [1054, 74], [1054, 95], [996, 95]], 'runpy'], [[[1098, 68], [1116, 68], [1116, 89], [1098, 89]], 'X'], [[[1175, 71], [1269, 71], [1269, 98], [1175, 98]], 'ocr py M'], [[[1354, 68], [1469, 68], [1469, 99], [1354, 99]], 'pruebapy U'], [[[1551, 70], [1654, 70], [1654, 98], [1551, 98]], 'setuppy M'], [[[1736, 67], [2085, 67], [2085, 145], [1736, 
145]], 'utilspy M #M < * : 0 0'], [[[101, 111], [191, 111], [191, 132], [101, 132]], 'VARIABLES'], [[[789, 110], [1212, 110], [1212, 169], [789, 169]], 'garrator runpy from app import App, settings'], [[[868, 
196], [1395, 196], [1395, 312], [868, 312]], 'if _name_ main__ LANGUAGE en Language for TTS GPU True Use GPU for OCR VOICE_SPEED 150 Voice speed for TTS'], [[[915, 339], [1464, 339], [1464, 423], [915, 423]], 
'tts, ocr settings( LANGUAGE , GPU , VOICE_SPEED) App(tts, ocr) run()'], [[[15, 351], [59, 351], [59, 473], [15, 473]], 'G'], [[[807, 399], [836, 399], [836, 420], [807, 420]], '10'], [[[101, 611], [527, 611], [527, 701], [101, 701]], 'WATCH self.OCR get_detections: not available detection: not available'], [[[101, 891], [199, 891], [199, 912], [101, 912]], 'CALL STACK'], [[[695, 893], [756, 893], [756, 912], [695, 912]], 'Running'], [[[113, 923], [281, 923], [281, 1015], [113, 1015]], 'MainThread Thread (listen) Thread (process)'], [[[678, 926], [753, 926], [753, 944], [678, 944]], 'RUNNING'], [[[678, 958], [753, 958], [753, 976], [678, 976]], 'RUNNING'], [[[797, 958], [885, 958], [885, 976], [797, 976]], 'PROBLEMS'], [[[915, 958], [981, 958], [981, 976], [915, 976]], 'OUTPUT'], [[[1012, 958], [1094, 958], [1094, 976], [1012, 976]], 'TERMINAL'], [[[1125, 958], [1178, 958], [1178, 976], [1125, 976]], 'PORTS'], [[[1208, 958], [1344, 958], [1344, 976], [1208, 976]], 'DEBUG CONSOLE'], [[[3258, 955], [3306, 955], [3306, 976], [3258, 
976]], '+v'], [[[678, 990], [753, 990], [753, 1008], [678, 1008]], 'RUNNING'], [[[798, 995], [3048, 995], [3048, 1049], [798, 1049]], 'env) PS C: |Users |Arnau |Desktoplgithub repos gaming-narrator> C: cd c: |Users | Arnau | Desktoplgithub repos Igaming-narrator c: |Users | Arnau | Desktoplgithub repos gaming-narrator| env| ScriptsIpython exe JUsers| Arnaul_vscodelextensionslms python python 2023-18 @lpythonFiles | libIpython |debugpy ladapter/ .  / = Idebugpy | launcher 54347\' C: |Users |Arnau|Desktoplgithub repos Igaming-narratorlgarratorlrun.py"'], [[[3076, 1001], [3099, 1001], [3099, 1016], [3076, 1016]], 'C:'], [[[3176, 996], [3382, 996], [3382, 1187], [3176, 1187]], 'powershell powershell powershell Python Debug Console Python powershell'], [[[974, 1065], [1312, 1065], [1312, 1096], [974, 1096]], 'Gaming Narrator is now running'], [[[101, 1280], [218, 1280], [218, 1301], [101, 1301]], 'BREAKPOINTS'], [[[59, 1312], [721, 1312], [721, 1437], [59, 1437]], 'Raised Exceptions Uncaught Exceptions User Uncaught Exceptions 89 hover_feature* 9 00 A 0 (4) 0 & Git Graph GIST [Create Profile]'], [[[2607, 1408], [2798, 1408], [2798, 1434], [2607, 1434]], 'Ln 10, Col 12 Spaces:'], [[[2831, 1412], [2946, 1412], [2946, 1433], [2831, 1433]], 'UTF-8 CRLF'], [[[2992, 1412], [3223, 1412], [3223, 1433], [2992, 1433]], "Python 3.10.8 ('env': venv)"], [[[3269, 1412], [3330, 1412], [3330, 1433], [3269, 1433]], 'Go Live']]

import numpy as np

selected_candidates = np.array([[1312, 1096], [1312, 1065], [1344, 976]])

detections = [
    [np.array([[(63, 15), (591, 15), (591, 43), (63, 43)]), 'File Edit Selection View Go Run Terminal Help'],
    [np.array([(1713, 20), (1850, 20), (1850, 41), (1713, 41)]), 'gaming-narrator'],
    # Add more data as needed
]

matching_detections = []

for detection in detections:
    for candidate in selected_candidates:
        if any(np.all(candidate == point, axis=1) for point in detection[0]):
            matching_detections.append(detection)

if matching_detections:
    print("Matching detections:")
    for detection in matching_detections:
        print(detection)
else:
    print("No matching detections found.")

