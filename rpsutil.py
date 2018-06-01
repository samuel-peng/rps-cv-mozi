# rpsutil.py
# Source: https://github.com/DrGFreeman/rps-cv
# This file defines variables and functions to ensure consistancy in capture and
# naming of images.

import glob
import time

import numpy as np

#import camera

# Define possible gestures as constants
ROCK = 0
PAPER = 1
SCISSORS = 2

# Define text labels corresponding to gestures
gestureTxt = {ROCK: 'rock', PAPER: 'paper', SCISSORS: 'scissors'}

# Define paths to raw image folders
imgPathsRaw = {ROCK: './img/rock/', PAPER: './img/paper/',
            SCISSORS: './img/scissors/'}

def cameraSetup():
    import camera
    """Returns a camera object with pre-defined settings."""

    # Settings
    size = 8
    frameRate = 40
    #awbFilename = 'awb_gains.txt'

    # Create Camera object
    print("Initializing camera")
    cam = camera.Camera()

    """
    # Check if white balance file exists
    if len(glob.glob(awbFilename)) != 0:
        # File exists, set camera white balance using gains from file
        print("Reading white balance gains from {}".format(awbFilename))
        cam.readWhiteBalance(awbFilename)
    else:
        # File does not exist. Prompt user to perform white balance.
        print("WARNING: No white balance file found. ")
        if input("Perform white balance (Y/n)?\n") != "n":
            print("Performing white balance.")
            print("Place a sheet of white paper in front of camera.")
            input("Press any key when ready.\n")
            cam.doWhiteBalance(awbFilename)
    """
    return cam
