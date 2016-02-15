#!/usr/bin/env python
import rospy
from tf2_msgs.msg import TFMessage
from icog_tf.msg import tfBundle
from icog_tf.msg import tfBundles

from pi_face_tracker.srv import *
from pi_face_tracker.msg import Faces
from pi_face_tracker.msg import Face
from pi_face_tracker.msg import FaceEvent

import re


# Returns the item in list1 and not in list2
def findDiff(list1, list2):
    for item in list1:
        if item not in list2:
            return item
    return None

def callback(data):
	global previous_faces
	current_faces = {};
	for user in data.tf_bundles:
		user_id = int(re.sub("user_","",user.user_id))	
		location = user.head.translation
		current_faces[user_id] = location
	
	new_face = findDiff(list(current_faces.keys()), list(previous_faces.keys()))
	lost_face = findDiff(list(previous_faces.keys()), list(current_faces.keys()))

	# Publishers 
	# if new face is found
	if (new_face):
		face_event_msg = FaceEvent()
		face_event_msg.face_event = "new_face"
		face_event_msg.face_id = new_face
		event_publisher.publish(face_event_msg)
	# if face is lost
	if (lost_face):
		face_event_msg = FaceEvent()
		face_event_msg.face_event = "lost_face"
		face_event_msg.face_id = lost_face
		event_publisher.publish(face_event_msg)

	# Face Location
	faces_msg = Faces()
	faces_msg.faces = []
	for user, location in current_faces.items():
		face_msg = Face()
		face_msg.id = user
		face_msg.point = location
		face_msg.attention = 1
		faces_msg.faces.append(face_msg)

	face_publisher.publish(faces_msg)

	previous_faces = current_faces

previous_faces = {};
event_publisher = rospy.Publisher('/camera/face_event', FaceEvent, queue_size=10)
face_publisher = rospy.Publisher('/camera/face_location', Faces, queue_size=10)

if __name__ == '__main__':
	rospy.init_node('head_tracker', anonymous=False)   
	rospy.Subscriber("/tf_bundles", tfBundles, callback)
	rospy.spin()