
from naoqi import ALProxy
IP = "172.20.10.14"
Port = 9559
motion = ALProxy("ALMotion", IP ,Port)
motion.rest()