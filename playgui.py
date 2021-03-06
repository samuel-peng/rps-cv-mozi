# playgui.py
# Source: https://github.com/DrGFreeman/rps-cv
# This file is the main program to run to play the Rock-Paper-Scissors game
# with the pygame graphical user interface (GUI).

import pickle
import random
import sys
import time

import pygame as pg
import pygame.locals

import numpy as np
import cv2

import rpsutil as rps
import rpsimgproc as imp
import rpsgui

def saveImage(img, gesture, notify=False):

    # Define image path and filename
    folder = rps.imgPathsRaw[gesture]
    name = rps.gestureTxt[gesture] + '-' + time.strftime('%Y%m%d-%H%M%S')
    extension = '.png'

    if notify:
        print('Saving {}'.format(folder + name + extension))

    # Save image
    cv2.imwrite(folder + name + extension, img)

if __name__ == '__main__':
    """Launches the Rock-Paper-Scissors game with a graphical interface
    Command line arguments:
        privacy: will display the privacy notice at beginning of game
        loop: will launch a new game once current game is over."""

    try:
        # Initialize game mode variables
        privacy = False
        loop = False

        # Read command line arguments
        argv = sys.argv
        argv.pop(0)

        if len(sys.argv) > 0:
            for arg in argv:
                if arg == 'privacy':
                    privacy = True
                elif arg == 'loop':
                    loop = True
                else:
                    print('{} is not a recognized argument'.format(arg))

        # Load classifier from pickle file
        filename = 'clf.pkl'
        with open(filename, 'rb') as f:
            clf = pickle.load(f)

        # Create camera object with pre-defined settings
        cam = rps.cameraSetup()

        # Initialize last gesture value
        lastGesture = -1

        # Define score at which game ends
        endScore = 5

        # Initialize GUI
        gui = rpsgui.RPSGUI(privacy=privacy, loop=loop)

        # Load static images for computer gestures
        coImgs = {}
        img = cv2.imread('img/gui/rock.png', cv2.IMREAD_COLOR)
        coImgs[rps.ROCK] = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        img = cv2.imread('img/gui/paper.png', cv2.IMREAD_COLOR)
        coImgs[rps.PAPER] = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        img = cv2.imread('img/gui/scissors.png',
                         cv2.IMREAD_COLOR)
        coImgs[rps.SCISSORS] = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

        # Load green image
        greenImg = cv2.imread('img/gui/green.png', cv2.IMREAD_COLOR)
        greenImg = cv2.cvtColor(greenImg, cv2.COLOR_BGR2RGB)

        calibrate = 0
        while True:

            # Get image from camera
            img = imp.crop(cam.getOpenCVImage())

            # Convert image to RGB (from BGR)
            imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

            # Set player image to imgRGB
            gui.setPlImg(imgRGB)

            # Get grayscale image
            gray = imp.getGray(imgRGB, threshold=17)

            # Count non-background pixels
            nonZero = np.count_nonzero(gray)
            #print(nonZero)

            # Define waiting time
            waitTime = 0

            # Parameters for saving new images
            gesture = None
            notify = False

            #time.sleep(2)
            # Check if player hand is present
            if nonZero > 32000:
                if calibrate > 10:
                    # Predict gesture
                    predGesture = clf.predict([gray])[0]

                    if predGesture == lastGesture:
                        successive += 1
                    else:
                        successive = 0

                    if successive == 2:
                        print('Player: {}'.format(rps.gestureTxt[predGesture]))
                        waitTime = 3000
                        gesture = predGesture

                        # Computer gesture
                        computerGesture = random.randint(0,2)
                        print('Computer: {}'.format(rps.gestureTxt[computerGesture]))

                        # Set computer image to computer gesture
                        gui.setCoImg(coImgs[computerGesture])

                        diff = computerGesture - predGesture
                        if diff in [-2, 1]:
                            print('Computer wins!')
                            gui.setWinner('computer')
                        elif diff in [-1, 2]:
                            print('Player wins!')
                            gui.setWinner('player')
                        else:
                            print('Tie')
                            gui.setWinner('tie')
                        print('Score: player {}, computer {}\n'.format(gui.plScore,
                                                                 gui.coScore))

                    lastGesture = predGesture

                else:
                    calibrate = calibrate + 1
            else:

                lastGesture = -1

                # Set computer image to green
                gui.setCoImg(greenImg)
                gui.setWinner()

            # Draw GUI
            gui.draw()

            # Flip pygame display
            pg.display.flip()

            # Wait
            pg.time.wait(waitTime)

            if gesture is not None:
                # Save new image
                saveImage(img, gesture, notify)

            # Check pygame events
            for event in pg.event.get():
                if event.type == pg.locals.QUIT:
                    gui.quit()

            # Check if scores reach endScore (end of game)
            if gui.plScore == endScore or gui.coScore == endScore:
                if gui.coScore > gui.plScore:
                    print('Game over, computer wins...\n')
                else:
                    print('Game over, player wins!!!\n')
                gui.gameOver()


    finally:
        f.close()
        cam.close()
