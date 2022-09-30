## Jerome Lam - PID:A15459972 and Kelvin Duong - PID:A15822315 

# Structure 
ece-140a-winter-2022-duongkelvin75/ece-140a-winter-2022-Jerome2L
- Lab 1
- Lab 2
- Lab 3
- Lab 4
- Lab 5
- Lab 6
	- Midterm 
		- public
			- basic.css
			- rest.js
		- app.py
		- index.html
		- init-db.py
    - Tutorials
        -Tutorial_1.png
        -Tutorial_2.png
	- .gitignore
	- README.md


## Tutorials
### Tutorial 1
In this tutorial, we learned how to use the Raspberry Pi, and some interesting caveats: enabling ssh and setting our internet network to the same one as the Raspberry Pi. We also learned new commands to log into our Raspberry Pi, run updates, and download libraries. 

![alt text](https://github.com/UCSD-ECE140/ece-140a-winter-2022-Jerome2L/blob/master/Lab%206/Tutorials/Tutorial_1.png)

### Tutorial 2
In this tutorial, we set up basic I/O on the raspberry pi. We set up the ultrasonic sensor according to the schematic. We then created a .py file and copied over the starting code. We were able to run the code with no issues. When it started running, it would print out the distance readings in cm and buzz. When we covered the sensor it output 0cm and stopped buzzing as expected from our interpretation of the code.

![alt text](https://github.com/UCSD-ECE140/ece-140a-winter-2022-Jerome2L/blob/master/Lab%206/Tutorials/Tutorial_2.png)

## Challenges
### Challenge 1

In this challenge, we built upon our knowledge from the previous labs and the tutorials to build hardware that inputs into a restful database and display them onto a webpage hosted on our server. We reused the ultrasonic sensor and the buzzer from the previous tutorial and chose to add a photoresistor that senses the light intensity level and outputs it as a voltage. We set up the hardware for the photoresistor according to the sensor tutorial. We collect 10 values at a rate of 1 Hz for both sensors and put them into a MySQL table. From our webpage, we have dropdown inputs for sensor, distance range, and voltage range along with a submit and buzz button. When submit is pressed it uses the sorting criteria from the page to dynamically inject the sorted sensor readings onto the page using a rest route. When the buzz button is pressed, it will use a rest route to call a function to buzz the buzzer for 1 second.

In order to test our project on another computer, you would have to download our code and set up the hardware to the correct pins. Then you would have to run the init-db.py file to create a database with a table in mysql from the sensor readings. Then you would have to run app.py to create the server. From there you can go to the localhost:6543 and interact with the page.

![hardware](https://github.com/UCSD-ECE140/ece-140a-winter-2022-Jerome2L/blob/master/Lab%206/Midterm/Midterm_Hardware.JPG)

[hardware demo](https://youtu.be/kU6EW680FFU)


