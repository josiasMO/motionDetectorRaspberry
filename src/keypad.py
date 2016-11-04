import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BOARD)

MATRIX = [[1,2,3,'A'],
          [4,5,6,'B'],
          [7,8,9,'C'],
          ['*',0,'#','D']]

ROW = [7,11,13,15] #Inputs of the keypad
COL = [12,16,18,22] #Outputs of the keypad

for j in range(4):
    GPIO.setup(COL[j], GPIO.OUT)
    GPIO.output(COL[j],1)

for i in range(4):
    GPIO.setup(ROW[i], GPIO.IN, pull_up_down = GPIO.PUD_UP)


#function that read the input
def read(num): #Parameter num is the number of inputs necessary.
    try:
        passcode = ""
        while(num):
            for j in range(4):
                GPIO.output(COL[j],0)

                for i in range(4):
                    if GPIO.input(ROW[i]) == 0:
                        
                        passcode += str(MATRIX[i][j])#append the key pressed on the keypad
                        num -= 1 
                        while(GPIO.input(ROW[i]) == 0):
                            pass

                GPIO.output(COL[j],1)
            
        return passcode
            
    except KeyboardInterrupt:
        GPIO.cleanup()




if __name__ == "__main__":
    
    passcode = "0000"  #Default passcode
    sound_alarm = False #Sound Alarm
    global alarm_on  #Variable that should be used in the motion_detection 
    while(True):
        print("Menu: A) Activate the alarm; B) Deactivate the alarm; C) Redefine Password")
        opt = read(1)
        print(str(opt))

        if(opt == "A" or opt == "B" or opt == "C"):      	
            tentatives = 3  #3 tentatives before alarm sound
            while(tentatives):
                print("Enter the actual passcode: ")
                temp = read(4)
                print(str(temp))
                if(temp == passcode):
                    alarm_on = (opt == "A")
	            print("Alarm On: "+ str(alarm_on))
                    if(opt == "C"):
                        print("Enter the new passcode: ")
                        passcode = read(4)
                        print("New passcode: " + passcode)
                    break
                else:
                    print("Wrong password")
                    tentatives -= 1
                if(tentatives == 0):
                    sound_alarm = True
                
        else: 	
            print("Invalid Option")
    
    

