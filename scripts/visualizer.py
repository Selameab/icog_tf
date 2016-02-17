#!/usr/bin/env python
import rospy
from tf2_msgs.msg import TFMessage
from icog_tf.msg import tfBundle
from icog_tf.msg import tfBundles

from pyqtgraph.Qt import QtCore, QtGui
import pyqtgraph as pg
import pyqtgraph.opengl as gl
import numpy as np

import thread

def drawLine (pt1, pt2):
    global view
    pts = np.array([pt1, pt2])
    plt = gl.GLLinePlotItem(pos=pts, width=2, antialias=True)
    view.addItem(plt)

def translation_to_3Dpt(translation):
	return [translation.x, translation.y, translation.z]

def drawUser(user):
	head = translation_to_3Dpt(user.head.translation)
	neck = translation_to_3Dpt(user.neck.translation)
	torso = translation_to_3Dpt(user.torso.translation)

	right_shoulder = translation_to_3Dpt(user.right_shoulder.translation)
	right_elbow = translation_to_3Dpt(user.right_elbow.translation)
	right_hand = translation_to_3Dpt(user.right_hand.translation)

	left_shoulder = translation_to_3Dpt(user.left_shoulder.translation)
	left_elbow = translation_to_3Dpt(user.left_elbow.translation)
	left_hand = translation_to_3Dpt(user.left_hand.translation)
	
	drawLine(head, neck)
	drawLine(neck, torso)

	drawLine(neck, right_shoulder)
	drawLine(right_shoulder, right_elbow)
	drawLine(right_elbow, right_hand)

	drawLine(neck, left_shoulder)
	drawLine(left_shoulder, left_elbow)
	drawLine(left_elbow, left_hand)

def callback(data):
	for user in data.tf_bundles:
		drawUser(user)


if __name__ == '__main__':
	# PyQt Init
	pg.mkQApp()
	view = gl.GLViewWidget()
	view.show()
	view.orbit(-135,90)

	

	# ROS Initialization
	rospy.init_node('visualizer', anonymous=False)   
	rospy.Subscriber("/tf_bundles", tfBundles, callback)
	thread.start_new_thread(rospy.spin, ())
	QtGui.QApplication.instance().exec_()