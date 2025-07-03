#!/usr/bin/env python3
import rospy
import socket
from nav_msgs.msg import Odometry
from geometry_msgs.msg import Quaternion, Point, Pose, PoseWithCovariance, Twist, TwistWithCovariance

def main():
    rospy.init_node('vio_udp_receiver', anonymous=True)
    pub = rospy.Publisher('/vio/odometry', Odometry, queue_size=10)

    udp_ip = '0.0.0.0'
    udp_port = 9000

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((udp_ip, udp_port))

    rospy.loginfo(f"Listening for VIO data on {udp_ip}:{udp_port}")

    # Publishing frequency
    rate = rospy.Rate(100)  # 100 Hz

    while not rospy.is_shutdown():
        data, _ = sock.recvfrom(1024)  # Buffer size is 1024 bytes
        try:
            parts = [float(x.strip()) for x in data.decode('utf-8').split(',')]
            # print(f"Received data: {parts}")
            if len(parts) != 7:
                rospy.logwarn("Received data does not have 7 parts, skipping...")
                continue
            px, py, pz, qx, qy, qz, qw = parts
            odom = Odometry()
            odom.header.stamp = rospy.Time.now()
            odom.header.frame_id = 'map'
            odom.pose.pose.position = Point(px, py, pz)
            odom.pose.pose.orientation = Quaternion(qx, qy, qz, qw)
            rospy.loginfo(f"Received VIO data: {odom.pose.pose}")
            pub.publish(odom)
            rate.sleep()
        except ValueError as e:
            rospy.logwarn(f"Invalid data: {e}")
            continue

if __name__ == '__main__':
    main()                                                                                                                               