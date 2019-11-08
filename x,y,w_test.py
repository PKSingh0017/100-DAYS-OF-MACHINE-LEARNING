import numpy as np
import cv2
import smbus
import time
import math
bus=smbus.SMBus(1)
address=0x04
def writeNumber(value):
    bus.write_byte(address,value)
    print(value)
    return -1
def readNumber():
    number=bus.read_byte(address)
    return number    
cap = cv2.VideoCapture(0)
cap2 = cv2.VideoCapture(1)

#**************for camera 1************************# 
def nothing(x):
    pass

# Create a black image, a window
cv2.namedWindow('image')

# create trackbars for color change
cv2.createTrackbar('Rl','image',0,255,nothing)
cv2.createTrackbar('Gl','image',0,255,nothing)
cv2.createTrackbar('Bl','image',0,255,nothing)
cv2.createTrackbar('Rh','image',255,255,nothing)
cv2.createTrackbar('Gh','image',255,255,nothing)
cv2.createTrackbar('Bh','image',255,255,nothing)
while(True):
    
    # Capture frame-by-frame
    ret, frame = cap.read()
    rl = cv2.getTrackbarPos('Rl','image')
    gl = cv2.getTrackbarPos('Gl','image')
    bl = cv2.getTrackbarPos('Bl','image')
    rh = cv2.getTrackbarPos('Rh','image')
    gh = cv2.getTrackbarPos('Gh','image')
    bh = cv2.getTrackbarPos('Bh','image')
    blur3 = cv2.medianBlur(frame,5)
    lower=np.array([rl, gl, bl])
    upper=np.array([rh,gh, bh])
    frame=frame.astype('uint8')
    frame_HSV= cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)
    frame_threshold = cv2.inRange(frame_HSV, lower, upper)
    _,contours,hierarchy=cv2.findContours(frame_threshold, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    cv2.drawContours(frame,contours,-1,(0,255,0),3)
    cv2.drawContours(frame_threshold,contours,-1,(0,255,0),3)
    
    if len(contours)>0:   #to return number of contours detected
        lencontour=len(contours[0])
        cn=contours[0]
        for cnt in contours:
            if(lencontour<len(cnt)):
                lencontour=len(cnt)
                cn=cnt
        M = cv2.moments(cn)
        a,b,c,d = cv2.boundingRect(cn)
        if M['m00']>0:
            cx = int(M['m10']/M['m00'])
            cy = int(M['m01']/M['m00'])
            (x,y),radius = cv2.minEnclosingCircle(cnt)
            center = (int(x),int(y))
            radius = int(radius)
            cv2.line(frame,(a,b),(a,b+d),(0,255,0),8)
            cv2.line(frame,(a+c,b),(a+c,b+d),(0,255,0),8)
            cv2.circle(frame,center,radius,(0,255,0),2)
            cv2.circle(frame,(cx,cy), 5, (255,0,0), -1)
            cv2.rectangle(frame,(a,b),(a+c,b+d),(0,0,255),2)
    cv2.imshow('frame',frame)
    cv2.imshow('frame_threshold',frame_threshold)
#**************for camera 2************************#
    ret, frame2 = cap2.read()
    blur3 = cv2.medianBlur(frame2,5)
    frame_HSV2 = cv2.cvtColor(frame2, cv2.COLOR_BGR2HSV)
    frame_threshold2 = cv2.inRange(frame_HSV2, lower, upper)
    _,contours2,hierarchy2=cv2.findContours(frame_threshold2, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    cv2.drawContours(frame2,contours2,-1,(0,255,0),3)
    cv2.drawContours(frame_threshold2,contours2,-1,(0,255,0),3)
    
    if len(contours2)>0:   #to return number of contours detected
        lencontour2=len(contours2[0])
        cn2=contours2[0]
        for cnt2 in contours2:
            if(lencontour2<len(cnt2)):
                lencontour2=len(cnt2)
                cn2=cnt2
        M2 = cv2.moments(cn2)
        a2,b2,c2,d2 = cv2.boundingRect(cn2)
        if M2 ['m00']>0:
            cx2 = int(M2['m10']/M2['m00'])
            cy2 = int(M2['m01']/M2['m00'])
            (x2,y2),radius2 = cv2.minEnclosingCircle(cnt2)
            center2 = (int(x2),int(y2))
            radius2 = int(radius2)
            #for X and Y and W
            CX=(cx+cx2)/2
            CY=(cy+cy2)/2
            X=math.floor(CX)
            Y=math.floor(CY)
            #distanceY2=2.38*(Y-239)    #per change in 1cm value increment by 1
            #distanceX2=0.15*(X-319)
            #if(distanceX2!=0):
                #Wr=math.atan((distanceY2/distanceX2))
                #W=Wr*57.296
            cv2.line(frame2,(a2,b2),(a2,b2+d2),(0,255,0),8)
            cv2.line(frame2,(a2+c2,b2),(a2+c2,b2+d2),(0,255,0),8)
            cv2.circle(frame2,center2,radius2,(0,255,0),2)
            cv2.circle(frame2,(cx2,cy2), 5, (255,0,0), -1)
            cv2.rectangle(frame2,(a2,b2),(a2+c2,b2+d2),(0,0,255),2)
            
    writeNumber(X)
    writeNumber(Y)
    number=readNumber()
    cv2.imshow('frame2',frame2)
    cv2.imshow('frame_threshold2',frame_threshold2)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()
exit(0)
