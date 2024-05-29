# -*- coding: utf-8 -*-
"""
Created on Sun May 26 13:23:47 2024

@author: Edanur
"""

# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
import cv2
import imutils
import numpy as np
import pytesseract  #metin tanıma
pytesseract.pytesseract.tesseract_cmd = r'C:\Users\Edanur\AppData\Local\Programs\Tesseract-OCR\\tesseract.exe'

img = cv2.imread('C:\\Resim\\22.jpg',cv2.IMREAD_COLOR) #görüntü okuma
img = cv2.resize(img,(600,400)) #görüntü boyutunu belirli boyuta dönüştürme

gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)  #gri tonlamaya dönüştürme
gray = cv2.bilateralFilter(gray, 13, 15, 15) #kenarları korumak için

edged = cv2.Canny(gray, 30, 200) #kenarları tespit eden algoritma
contours = cv2.findContours(edged.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE) #kontur bulma
contours = imutils.grab_contours(contours) #kontur bulma                                       
contours = sorted(contours, key = cv2.contourArea, reverse = True)[:10] #en büyük 10 konturu seçeriz 
screenCnt = None
 

for c in contours:   #plaka konturunu bulma
    
    peri = cv2.arcLength(c, True) #kontur çerçevesi hesaplama
    approx = cv2.approxPolyDP(c, 0.018 * peri, True) #konturun yaklaşık temsili
 
    if len(approx) == 4:
        screenCnt = approx
        break

if screenCnt is None:
    detected = 0
    print ("No contour detected")
else:
     detected = 1

if detected == 1:
    cv2.drawContours(img, [screenCnt], -1, (0, 0, 255), 3) #kontur bulunduysa görselleştirme işlemi

mask = np.zeros(gray.shape,np.uint8) #gri tonlamalı görüntünün boyutunda sıfırlar dizisi oluşturur
new_image = cv2.drawContours(mask,[screenCnt],0,255,-1,) #kontur kullanarak maskeyi oluşturur.
new_image = cv2.bitwise_and(img,img,mask=mask)  #plaka alanını alır

(x, y) = np.where(mask == 255)  #piksel seçme
(topx, topy) = (np.min(x), np.min(y))
(bottomx, bottomy) = (np.max(x), np.max(y))
Cropped = gray[topx:bottomx+1, topy:bottomy+1]

text = pytesseract.image_to_string(Cropped, config='--psm 11') #plaka görüntüsünden metni okur
print("Plaka Tanıma Programlaması\n")
print("Plaka Numarası:",text)
img = cv2.resize(img,(500,300))
Cropped = cv2.resize(Cropped,(300,80))
cv2.imshow('Araba',img) #resim görüntüsünü çıkarır
cv2.imshow('Plaka',Cropped) #plaka görüntüsünü çıkarır

cv2.waitKey(0)
cv2.destroyAllWindows() #görüntü pencerelerini kapatır

