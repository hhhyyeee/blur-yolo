import numpy as np
import math
import cv2
import os
import json
#from scipy.special import expit
#from utils.box import BoundBox, box_iou, prob_compare
#from utils.box import prob_compare2, box_intersection
from ...utils.box import BoundBox
from ...cython_utils.cy_yolo2_findboxes import box_constructor

def expit(x):
	return 1. / (1. + np.exp(-x))

def _softmax(x):
    e_x = np.exp(x - np.max(x))
    out = e_x / e_x.sum()
    return out

def findboxes(self, net_out):
	# meta
	meta = self.meta
	boxes = list()
	boxes=box_constructor(meta,net_out)
	return boxes

def postprocess(self, net_out, im, save = True):
	"""
	Takes net output, draw net_out, save to disk
	"""
	boxes = self.findboxes(net_out)

	print('********************')

	# meta
	meta = self.meta
	threshold = meta['thresh']
	colors = meta['colors']
	labels = meta['labels']
	if type(im) is not np.ndarray:
		imgcv = cv2.imread(im)
		imgcv_blur = cv2.imread(im)
	else:
		imgcv = im
		imgcv_blur = im
	h, w, _ = imgcv.shape
	
	resultsForJSON = []
	resultsForBlur = []
	maxBlur = 0
	for b in boxes:
		boxResults = self.process_box(b, h, w, threshold)
		if boxResults is None:
			continue
		left, right, top, bot, mess, max_indx, confidence = boxResults
		thick = int((h + w) // 300)
		if self.FLAGS.json:
			resultsForJSON.append({"label": mess, "confidence": float('%.2f' % confidence), "topleft": {"x": left, "y": top}, "bottomright": {"x": right, "y": bot}})
			continue

		# 블러 처리
		print('mess:', mess, ', confidence:', float('%.2f' % confidence))
		if confidence > maxBlur:
			maxBlur = confidence
			resultsForBlur = [mess, confidence, left, top, right, bot]

		cv2.rectangle(imgcv,
			(left, top), (right, bot),
			colors[max_indx], thick)
		cv2.putText(imgcv, mess, (left, top - 12),
			0, 1e-3 * h, colors[max_indx],thick//3)

	if not save: return imgcv

	outfolder = os.path.join(self.FLAGS.imgdir, 'out')
	img_name = os.path.join(outfolder, os.path.basename(im))
	if self.FLAGS.json:
		textJSON = json.dumps(resultsForJSON)
		textFile = os.path.splitext(img_name)[0] + ".json"
		with open(textFile, 'w') as f:
			f.write(textJSON)
		return		
	
	cv2.imwrite(img_name, imgcv)

	# 블러 처리
	print('max confidence result:', resultsForBlur)
	blurred_img = cv2.GaussianBlur(imgcv_blur, (21, 21), 0)

	mask = np.zeros((h, w, 3), dtype=np.uint8)
	mask = cv2.rectangle(mask, (resultsForBlur[2], resultsForBlur[3]), (resultsForBlur[4], resultsForBlur[5]), (255, 255, 255), -1)
	out = np.where(mask==(255, 255, 255), imgcv_blur, blurred_img)

	blurfolder = os.path.join(self.FLAGS.imgdir, 'blur')
	blurred_img_name = os.path.join(blurfolder, os.path.basename(im))
	cv2.imwrite(blurred_img_name, out)
