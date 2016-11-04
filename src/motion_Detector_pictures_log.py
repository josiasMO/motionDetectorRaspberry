import io
import time, datetime
import picamera 
import cv2
import cv2.cv as cv
import numpy as np
from time import sleep
import picamera as camera
import logging

import os as os


# A simple Motion Detection algorithm.
class MotionDetection:

#Function to create 3 news objects
    def __init__(self):
        self.__image0 = None
        self.__image1 = None
        self.__image2 = None


        # Configurations
        # Change these to adjust sensitive of motion
        self._MOTION_LEVEL = 500000
        self._THRESHOLD = 35

#Function to update the images: Change image 2 for the 1, one for the zero and create a new at zero
    def _updateImage(self, image):
        self.__image2 = self.__image1
        self.__image1 = self.__image0
        self.__image0 = image

#Function to see if the three necessary pictures were taken
    def _ready(self):
        return self.__image0 != None and self.__image1 != None and self.__image2 != None

#Function that compares the 3 images to detect motion
    def _getMotion(self):
        if not self._ready():
            return None

#Make the absolut difference between the images and the compare bit per bit the difference
        d1 = cv2.absdiff(self.__image1, self.__image0)
        d2 = cv2.absdiff(self.__image2, self.__image0)
        result = cv2.bitwise_and(d1, d2)

        (value, result) = cv2.threshold(result, self._THRESHOLD, 255, cv2.THRESH_BINARY)

        scalar = cv2.sumElems(result)

        print (" - scalar:", scalar[0], scalar)
        return scalar

#First update the pictures and the check if the motion was sufficient good. 
    def detectMotion(self, image):
        self._updateImage(image)

        motion = self._getMotion()
        if motion and motion[0] > self._MOTION_LEVEL:
            return True
        return False

#Save the image of the motion, it will be substituted by the video record.
    def saveImage(self, file_name):
    	#get the date to save the directory with the actual day
    	date = datetime.datetime.now().strftime("%Y-%m-%d")
    	
    	#get the actual directory of the aplication 
    	actual = os.getcwd() 
    	
    	#test to see if the directory with the date already exist 
    	if os.path.exists(date): 
    		os.chdir(date) # go to the directory date if it exist 

	#if the directory do not exist then, create the directory and access it
    	else : 
    		os.mkdir(date)
    		print('Directory created: ' + date)
    		os.chdir(date)
    		
    	#save the image on the directory date	
    	cv2.imwrite(file_name, self.__image0)
    	print("  - Image saved:", file_name)	
	#return to the main directory of the aplication
    	os.chdir(actual)

#Function that create the logs inside the archive.
def log_start(alarm):

	if alarm :
		logging.warning(datetime.datetime.now().strftime("%Y/%m/%d-%H:%M:%S") + ' Event with the alarm system on.')
	else : 
		logging.warning(datetime.datetime.now().strftime("%Y/%m/%d-%H:%M:%S") + ' Record from motion detection with the alarm off.')
	
	return datetime.datetime.now().strftime("%Y/%m/%d-%H:%M:%S")
	

#Function that close the logs inside the archive.
def log_finish(date_time):
	logging.warning(datetime.datetime.now().strftime("%Y/%m/%d-%H:%M:%S") + ' End of the event started at '+ date_time)

#Function to control the lights using the hour of the day.
def lights():
	current_time = datetime.datetime.now().strftime("%H%M")

	if (int(current_time) > 1800) or (int(current_time) < 700):
		return True;
		print("Turning on the lights")
	else:
		return False;
		



#Initiate the execution of the code.
def process():
    
    print("Initializing camera...")
    with picamera.PiCamera() as camera:
        #camera.start_preview()
        print("Setting focus and light level on camera...")


        print("Initializing the CameraDetection...")
        detection = MotionDetection()
	
        logging.basicConfig(filename=datetime.datetime.now().strftime("%Y-%m-%d")+'.txt',level=logging.DEBUG)
	 
        count = 0

        while True:
           
            print("Capture picture...")
            # Create the in-memory stream
            stream = io.BytesIO()
            camera.capture(stream, format='jpeg')

            # Construct a numpy array from the stream
            data = np.fromstring(stream.getvalue(), dtype=np.uint8)
            # "Decode" the image from the array, preserving colour
            image = cv2.imdecode(data, 1)
            
            ctrl = 1
            alarm_on = True
            
            if detection.detectMotion(image):

            	start_log = log_start(alarm_on)
            	
            	light_on_off = lights()
                
                	
            	while ctrl < 10:
            	    tstmp = datetime.datetime.now().strftime("%Y-%m-%d-%H:%M:%S")
            	    image_file  = "image_%s_%05d.jpg" % (tstmp, count)
            	    count += 1
            	    detection.saveImage(image_file)
            	    print (ctrl)

            	    stream2 = io.BytesIO()
            	    camera.capture(stream2, format='jpeg')
            	    data2 = np.fromstring(stream2.getvalue(), dtype=np.uint8)
            	    image2 = cv2.imdecode(data2, 1)

            	    test = detection.detectMotion(image2)
            	    if test == False:
                    	ctrl = ctrl +1
            	    else :
                    	ctrl = 1
                
            	if light_on_off == True: 
                	light_on_off = False
                	print("Turning of the lights")
	    	
            	log_finish(start_log)

                


if __name__ == "__main__":
    process()
    
    
    
    
    
    