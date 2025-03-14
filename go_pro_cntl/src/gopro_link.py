#!/usr/bin/env python3

import rospy
from std_msgs.msg import String
import pexpect
import threading

# TO GET THIS WORKING:
# Go to line 133 in gopro_wireless.py - 'enable_wifi: bool = True,'
# Disable it                          - 'enable_wifi: bool = False,'
# No more sudo requirements (hopefully)

class GoproVenvController:
    def __init__(self):
        rospy.init_node('sony_sdk_link_node')

        # Start the virtual environment using pexpect
        self.child = pexpect.spawn('/bin/bash', encoding='utf-8')
        self.child.logfile = open('/tmp/GoproVenv.log', 'w')  # Log to file
        self.child.timeout = None

        # Start a thread to read output
        self.output_thread = threading.Thread(target=self.read_output)
        self.output_thread.daemon = True
        self.output_thread.start()

        self.child.sendline("source /home/reece/Desktop/opengopro_env/bin/activate")
        self.child.sendline("cd /home/reece/Desktop/opengopro_env/bin")
        self.child.sendline("")

        # Subscribe to the topic
        rospy.Subscriber('/gopro_cntl', String, self.command_callback, queue_size=1)

        # Register shutdown hook
        rospy.on_shutdown(self.shutdown)

    def read_output(self):
        while not rospy.is_shutdown():
            try:
                line = self.child.readline()
                
                if line:
                    rospy.loginfo(line.strip())
                    
            except Exception as e:
                rospy.logerr("Error reading output: %s" % e)
                break


    def command_callback(self, msg):
        if msg.data == "start":
            self.child.sendline("python3 gopro-start-rec.py")
            self.child.sendline("")

        elif msg.data == "stop":
            self.child.sendline("python3 gopro-stop-rec.py")
            self.child.sendline("")

        elif msg.data == "sync":
            self.child.sendline("python3 gopro-sync-time.py")
            self.child.sendline("")

    def shutdown(self):
        rospy.loginfo("Shutting down Gopro Venv controller")
        if self.child:
            self.child.terminate()

def main():
    try:
        gopro_venv = GoproVenvController()
        rospy.spin()
    except rospy.ROSInterruptException:
        pass

if __name__ == "__main__":
    main()
