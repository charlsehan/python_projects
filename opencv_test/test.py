import cv2
import imutils
import numpy as np


def img_debug(img):
    pass
    img = imutils.resize(img, width=360)
    cv2.imshow('img', img)
    cv2.waitKey(0)


img = cv2.imread('screencap.png')
img_debug(img)

gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
img_debug(gray)


#kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
#dilated = cv2.dilate(img, kernel)
#img_debug(dilated)

#kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))
#closed = cv2.morphologyEx(img, cv2.MORPH_CLOSE, kernel)
#img_debug(closed)

MIN_BLOCK_SIZE = 30
MIN_GAP_SIZE = 30

class Rect:
    def __init__(self, x, y, w, h):
        self.x = x
        self.y = y
        self.w = w
        self.h = h


def get_row_rects(source):
    rects = []
    in_block = False
    start = 0
    for i, line in enumerate(source):
        is_blank = all(v == line[0] for v in line)
        #mode = np.argmax(np.bincount(line))
        #is_blank = sum(line == mode) > len(line) * 0.9
        if not in_block and not is_blank:
            in_block = True
            start = i
        elif in_block and is_blank:
            in_block = False
            if i - start >= MIN_BLOCK_SIZE:
                rects.append(Rect(0, start, len(line), i - start))
    return rects


def get_block_rects(row_source, row_top):
    rects = []
    in_block = False
    start = 0
    for i in range(row_source.shape[1]):
        col = row_source[:, i]
        is_blank = all(v == col[0] for v in col)
        #mode = np.argmax(np.bincount(col))
        #is_blank = sum(col == mode) > len(col) * 0.9
        if not in_block and not is_blank:
            in_block = True
            start = i
        elif in_block and is_blank:
            in_block = False

            if len(rects) > 0:
                last = rects[-1]
                if start - last.x - last.w < MIN_GAP_SIZE:
                    last.w = i - last.x
                else:
                    if i - start >= MIN_BLOCK_SIZE:
                        rects.append(Rect(start, row_top, i - start, len(row_source)))
            else:
                if i - start >= MIN_BLOCK_SIZE:
                    rects.append(Rect(start, row_top, i - start, len(row_source)))
    return rects


rows = get_row_rects(gray)
items = []
for row in rows:
    row_img = gray[row.y:row.y + row.h]
    rects = get_block_rects(row_img, row.y)
    items += rects

for rect in items:
    cv2.rectangle(img, (rect.x, rect.y), (rect.x + rect.w, rect.y + rect.h), (0, 0, 255), 3)


img_debug(img)