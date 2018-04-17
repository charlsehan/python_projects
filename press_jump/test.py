import numpy as np
import cv2
import imutils
import random
import os
import pickle
import math
import time
from sklearn.linear_model import LinearRegression
from matplotlib import pyplot as plt


def logger(log):
    print(log)


def img_debug(img):
    pass
    #cv2.imshow('img', img)
    #cv2.waitKey(0)


def get_distance():
    DEBUG = False
    # load the image and resize it to a smaller factor so that
    # the shapes can be approximated better
    img = cv2.imread('screencap.png')
    img = imutils.resize(img, width=240)

    # find the man
    man_img = img.copy()
    img_debug(man_img)

    # mask for black man
    man_img = cv2.inRange(man_img, np.array([80, 50, 50]), np.array([125, 70, 85]))
    img_debug(man_img)

    x0 = -1
    y0 = 150

    for line in man_img[y0:y0+100, :]:
        y0 += 1
        white = np.where(line > 0)[0]
        if DEBUG:
            print(white)
        if len(white) == 0:
            continue
        elif x0 == -1:
            x0 = (white[0] + white[-1]) // 2
            if DEBUG:
                print('x0:{}'.format(x0))
            break
    y0 += 40
    x0 += 2

    # find the target
    target_img = img.copy()
    img_debug(target_img)

    # spread the black man mask
    mask = cv2.GaussianBlur(man_img, (13, 13), 0)
    img_debug(mask)

    # carve the mask part off (where the black man is)
    target_img[mask > 0] = 0
    img_debug(target_img)

    # mask for background
    upper = target_img[1, 1]
    lower = target_img[-2, -2]
    if any((upper - lower) > 40):
        lower = target_img[-2, 1]
    if any((upper - lower) > 40):
        lower = target_img[-2, -120]
    mask = cv2.inRange(target_img, lower, upper)

    # set background to black
    target_img[mask > 0] = 0
    img_debug(target_img)

    # background is black, set other part to white
    target_img = cv2.threshold(target_img, 0, 255, cv2.THRESH_BINARY)[1]
    img_debug(target_img)

    x1 = -1
    y1 = 150

    for line in target_img[y1:y1+100, :]:
        y1 += 1
        white = np.where(line > 0)[0]
        if DEBUG:
            print(white)
        if len(white) == 0:
            continue
        elif x1 == -1:
            x1 = (white[0] + white[-1]) // 2
            if DEBUG:
                print('x1:{}'.format(x1))
            break
    y1 += 21

    show_plot = True
    if show_plot:
        plt.close()
        plt.ion()

        plt.subplot(1, 3, 1, facecolor='black')
        plt.axis('off')
        plt.imshow(man_img)

        plt.subplot(1, 3, 2)
        plt.axis('off')
        plt.imshow(target_img)

        plt.subplot(1, 3, 3)
        plt.axis('off')
        cv2.circle(img, (x0, y0), 3, (0, 0, 255), thickness=1)
        cv2.circle(img, (x1, y1), 3, (0, 0, 255), thickness=1)
        plt.imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))

        plt.pause(0.01)

    dis = math.sqrt(abs(x1 - x0) ** 2 + abs(y1 - y0) ** 2)
    return dis

'''
# find contours in the thresholded image and initialize the
# shape detector
cnts = cv2.findContours(thresh.copy(), cv2.RETR_TREE,
                        cv2.CHAIN_APPROX_SIMPLE)
cnts = cnts[0] if imutils.is_cv2() else cnts[1]

for cnt in cnts:
    cv2.drawContours(thresh, [cnt], -1, (255, 0, 0), 2)
    approx = cv2.approxPolyDP(cnt, 0.01 * cv2.arcLength(cnt, True), True)
    print(len(approx))

cv2.imshow('img', thresh)
cv2.waitKey(0)
'''

#cv2.destroyAllWindows()
epsilon = 0.6


def get_action_time(model, distance):
    """
    :return: press time in ms
    """
    t = 0
    logger('epsilon:{}'.format(epsilon))
    if random.random() > epsilon:
        t = model.predict(np.reshape([distance], (-1, 1)))[0]
        t = int(t)
        logger('We got a predict time:{}'.format(t))
    else:
        t = (random.randrange(7) + 3) * 100
        logger('We got a random time:{}'.format(t))
    return t


def take_action(t):
    os.system('adb shell input swipe 100 100 1000 1000 {}'.format(t))


def screencap():
    os.system('adb shell screencap -p /sdcard/screencap.png && adb pull /sdcard/screencap.png')


def is_failed():
    img = cv2.imread('screencap.png')
    img = imutils.resize(img, width=240)
    point = img[340, 160]
    return sum(point) == 255 * 3


def retry():
    #os.system('adb shell input tap 720 2040')
    os.system('adb shell input tap 540 1530')


def train_epoch(model, epoch):
    logger('==============================================')
    logger('Begin train epoch {}'.format(epoch))

    X = []
    Y = []

    screencap()
    if is_failed():
        logger('Fail or not begin, tap to start')
        retry()
        time.sleep(0.5)
        screencap()
    loop = 0
    while loop < 30 or len(X) == 0:
        logger('-------------------------------------------')
        logger('loop: {}'.format(loop))
        loop += 1
        d = get_distance()
        t = get_action_time(model, d)
        logger('distance:{}, time:{}'.format(d, t))
        take_action(t)
        time.sleep(3)

        screencap()
        if is_failed():
            logger('Failed, Retry.')
            retry()
            time.sleep(0.5)
            screencap()
        else:
            X.append(d)
            Y.append(t)
            logger('X length: {}'.format(len(X)))

    model.fit(np.reshape(X, (-1, 1)), np.reshape(Y, (-1, 1)))


def train():
    global epsilon
    model = LinearRegression()
    for i in range(10):
        if i == 0:
            epsilon = 1.
        else:
            if i == 1:
                X = []
                Y = []
                epsilon = 0
            #epsilon -= 0.1
            if epsilon <= 0:
                epsilon = 0
        train_epoch(model, i)

    pickle.dump(model, open('model.pkl', 'wb'))


def test():
    model = pickle.load(open('model6.pkl', 'rb'))
    X = []
    Y = []
    global epsilon
    epsilon = 0
    screencap()
    if is_failed():
        logger('Failed, Retry.')
        retry()
        time.sleep(1)
        screencap()

    while True:
        d = get_distance()
        t = get_action_time(model, d)
        logger('distance:{}, time:{}'.format(d, t))
        take_action(t)
        time.sleep(1)
        screencap()
        if is_failed():
            logger('Failed, Exit.')
            model.fit(np.reshape(X[:-2], (-1, 1)), np.reshape(Y[:-2], (-1, 1)))
            pickle.dump(model, open('model7.pkl', 'wb'))
            break
            #logger('Failed, Retry.')
            #retry()
            #time.sleep(0.5)
            #screencap()
        else:
            X.append(d)
            Y.append(t)
            logger('X length: {}'.format(len(X)))


test()
