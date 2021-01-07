import numpy as np
import cv2
import math

#LOADING HAND CASCADE
hand_cascade = cv2.CascadeClassifier('D:/Hand_Recognition-master/Hand_haar_cascade.xml')

while (True):
	frame = cv2.flip(frame,1)
	blur_frame = cv2.GaussianBlur(frame,(5,5),0) # BLURRING IMAGE TO SMOOTHEN EDGES

	hsv = cv2.cvtColor(blur_frame, cv2.COLOR_BGR2HSV)

	# define range of skin color in HSV
	lower_skin = np.array([0, 18, 73], dtype=np.uint8) #light
	upper_skin = np.array([22, 255, 200], dtype=np.uint8) #dark
	thresh1 = cv2.inRange(hsv, lower_skin, upper_skin)

	hand = hand_cascade.detectMultiScale(thresh1, 1.05, 5) # DETECTING HAND IN THE THRESHOLDE IMAGE
	mask = np.zeros(thresh1.shape, dtype = "uint8") # CREATING MASK
	for (x,y,w,h) in hand: # MARKING THE DETECTED ROI
		cv2.rectangle(frame,(x,y),(x+w,y+h), (122,122,0), 2) 
		cv2.rectangle(mask, (x,y),(x+w,y+h),255,-1)
	img2 = cv2.bitwise_and(thresh1, mask)
	final = cv2.GaussianBlur(img2,(7,7),0)	
	contours, hierarchy = cv2.findContours(final, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

	cv2.drawContours(frame, contours, 0, (255,255,0), 3)
	cv2.drawContours(final, contours, 0, (255,255,0), 3)

	if len(contours) > 0:
		cnt=contours[0]
		hull = cv2.convexHull(cnt, returnPoints=False)
		# finding convexity defects
		defects = cv2.convexityDefects(cnt, hull)
		count_defects = 0
		# applying Cosine Rule to find angle for all defects (between fingers)
		# with angle > 90 degrees and ignore defect
		if defects is not None:
			for i in range(defects.shape[0]):
				p,q,r,s = defects[i,0]
				finger1 = tuple(cnt[p][0])
				finger2 = tuple(cnt[q][0])
				dip = tuple(cnt[r][0])
				# find length of all sides of triangle
				a = math.sqrt((finger2[0] - finger1[0])**2 + (finger2[1] - finger1[1])**2)
				b = math.sqrt((dip[0] - finger1[0])**2 + (dip[1] - finger1[1])**2)
				c = math.sqrt((finger2[0] - dip[0])**2 + (finger2[1] - dip[1])**2)
				# apply cosine rule here
				angle = math.acos((b**2 + c**2 - a**2)/(2*b*c)) * 57.29
				# ignore angles > 90 and highlight rest with red dots
				if angle <= 90:
				    count_defects += 1
		# define actions required
		if count_defects == 1:
			cv2.putText(frame,"THIS IS 2", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 2, 2)
		elif count_defects == 2:
			cv2.putText(frame, "THIS IS 3", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 2, 2)
		elif count_defects == 3:
			cv2.putText(frame,"This is 4", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 2, 2)
		elif count_defects == 4:
			cv2.putText(frame,"THIS IS 5", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 2, 2)

	cv2.imshow('img',thresh1)
	cv2.imshow('frame',frame)
	cv2.imshow('img2',img2)
	
	if cv2.waitKey(1) & 0xFF == ord('q'):
		break

cap.release()
cv2.destroyAllWindows()
