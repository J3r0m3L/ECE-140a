import cv2
import numpy as np
from PIL import Image
import pytesseract

from wsgiref.simple_server import make_server
from pyramid.config import Configurator
from pyramid.response import Response, FileResponse
import mysql.connector as mysql
from dotenv import load_dotenv
import os

#Filters out noise and crops image around plate, returns roi and corners of roi, location = coord
def detect_plate(img):
    # Add a Gaussian Blur to smoothen the noise
    print("line 15")
    blur = cv2.GaussianBlur(img.copy(), (11, 11), 0)

    thresh = cv2.adaptiveThreshold(blur ,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,\
            cv2.THRESH_BINARY,11,2)

    thresh = cv2.GaussianBlur(thresh, (9, 9), 0)
    print("line 28")
    thresh = cv2.adaptiveThreshold(thresh ,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,\
            cv2.THRESH_BINARY,11,2)

    # Invert the image to swap the foreground and background
    invert = 255 - thresh

    # Dilate the image to join disconnected fragments
    kernel = np.array([[0., 1., 0.], [1., 1., 1.], [0., 1., 0.]], np.uint8)
    dilated = cv2.dilate(invert, kernel)
    img_erosion = cv2.erode(img, kernel)

    contours, hierarchy = cv2.findContours(dilated, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    contours = sorted(contours, key=cv2.contourArea, reverse=True)[:15]

    # Find best polygon and get location
    location = None
    print(type(location))
    counter = 0

    # Finds rectangular contour
    for contour in contours:
        peri = cv2.arcLength(contour, True)
        approx = cv2.approxPolyDP(contour, 0.02*peri, True)
        if len(approx) == 4:
            counter += 1
            location = approx
            break
    print(counter)

    # Sudoku Specific: Transform a skewed quadrilateral
    def get_perspective(img, location, height = 600, width = 1200):
        pts1 = np.float32([location[0], location[3], location[1], location[2]])
        pts2 = np.float32([[0, 0], [width, 0], [0, height], [width, height]])

        # Apply Perspective Transform Algorithm
        matrix = cv2.getPerspectiveTransform(pts1, pts2)
        result = cv2.warpPerspective(img, matrix, (width, height))
        return result

    if type(location) != type(None):
        result = get_perspective(img, location)
        print("Corners of the contour are: ",location)
        return result, location
    else:
        print("No quadrilaterals found")
        return  result, [ [-1, -1], [-1, -1], [-1, -1], [-1, -1] ]

#Filter out noise to get treshold image for Arizona plate, returns treshold array and dummy location
def detect_arizona(img):
    hsv_image = cv2.cvtColor(img.copy(), cv2.COLOR_BGR2HSV)
    cv2.imwrite("hsv.png", hsv_image)

    range1 = np.array([20, 50, 20])
    range2 = np.array([120, 120, 120])

    mask = cv2.inRange(hsv_image, range1, range2)

    blur = cv2.GaussianBlur(mask, (25, 23), 0)
    thresh = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
    thresh = 255 - thresh

    return thresh, [ [-1, -1], [-1, -1], [-1, -1], [-1, -1] ]

#Uses pytesserct to get text from image, returns text found
def get_text(img):
    pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

    text = pytesseract.image_to_string (img, lang='eng', config='--psm 10 --oem 3 -c tessedit_char_whitelist=0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ')

    print("length: ", len(text))
    if len(text)==0:
        text = 'text not found'        
    
    return text

#Uses pytesserct to get text from Arizona plate, returns text found
def get_text_arizona(img):
    pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

    text = pytesseract.image_to_string (img, lang='eng', config='--psm 11 -c tessedit_char_whitelist=0123456789ABCDEFHIJLMNOPQRSTUWXZ')

    print("length: ", len(text))
    if len(text)==0:
        text = 'text not found'        
    
    return text

