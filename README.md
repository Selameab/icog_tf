# icog_tf
ROS Package for TF

Run
---
```sh
rosrun icog_tf user_bundler.py    #For bundling users
rosrun icog_tf tf_bundler.py      #For bundling each user's transforms
```

ROS Nodes
---------
#### /user_bundler

###### Publications: 
 * /users_bundle [icog_tf/users]
 
###### Subscriptions: 
 * /tf [tf2_msgs/TFMessage]
 
#### /tf_bundler

###### Publications: 
 * /tf_bundles [icog_tf/tfBundles]
 
###### Subscriptions: 
 * /tf [tf2_msgs/TFMessage]
 
 