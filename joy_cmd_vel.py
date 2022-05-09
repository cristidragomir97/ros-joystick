
import rospy, subprocess

from sensor_msgs.msg import Joy, JointState
from geometry_msgs.msg import Twist
from trajectory_msgs.msg import JointTrajectory, JointTrajectoryPoint


SOURCE_ROOT = ". /opt/ros/noetic/setup.sh"
SOURCE_WS = ". /root/catkin_ws/devel/setup.sh"
COMMAND = "rosrun joy joy_node"
JOY_NODE = "{} {} {}".format(SOURCE_ROOT, SOURCE_WS, COMMAND)

class JoyToCommands(object):
    def __init__(self):        
        self.twist_pub = rospy.Publisher('/cmd_vel', Twist, queue_size=1)        
        rospy.Subscriber("/joy", Joy, callback=self.joy_cb, queue_size=1)        
        self.linear_vel_multiplier = 0.5        
        self.angular_vel_multiplier = 0.3

    def joy_cb(self, joy_msg):
        rospy.logdebug_throttle(0.5, "received joy message: {}".format(joy_msg))
        twist_cmd = Twist()        
        twist_cmd.linear.x = self.linear_vel_multiplier * joy_msg.axes[3]        
        twist_cmd.linear.y = self.linear_vel_multiplier * joy_msg.axes[2]        
        twist_cmd.linear.z = self.linear_vel_multiplier * joy_msg.axes[1]        
        twist_cmd.angular.z = self.angular_vel_multiplier * joy_msg.axes[0]
        self.twist_pub.publish(twist_cmd)


if __name__ == '__main__':    
    subprocess.call(JOY_NODE, shell=True)
    rospy.init_node("joy2commands", log_level=rospy.INFO)    
    JoyToCommands()    
    rospy.spin()
