#! /usr/bin/env python

import rospy
from std_msgs.msg import Float32, Float64
import threading
from networktables import NetworkTables

# Creates proxy node
rospy.init_node('robot_proxy')

cond = threading.Condition()
notified = [False]

# Checks if connected to networktables
def connectionListener(connected, info):
    print(info, '; Connected=%s' % connected)
    with cond:
        notified[0] = True
        cond.notify()

NetworkTables.initialize(server='10.06.24.2')
NetworkTables.addConnectionListener(connectionListener, immediateNotify=True)

with cond:
    print("Waiting")
    if not notified[0]:
        cond.wait()


class Proxy:

    def __init__(self):
        # Runs code below if connected to the server
        print("Connected!")
        self.table = NetworkTables.getTable('SmartDashboard')

        # Creates ROS publishers of data
        self.l_enc_pub = rospy.Publisher('/l_enc_data', Float32, queue_size=1)
        self.r_enc_pub = rospy.Publisher('/r_enc_data', Float32, queue_size=1)
        self.angle_pub = rospy.Publisher('/angle', Float64, queue_size=1)
        self.yaw_data_pub = rospy.Publisher('/yaw_data', Float64, queue_size=1)
        self.pitch_data_pub = rospy.Publisher('/pitch_data', Float64, queue_size=1)
        self.roll_data_pub = rospy.Publisher('/roll_data', Float64, queue_size=1)
        self.acceleration_x_data_pub = rospy.Publisher('/acceleration_x_data', Float64, queue_size=1)
        self.acceleration_y_data_pub = rospy.Publisher('/acceleration_y_data', Float64, queue_size=1)
        self.acceleration_z_data_pub = rospy.Publisher('/acceleration_z_data', Float64, queue_size=1)
        self.quaternion_w_data_pub = rospy.Publisher('/quaternion_w_data', Float64, queue_size=1)
        self.quaternion_x_data_pub = rospy.Publisher('/quaternion_x_data', Float64, queue_size=1)
        self.quaternion_y_data_pub = rospy.Publisher('/quaternion_y_data', Float64, queue_size=1)
        self.quaternion_z_data_pub = rospy.Publisher('/quaternion_z_data', Float64, queue_size=1)

        # Declare data types
        self.l_values = Float32()
        self.r_values = Float32()
        self.angle_values = Float64()
        self.yaw_values = Float64()
        self.pitch_values = Float64()
        self.roll_values = Float64()
        self.acceleration_x_values = Float64()
        self.acceleration_y_values = Float64()
        self.acceleration_z_values = Float64()
        self.quaternion_w_values = Float64()
        self.quaternion_x_values = Float64()
        self.quaternion_y_values = Float64()
        self.quaternion_z_values = Float64()
        

        self.left_vel = 0
        self.right_vel = 0

    def left_callback(self,msg): 
        self.left_vel = msg.data

    def right_callback(self,msg): 
        self.right_vel = msg.data

    def main(self):

        left_vel_sub = rospy.Subscriber('l_wheel_vel', Float32, self.left_callback)
        right_vel_sub = rospy.Subscriber('r_wheel_vel', Float32, self.right_callback)

        # Set how many times this should run per second
        r = rospy.Rate(15.0)

        while not rospy.is_shutdown():
            current_time = rospy.Time.now()

            # Get encoder and imu data from networktables
            self.l_values.data = self.table.getNumber('l_enc_data',1)
            self.r_values.data = self.table.getNumber('r_enc_data',1)
            self.angle_values.data = self.table.getNumber("angle",1)
            self.yaw_values.data = self.table.getNumber("yaw_data",1)
            self.pitch_values.data = self.table.getNumber("pitch_data",1)
            self.roll_values.data = self.table.getNumber("roll_data",1)
            self.acceleration_x_values.data = self.table.getNumber("acceleration_x_data",1)
            self.acceleration_y_values.data = self.table.getNumber("acceleration_y_data",1)
            self.acceleration_z_values.data = self.table.getNumber("acceleration_z_data",1)
            self.quaternion_w_values.data = self.table.getNumber("quaternion_w_data",1)
            self.quaternion_x_values.data = self.table.getNumber("quaternion_x_data",1)
            self.quaternion_y_values.data = self.table.getNumber("quaternion_y_data",1)
            self.quaternion_z_values.data = self.table.getNumber("quaternion_z_data",1)



            # Publish encoder and imu data to ROS
            self.l_enc_pub.publish(self.l_values)
            self.r_enc_pub.publish(self.r_values)
            self.angle_pub.publish(self.angle_values)
            self.yaw_data_pub.publish(self.yaw_values)
            self.pitch_data_pub.publish(self.pitch_values)
            self.roll_data_pub.publish(self.roll_values)
            self.acceleration_x_data_pub.publish(self.acceleration_x_values)
            self.acceleration_y_data_pub.publish(self.acceleration_y_values)
            self.acceleration_z_data_pub.publish(self.acceleration_z_values)
            self.quaternion_w_data_pub.publish(self.quaternion_w_values)
            self.quaternion_x_data_pub.publish(self.quaternion_x_values)
            self.quaternion_y_data_pub.publish(self.quaternion_y_values)
            self.quaternion_z_data_pub.publish(self.quaternion_z_values)

            # Sends right and left wheel velocities through networktables
            self.table.putNumber('l_wheel_vel',self.left_vel)
            self.table.putNumber('r_wheel_vel',self.right_vel)

            # Sleeps to meet specified rate
            r.sleep()

proxy_node = Proxy()
proxy_node.main()
    

