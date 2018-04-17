import numpy as np
import cv2
import imutils
import random
import os
import pickle
import math
import time
from matplotlib import pyplot as plt


learning = True
epsilon = 1.
alpha = 0.5
valid_actions = [300, 400, 500, 600, 700, 800, 900]
Q = {}


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
    y1 += 22

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
    return int((dis + 1.5)//3)*3


def is_failed():
    img = cv2.imread('screencap.png')
    img = imutils.resize(img, width=240)
    point = img[340, 160]
    return sum(point) == 255 * 3


def retry():
    #os.system('adb shell input tap 720 2040')
    os.system('adb shell input tap 540 1530')


def take_action(action):
    os.system('adb shell input swipe 100 100 1000 1000 {}'.format(action))


def screencap():
    os.system('adb shell screencap -p /sdcard/screencap.png && adb pull /sdcard/screencap.png')


def get_maxQ(state):
    maxQ = max(Q[state].values())
    return maxQ


def get_maxQ_action(state):
    listA = []
    mxQ = get_maxQ(state)
    logger('| state:{}, mxQ:{}'.format(state, mxQ))
    for a in valid_actions:
        logger('  | action:{}, value:{}'.format(a, Q[state][a]))
        if Q[state][a] == mxQ:
            listA.append(a)
    if len(listA) == 1:
        return listA[0]
    return listA[random.randrange(len(listA))]


def createQ(state):
    if learning and state not in Q:
        Q[state] = {a: 0.0 for a in valid_actions}
    return


def choose_action(state):
    """
    :return: press time in ms
    """
    if not learning or random.random() > epsilon:
        action = get_maxQ_action(state)
        logger('<<<< Q time: {}'.format(action))
    else:
        action = random.choice(valid_actions)
        logger('<<<< Random time: {}'.format(action))
    return action


def learn(state, action, reward):
    """ The learn function is called after the agent completes an action and
        receives an award. This function does not consider future rewards
        when conducting learning. """

    ###########
    ## TO DO ##
    ###########
    # When learning, implement the value iteration update rule
    #   Use only the learning rate 'alpha' (do not use the discount factor 'gamma')
    if learning:
        Q[state][action] += alpha * (reward - Q[state][action])

    return


def act(action):
    take_action(action)
    time.sleep(3)
    screencap()
    if is_failed():
        logger('Failed, Retry, reward -1')
        retry()
        time.sleep(0.5)
        screencap()
        reward = -1
    else:
        logger('Success, reward +1')
        reward = 1
    return reward


def update():
    """ The update function is called when a time step is completed in the
        environment for a given trial. This function will build the agent
        state, choose an action, receive a reward, and learn if enabled. """

    state = int(get_distance())              # Get current state
    logger('>>>> state (distance) {}'.format(state))
    createQ(state)                 # Create 'state' in Q-table
    action = choose_action(state)  # Choose an action
    reward = act(action) # Receive a reward
    learn(state, action, reward)   # Q-learn

    return


def printQ():
    print("/-----------------------------------------")
    print("| State-action rewards from Q-Learning    ")
    print("\-----------------------------------------")

    for state in sorted(Q.keys()):
        print("{}".format(state))
        for action in sorted(Q[state].keys()):
            print(" -- {} : {:.3f}".format(action, Q[state][action]))


def train_epoch(epoch):
    logger('==============================================')
    logger('Begin train epoch {}'.format(epoch))
    logger('epsilon: {}'.format(epsilon))
    screencap()
    if is_failed():
        logger('Fail or not begin, tap to start')
        retry()
        time.sleep(0.5)
        screencap()

    for i in range(10):
        logger('---------------------------------------------')
        logger('step {}'.format(i))
        update()

    printQ()


def train():
    global learning, epsilon
    for i in range(101):
        if not learning:
            epsilon = 0
        else:
            epsilon = math.e ** (-0.02315 * i)
            if epsilon < 0.1:
                logger('epsilon less then 0.1, stop training')
                break
        train_epoch(i)

    pickle.dump(Q, open('Q.pkl', 'wb'))


def test():
    global Q, learning
    learning = False
    Q = pickle.load(open('Q.pkl', 'rb'))
    printQ()
    screencap()
    if is_failed():
        logger('Fail or not begin, tap to start')
        retry()
        time.sleep(0.5)
        screencap()

    while True:
        state = int(get_distance())    # Get current state
        logger('>>>> state (distance) {}'.format(state))
        action = choose_action(state)  # Choose an action
        take_action(action)
        time.sleep(2)
        screencap()
        if is_failed():
            logger('Failed, Exit.')
            break
            #logger('Failed, Retry.')
            #retry()
            #time.sleep(0.5)
            #screencap()


test()

'''
get_distance()
'''

