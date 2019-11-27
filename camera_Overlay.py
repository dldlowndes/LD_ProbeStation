'''
Overlay a big square and 4 little squares. Corresponding to the LED chip
carrier and 4 LED chips to be placed inside it. The chip carrier size (in
pixels) is controllable to cater for a variable microscope magnification.
The 4 LEDs are centred on the centre of the chip carrier with a user defined
spacing.

Chip carrier size is 3mm sq?
LEDs are 400um sq?
'''

import cv2


def DrawGuides_Square(frame, square_Size, led_Sep_Microns):
    middle = (frame.shape[0]/2, frame.shape[1]/2)
    topLeft = (
            int(middle[1]-(square_Size/2)),
            int(middle[0]+(square_Size/2))
            )
    bottomRight = (
            int(middle[1]+(square_Size/2)),
            int(middle[0]-(square_Size/2))
            )

    # Squares around the LEDs
    # LED size is a fixed proportion of the chip carrier size
    led_Size = square_Size / 10
    # translate a value in microns to a value in pixels.o
    led_Sep = led_Sep_Microns / (3000 / square_Size)
    leds = [
            [(int(middle[1]+(led_Sep/2)),
              int(middle[0]+(led_Sep/2))),
             (int(middle[1]+((led_Sep/2)+led_Size)),
              int(middle[0]+((led_Sep/2)+led_Size)))],
            [(int(middle[1]+(led_Sep/2)),
              int(middle[0]-(led_Sep/2))),
             (int(middle[1]+((led_Sep/2)+led_Size)),
              int(middle[0]-((led_Sep/2)+led_Size)))],
            [(int(middle[1]-(led_Sep/2)),
              int(middle[0]+(led_Sep/2))),
             (int(middle[1]-((led_Sep/2)+led_Size)),
              int(middle[0]+((led_Sep/2)+led_Size)))],
            [(int(middle[1]-(led_Sep/2)),
              int(middle[0]-(led_Sep/2))),
             (int(middle[1]-((led_Sep/2)+led_Size)),
              int(middle[0]-((led_Sep/2)+led_Size)))]
            ]
    cv2.rectangle(frame, topLeft, bottomRight, (255, 0, 0), 2)
    for led in leds:
        cv2.rectangle(frame, led[0], led[1], (0, 0, 255), 1)

def DrawGuides_Circles(frame, square_Size, led_Sep_Microns):
    middle = (frame.shape[0]/2, frame.shape[1]/2)
    topLeft = (
            int(middle[1]-(square_Size/2)),
            int(middle[0]+(square_Size/2))
            )
    bottomRight = (
            int(middle[1]+(square_Size/2)),
            int(middle[0]-(square_Size/2))
            )

    # Squares around the LEDs
    # LED size is a fixed proportion of the chip carrier size
    led_Size = square_Size / 50
    # translate a value in microns to a value in pixels.
    led_Sep = led_Sep_Microns / (3000 / square_Size)
    # circles defined by centres so get the spacing between the centres.
    centre_Sep = led_Sep + int(led_Size/2)
    leds = [
            (int(middle[1]) + int(centre_Sep/2),
             int(middle[0]) + int(centre_Sep/2)),
            (int(middle[1]) + int(centre_Sep/2),
             int(middle[0]) - int(centre_Sep/2)),
            (int(middle[1]) - int(centre_Sep/2),
             int(middle[0]) + int(centre_Sep/2)),
            (int(middle[1]) - int(centre_Sep/2),
             int(middle[0]) - int(centre_Sep/2))
            ]
    cv2.rectangle(frame, topLeft, bottomRight, (255, 0, 0), 2)
    for led in leds:
        cv2.circle(frame, led, int(led_Size), (0, 0, 255), 1)

# Init video and grab a frame to get the image parameters.
video = cv2.VideoCapture(2)
# video.set(cv2.CAP_PROP_EXPOSURE, -1)
ret, frame = video.read()

# Sliders to choose the size of the chip carrier square and LED separation.
cv2.namedWindow("Sizes")
cv2.createTrackbar("Carrier size",
                   "Sizes",
                   480, min(frame.shape[:2]), lambda x: x)
cv2.createTrackbar("LED separation", "Sizes", 200, 800, lambda x: x)

while(True):
    square_Size = cv2.getTrackbarPos("Carrier size", "Sizes")
    if square_Size == 0:
        square_Size = 1 # Avoid divide by zero!
    led_Sep_Microns = cv2.getTrackbarPos("LED separation", "Sizes")

    ret, frame = video.read()
    DrawGuides_Circles(frame, square_Size, led_Sep_Microns)

    frame = cv2.resize(frame, (1280, 1024), cv2.INTER_LINEAR)

    cv2.imshow("Frame", frame)
    if (cv2.waitKey(1) & 0xFF) == ord('q'):
        break

video.release()
cv2.destroyAllWindows()
