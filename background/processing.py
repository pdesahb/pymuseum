import pathlib

import cv2

# default values, not very pretty
WIDTH = 1920
HEIGHT = 1080


def create_background(img, dark=.8):
    """
    Create the background image from the input

    Resize the image to take the whole screen, blurs it and darkens it
    """
    h_ratio = HEIGHT / img.shape[0]
    w_ratio = WIDTH / img.shape[1]
    bgd = cv2.resize(img, (0, 0), fx=w_ratio, fy=h_ratio)
    bgd = cv2.blur(bgd, (HEIGHT//15,  WIDTH//15))
    bgd = (dark * bgd).astype('uint8')
    return bgd


def resize_image(img, max_ratio=.9):
    """
    Resize the image to fit on the screen

    Only reduce the image size as not to low quality pictures
    """
    h_ratio = img.shape[0] / HEIGHT
    w_ratio = img.shape[1] / WIDTH
    ratio = max(h_ratio, w_ratio)
    ratio = max_ratio/ratio if ratio >= max_ratio else 1
    img = cv2.resize(img, (0, 0), fx=ratio, fy=ratio)
    return img


def combine_images(img, dark=.8, max_ratio=.9):
    """
    Create and combine the foreground and background images
    """
    bgd = create_background(img, dark=dark)
    img = resize_image(img, max_ratio=max_ratio)
    # center the image on the screen
    img_h, img_w, _ = img.shape
    off_h = (HEIGHT - img_h) // 2
    off_w = (WIDTH - img_w) // 2
    bgd[off_h:off_h+img_h, off_w:off_w+img_w, :] =img
    return bgd

def annotate_image(img, text):
    """
    Put text on the bottom left corner of an image
    """
    font = cv2.FONT_HERSHEY_COMPLEX
    bottom_left = (30, HEIGHT - 10)
    scale = 1
    color = (255,255,255)
    line_type = 2
    cv2.putText(img, text, bottom_left, font, scale, color, line_type)
    return img

def museumify(img, title, dark=.8, max_ratio=.9):
    """
    Put image on dilated background and add caption
    """
    pretty_image = combine_images(image, dark=dark, max_ratio=max_ratio)
    return annotate_image(pretty_image, title)
