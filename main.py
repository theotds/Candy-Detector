import cv2
import numpy as np
from Candy import Candy

candy_list = []

colors = {
        'gold': ((20, 20, 100), (30, 70, 200)),  # done
        'red': ((0, 0, 170), (13, 30, 230)),  # done
        'black': ((13, 0, 150), (20, 13, 255)),  # done
    }

def convex_hull(contours, image):
    for contour in contours:
        hull = cv2.convexHull(contour)
        cv2.drawContours(image, [hull], 0, 255, -1)


def process_stream():
    while cap.isOpened():
        ret, frame = cap.read()

        if not ret:
            break

        image = process(frame)

        cv2.imshow("tasmociag", image)

        if cv2.waitKey(5) & 0xFF == ord('q'):
            break


def getSimilarCandy(search_candy):
    for candy in candy_list:
        if candy.is_similar(search_candy):
            return candy
    return None


def detect_candy_color(hsv, x, y, w, h):
    # Crop the part of the image where the candy is
    candy_roi = hsv[y:y + h, x:x + w]

    dominant_color = get_dominant_color(candy_roi, colors)

    candy = Candy(dominant_color, (x, y, w, h))
    similar_candy = getSimilarCandy(candy)
    if similar_candy is None:
        candy_list.append(candy)
        print("candy added", candy.color)
    else:
        similar_candy.update((x, y, w, h))
    return dominant_color


def get_dominant_color(candy_roi, colors):
    max_pixels = 0
    dominant_color = "unknown"
    for color, (lower, upper) in colors.items():
        lower_hsv = np.array(lower, np.uint8)
        upper_hsv = np.array(upper, np.uint8)

        # Create a mask for the current color range
        mask = cv2.inRange(candy_roi, lower_hsv, upper_hsv)
        num_pixels = cv2.countNonZero(mask)

        if num_pixels > max_pixels:
            max_pixels = num_pixels
            dominant_color = color
    return dominant_color


def summary():
    color_counts = {}
    for candy in candy_list:
        if candy.color in color_counts:
            color_counts[candy.color] += 1
        else:
            color_counts[candy.color] = 1

    total_candies = len(candy_list)
    print(f'Total candies: {total_candies}')
    for color, count in color_counts.items():
        print(f'{color.capitalize()} Candy: {count}')

def bounding_box(contours, frame):
    # Convert BGR to HSV color space for color detection
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    for contour in contours:
        area = cv2.contourArea(contour)
        if area > 9000:
            x, y, w, h = cv2.boundingRect(contour)
            color = detect_candy_color(hsv, x, y, w, h)  # Detect the color of the candy
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)
            cv2.putText(frame, color.capitalize() + " candy", (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255),
                        2)


def process(frame):
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    image = cv2.GaussianBlur(gray_frame, (5, 5), 0)
    _, image = cv2.threshold(image, 100, 255, cv2.THRESH_BINARY)
    image = cv2.bitwise_not(image)

    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))

    # fill in  holes inside the contour
    image = cv2.morphologyEx(image, cv2.MORPH_CLOSE, kernel, iterations=7)
    # open small obejcts out of image
    image = cv2.morphologyEx(image, cv2.MORPH_OPEN, kernel, iterations=5)

    contours, _ = cv2.findContours(image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    convex_hull(contours, image)

    contours, _ = cv2.findContours(image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    bounding_box(contours, frame)

    return frame


# Load the video file
cap = cv2.VideoCapture('video/VideoRed1.mov')

process_stream()
summary()

cap.release()
cv2.destroyAllWindows()
