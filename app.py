# -*- coding: utf-8 -*-
"""
Created on Sat Dec 22 22:09:51 2018

@author: 21wolgab
"""

from flask import Flask
from flask import request
from flask import render_template


app = Flask(__name__)

@app.route('/')
def my_form():
    #return render_template("appHTML.html") # this should be the name of your html file
	print("test2")

@app.route('/', methods=['POST'])
def my_form_post():
    print("test")
   

if __name__ == '__main__':
    app.run()
