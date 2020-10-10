import cv2
from ocr import detection

if __name__ == '__main__':
	print(detection(r"test_images/user_photo.jpg",6))