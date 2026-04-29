import time
import datetime
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
from gpiozero import LED, Buzzer
from w1thermsensor  import W1ThermSensor, Unit
import math

sensor = W1ThermSensor()
red = LED(18)
blue = LED(24)
buzzer = Buzzer(22)

plt.ion()

def main():
    #creating global variables to be used later
    blue.off()
    red.off()
    buzzer.off()
    Start_Time=time.time()
    X_Axis=np.array([])
    Y_Axis=np.array([])
    Date=datetime.datetime.now()
    Time=Date.strftime("%d_%m_%Y""_""%H")
    Past_Time=str(Time)
    #The main structure to that will be looped
    while True:
        Temp_C=Get_Temp()
         
        #preparing variables for display function
        Current_Time=time.time()-Start_Time
        Current_Time=int(Current_Time)
         
        X_Axis=np.append(X_Axis,[Current_Time])
        Y_Axis=np.append(Y_Axis,[Temp_C])

        #printing for user
        print(Temp_C, " Celsius")
        print(Current_Time, " Time")
         
        Display_Temp(X_Axis,Y_Axis)
        Save_Temp(Temp_C,Past_Time)
        time.sleep(5)
    
    
def Get_Temp():
        Temp_C = sensor.get_temperature(Unit.DEGREES_C)
        #alarm system parameters
        if Temp_C <= 20:
            blue.on()
        elif Temp_C >= 25:
            red.on()
        elif Temp_C >= 30:
            buzzer.on()
            Save_Alarm(Temp_C)
        elif Temp_C <= 15:
            buzzer.on()
            Save_Alarm(Temp_C)
        else:
            blue.off()
            red.off()
            buzzer.off()
        

        
        return Temp_C
    

def Display_Temp(X_Axis,Y_Axis):
    #adding to the graph to enhance and better inform
    plt.clf()
    Y_Axis=Y_Axis[-10:]
    X_Axis=X_Axis[-10:]
    plt.title("Temperature change")
    plt.xlabel("Time passed (Seconds)")
    plt.ylabel("Temperature(°C)")
    plt.axhline(y=25, linestyle='--', color='r')
    plt.axhline(y=20, linestyle='--', color='b')
    plt.axhline(y=30, linestyle='-', color='#000000')
    plt.axhline(y=15, linestyle='-', color='#000000')
    plt.plot(X_Axis,Y_Axis, marker = 'o' , color = '#000000')
    plt.pause(0.1)
    
def Save_Temp(Temp_C,Past_Time):
    #create date for file name and check if hour has passed
    Date=datetime.datetime.now()
    Time=Date.strftime("%d_%m_%Y""_""%H")
    New_Time=str(Time)
    print(New_Time)
    
    #create time variable to add to text file
    Temp_C=format(Temp_C,'.4f')
    Date=Date.strftime("%x"" ""%X"),Temp_C
    Date=str(Date)
    
    File_Name=Past_Time+"_Temperatures.txt"
    #check if hour has passed
    try:
        if Past_Time==New_Time:
            File=open(File_Name,"a")
            File.write(Date+"\n")
            File.close()
        else:
            Calculate(Past_Time,File_Name)
    #exception handling   
    except:
        File=open(File_Name,"x")
        File.close()
        Calculate(Past_Time,File_Name)
        
    Past_Time=New_Time

def Calculate(Past_Time,File_Name):
    Total_Temperature_Array=np.array([])
    Total_Time_Array=np.array([])
    #loop through every row in text file to get temperature and time
    with open(File_Name) as File:
        for X in File:
            Total_Temperature=X[28:31]
            Total_Temperature=float(Total_Temperature)
            Total_Temperature_Array=np.append(Total_Temperature_Array,[Total_Temperature])
            
            Total_Time=X[16:21]
            Total_Time=Total_Time.replace(":",".")
            Total_Time=float(Total_Time)

            Total_Time_Array=np.append(Total_Time_Array,[Total_Time])
    #plot the file into a graph
    File.close()
    plt.title("Temperature change")
    plt.xlabel("Time passed (Seconds)")
    plt.ylabel("Temperature(°C)")
    plt.plot(Total_Time_Array,Total_Temperature_Array, marker = 'o' , color = '#000000')
    plt.savefig(Past_Time)
    plt.pause(0.1)
    #calculate average and add to file
    Average=0
    for X in Total_Temperature_Array:
            Average+=X
    Average=Average/len(Total_Temperature_Array)
    Average=str(Average)
    File=open(File_Name,"a")
    File.write("Average is :"+Average+"\n")
    File.close()

def Save_Alarm(Temp_C):
    #save every time  alarm goes off
    File=open("Alarm.txt","a")
    Date=datetime.datetime.now()
    Date=Date.strftime("%x"" ""%X"),Temp_C
    Date=str(Date)
    print(Date)
    File.write(Date+" Alarm Activated.\n")
    File.close()
    
main()

    
        
