#!/usr/bin/env python

import rospy
import tf
from sensor_msgs.msg import Imu
from std_msgs.msg import Float64
from geometry_msgs.msg import Quaternion, Vector3

class IMU:
    def __init__(self):
        rospy.init_node('navX_source')
        self.imu_pub = rospy.Publisher('imu_data', Imu, queue_size=50)

        self.yaw = 0.0      #Z-axis
        self.pitch = 0.0    #X-axis
        self.roll = 0.0     #Y-axis
        self.line_acc_x = 0.0
        self.line_acc_y = 0.0
        self.line_acc_z = 0.0
        self.quat_w = 0.0
        self.quat_x = 0.0
        self.quat_y = 0.0
        self.quat_z = 0.0

    def yaw_callback(self,msg):
        self.yaw = msg.data
    
    def pitch_callback(self,msg):
        self.pitch = msg.data
    
    def roll_callback(self,msg):
        self.roll = msg.data
    
    def acc_x_callback(self,msg):
        self.line_acc_x = msg
    
    def acc_y_callback(self,msg):
        self.line_acc_y = msg
    
    def acc_z_callback(self,msg):
        self.line_acc_z = msg

    def qw_callback(self,msg):
        self.quat_w = msg

    def qx_callback(self,msg):
        self.quat_x = msg
    
    def qy_callback(self,msg):
        self.quat_y = msg
    
    def qz_callback(self,msg):
        self.quat_z = msg
    

    def main(self):
        yaw_sub = rospy.Subscriber('yaw_data', Float64, self.yaw_callback)
        pitch_sub = rospy.Subscriber('pitch_data', Float64, self.pitch_callback)
        roll_sub = rospy.Subscriber('roll_data', Float64, self.roll_callback)
        acc_x_sub = rospy.Subscriber('acceleration_x_data', Float64, self.acc_x_callback)
        acc_y_sub = rospy.Subscriber('acceleration_y_data', Float64, self.acc_y_callback)
        acc_z_sub = rospy.Subscriber('acceleration_z_data', Float64, self.acc_z_callback)
        quat_w_sub = rospy.Subscriber('quaternion_w_data', Float64, self.qw_callback)
        quat_x_sub = rospy.Subscriber('quaternion_x_data', Float64, self.qx_callback)
        quat_y_sub = rospy.Subscriber('quaternion_y_data', Float64, self.qy_callback)
        quat_z_sub = rospy.Subscriber('quaternion_z_data', Float64, self.qz_callback)
        
        #variables for angular velocity math
        #need to get to rad/sec
        prev_yaw = self.yaw
        prev_pitch = self.pitch
        prev_roll = self.roll

        hz_rate = 15.0 #number of times the program runs in a second
        r = rospy.Rate(hz_rate)


        while not rospy.is_shutdown():
            current_time = rospy.Time.now()

            yaw_now = self.yaw
            pitch_now = self.pitch
            roll_now = self.roll

            vyaw = (yaw_now-prev_yaw)*hz_rate
            vpitch = (pitch_now-prev_pitch)*hz_rate
            vroll = (roll_now-prev_roll)*hz_rate

            #Setting all the data for the publisher
            imu_data = Imu()
            imu_data.header.stamp = current_time
            imu_data.header.frame_id = 'imu_odom'
            #orientation - given by navX
            q_avg = tf.transformations.quaternion_from_euler(0.0, 0.0, yaw_now);
            imu_msg = Imu()
            imu_msg.orientation.w = q_avg[3]
            imu_msg.orientation.x = q_avg[0]
            imu_msg.orientation.y = q_avg[1]
            imu_msg.orientation.z = q_avg[2]
            
            imu_data.orientation_covariance = [.0001, 0, 0, #3x3 matrix
                                               0, .0001, 0,
                                               0, 0, .0001]
            #angular velocity - calculated
            imu_data.angular_velocity.x = vpitch
            imu_data.angular_velocity.y = vroll
            imu_data.angular_velocity.z = vyaw

            imu_data.angular_velocity_covariance = [.0001, 0, 0, #3x3 matrix
                                                    0, .0001, 0,
                                                    0, 0, .0001]

            #linear acceleration - given by nzvX
            imu_data.linear_acceleration = Vector3(acc_x_sub,acc_y_sub,acc_z_sub)#vector for linear accel.
            imu_data.linear_acceleration_covariance = [.0001, 0, 0, #3x3 matrix
                                                       0, .0001, 0,
                                                       0, 0, .0001]


            #publish message
            self.imu_pub.publish(imu_data)

            prev_pitch = pitch_now
            prev_roll = roll_now
            prev_yaw = yaw_now

            r.sleep()

navX_source = IMU()
navX_source.main()