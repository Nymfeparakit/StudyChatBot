import cv2
import numpy
from imutils.contours import sort_contours
from tensorflow.keras.models import load_model
import numpy as np
import imutils
import tensorflow as tf
from tensorflow.compat.v1 import InteractiveSession


def find(contours, count):
	d = {}
	for cnt in contours:
		x, y, w, h = cv2.boundingRect(cnt)
		d[w * h] = cnt
	list_d = list(d.items())
	list_d.sort(key=lambda i: i[0])
	new_cnts = []
	for i in range(len(list_d) - count, len(list_d)):
		new_cnts.append(list_d[i][1])
	return new_cnts


def blob(image):
	(tH, tW) = image.shape
	if tW > tH:
		thresh = imutils.resize(image, width=32)
	else:
		thresh = imutils.resize(image, height=32)
	padded = cv2.copyMakeBorder(image, top=12, bottom=12,
								left=16, right=16, borderType=cv2.BORDER_CONSTANT,
								value=(0, 0, 0))
	padded = cv2.resize(padded, (32, 32), cv2.INTER_CUBIC)
	padded = padded.astype("float32") / 255.0
	padded = np.expand_dims(padded, axis=-1)
	return padded


def getContours(img, count):
	img = cv2.medianBlur(img, 9)
	thresh = cv2.adaptiveThreshold(img, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, \
								   cv2.THRESH_BINARY, 11, 2)
	edged = cv2.Canny(thresh, 80, 150)

	cnts = cv2.findContours(edged.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[0]
	new_cnts = []
	for c in cnts:
		x, y, w, h = cv2.boundingRect(c)
		if (w >= 5 and w <= 150) and (h >= 15 and h <= 200):
			new_cnts.append(c)
	cnts = new_cnts
	cnts = find(cnts, count)
	return cnts


def getChars(image, cnts):
	image = cv2.threshold(image, 150, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]
	chars = []
	for cnt in cnts:
		x, y, w, h = cv2.boundingRect(cnt)
		char = image[y:y + h, x:x + w]
		char = blob(char)
		chars.append(char)
	return chars


def getLabels(model, chars, cnts, labelNames):
	chars = np.array([c for c in chars], dtype="float32")
	preds = model.predict([chars])
	answers = {}
	for i in range(len(cnts)):
		cnt = cnts[i]
		pred = preds[i]
		x, y, w, h = cv2.boundingRect(cnt)
		i = np.argmax(pred)
		prob = pred[i]
		label = labelNames[i]
		answers[y] = label
	sorted_ans = sorted(answers.items())
	labels = []
	for k, v in sorted_ans:
		print(k, " ", v)
		labels.append(v)
	return labels


def detection(image_path, count):
	#image - путь к изображению
	#count - количество символов, включая id + ответы на сам тест
	###tf config###
	config = tf.ConfigProto()
	config.gpu_options.allow_growth = True
	session = InteractiveSession(config=config)
	##model and labels###
	model = load_model("model/handwriting.model")
	labelNames = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"
	labelNames = [l for l in labelNames]

	img = cv2.imread(image_path, 0)
	img = cv2.resize(img, (480, 640), cv2.INTER_CUBIC)

	copy = img.copy()

	cnts = getContours(img, count)
	chars = getChars(copy, cnts)

	labels = getLabels(model, chars, cnts, labelNames)
	return labels
