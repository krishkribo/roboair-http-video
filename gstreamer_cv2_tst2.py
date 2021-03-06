#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Feb  6 19:56:38 2017

@author: krishna
"""

from __future__ import unicode_literals
from flask import Flask,Response
import subprocess
import cv2


app=Flask(__name__)
class videocamera(object):
    
    def __init__(self):
        self.cptr=cv2.VideoCapture(0)
    def get_frame(self):
        img=self.img_processing()
        ret, jpeg=cv2.imencode('.jpg',img)
        return jpeg.tobytes()
    
    def img_processing(self):
         while True:
             ret,frame=self.cptr.read()
             
             img=cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
             cv2.imshow('image',img)
         return frame 
def gen(videocamera):
    while True:
        frame=videocamera.get_frame()
        yield(b'--frame\r\n'
              b'content-'
              b'Type=image/jpeg\r\n\r\n'+frame+b'\r\n\r\n')
#     cv2.DestoryallWindows()
@app.route('/',methods=["GET"])
def index():
    return '<h1>cv2_video_streaming</h1><img src="/video"/>'
@app.route('/video')
def video():
    return Response(gen(videocamera()),mimetype='mutipart/x-mixed-replace;boundary=--spionisto')

if __name__=="__main__":
    app.debug=True
    app.run(host='0.0.0.0',port=10000)
    
