# Kelvin Duong A15822315 and Jerome Lam A15459972  ECE 140A Lab 7

# Intro:
In this lab we begin working with the raspberry pi camera and pytresseract. In the tutorials we set up the camera to take pictures and did some image processing and character recognition to crop and detect the text from a sudoku puzzle. In the challenge, we used what we learned in Tutorial 2 to crop images of license plates and read the characters from the plate. We then made a webpage that would upload the detected text to a mysql table at the request of the user.

# Structure 
ece-140a-winter-2022-duongkelvin75/ece-140a-winter-2022-Jerome2L
- Lab 1
- Lab 2
- Lab 3
- Lab 4
- Lab 5
- Lab 6
- Lab 7
	- Tutorials
		- Tutorial_1
			- test.png
			- camera_trial.py
		- Tutorial_2
			- sudoku_finder.py
			- sudoku_test.jpeg
			- Blur.png
			- Threshold.png
			- Inverted.png
			- Dilated.png
			- Result.png
			- sudoku_finder.py
	- Challenges
		- Challenge_1
		- detector.py
		- init-db.py
		- app.py
		- index.html
		-public
			- rest.js
			-images
				-Arizona_47.jpg
				- Contrast.jpg
				- Delaware_Plate.png
				- Result.png
		
# Tutorials

## Tutorial 1
In this tutorial, we set up the camera for the raspberry pi. We started by verifying that OpenCV was installed on raspberry pi. We then copied the code to take a picture. When we ran the code the first time the picture was very dark so we added the normalizing code and it turned out fine.

![test](https://github.com/UCSD-ECE140/ece-140a-winter-2022-Jerome2L/blob/master/Lab%207/Tutorials/Tutorial_1/test.jpg) 

This is the test photo from tutorial 1.


## Tutorial 2
In this tutorial, we preprocessed an image of a sudoku board. We started off by blurring the image to reduce noise and then thresholding, cropping, and dividing the image into individual squares. Finally, we used pytesseract to detect the numbers and store them in an array. 

# Challenges

## Challenge 1
In this challenge, we took three different images of license plates, read the text on all of them, and stored and displayed them using a pyramid backend and html/javascript frontend. Specifically, for the Delaware image and the Contrast image, we were able to filter and crop as in Tutorial 2 with a little fine-tuning and then read the text off of them. However for the Arizona_47 image we were unable to do that because the background matched too much with the borders of the license plate and the image was too noisy. So instead of filtering and cropping we used cv2.inrange function to grab only the text by it’s bold color, and then we fed it to Py Tesseract to read the text. We then created a webpage that when an image is selected, it runs the Detection program, stores the image in our mysql database, and displays the original image, the cropped/filtered image, and the detected text.

[website demo](https://youtu.be/CV8dpK90taA)
