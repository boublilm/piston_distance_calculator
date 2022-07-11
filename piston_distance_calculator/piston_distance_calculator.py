import math
import cv2
import matplotlib.pyplot as plt
import plotly.express as px


def process_image(path, sticker_color, resize=None):
    """
    :param path: path for frame
    :param sticker_color: tuple of the sticker color (Lower_bound_RGB, Higher_bound_RGB)
    :param resize: if its not the first frame it will take resize dimensions
    :return: returns the centers of the stickers
    """
    img = cv2.imread(path)
    # Resizes frames to the dimensions of the first frame.
    if resize:
        img = cv2.resize(img, resize)

    # Converting image to HSV
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    # Filtering by the colors of the stickers
    lower = sticker_color[0]
    upper = sticker_color[1]
    mask = cv2.inRange(hsv, lower, upper)

    # Finding Contours
    contours = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    contours = contours[0] if len(contours) == 2 else contours[1]
    contours = sorted(contours, key=lambda x: cv2.contourArea(x), reverse=True)

    # Creating an Image to display the stickers positions
    original = img.copy()
    centers = []
    for c in contours:
        if cv2.contourArea(c) < 200:
            continue
        x, y, w, h = cv2.boundingRect(c)
        centers.append((x + (w / 2), y + (h / 2)))
        cv2.rectangle(original, (x, y), (x + w, y + h), (36, 255, 12), 2)

    plt.imshow(original)
    plt.show()
    return centers


def calculate_distance(p1, p2):
    """
    :param p1: tuple (x,y) for point 1
    :param p2: tuple (x,y) for point 2
    :return: the distance between them
    """
    return math.sqrt((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2)


def piston_difference(paths_arr, sticker_color):
    """
    :param paths_arr: List of all frame paths
    :param sticker_color: tuple of the sticker color (Lower_bound_RGB, Higher_bound_RGB)
    :return: returns the distances between all the frames.
    """
    distances = []
    first_shape = cv2.imread(paths_arr[0]).shape[:2]
    first_shape = (first_shape[1], first_shape[0])

    centers = process_image(paths_arr[0], sticker_color)
    distances.append(calculate_distance(centers[0], centers[1]))
    for path in paths_arr[1:]:
        centers = process_image(path, sticker_color, first_shape)
        distances.append(calculate_distance(centers[0], centers[1]))

    return distances


def generate_graphs(distance_lst):
    """
    :param distance_lst: Distance lists (from piston_difference)
    :return: None
    Show plot - Distance (Pixels) Per Frame
    """
    fig = px.line(y=distance_lst, x=[i for i in range(len(distance_lst))],
                  title="Distance (Pixels) Per Frame")

    fig.update_layout(xaxis_title="Frames", yaxis_title="Distance")
    fig.show()
