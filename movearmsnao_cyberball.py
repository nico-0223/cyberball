from naoqi import ALProxy
import time
import math

nao_ip = "169.254.129.162" 
port = 9559

class Nao:
    def __init__(self, nao_ip, port):
        self.ip = nao_ip
        self.port = port
        # Inizializza i proxies per speech, movimento e postura
        self.tts = ALProxy("ALTextToSpeech", self.ip, self.port)
        self.motion = ALProxy("ALMotion", self.ip, self.port)
        self.posture = ALProxy("ALRobotPosture", self.ip, self.port)

nao = Nao(nao_ip, port)

def init_nao():

    nao.tts.say("Hi, my name is Nao! I am a robot")
    time.sleep(2.0)

    nao.posture.goToPosture("Crouch", 0.5)
    print ('Assumo la postura')

    # Per muovere i giunti impostare la stiffness dei giunti a un valore diverso da 0
    nao.motion.setStiffnesses("RArm", 1.0)
    nao.motion.setStiffnesses("LArm", 1.0)

    #Movimento iniziale: nao porta le braccia in posizione iniziale
    names_init = ["RShoulderRoll","LShoulderRoll","RElbowYaw","LElbowYaw","RWristYaw","LWristYaw"]
    angles_init = [math.radians(-20),math.radians(20),math.radians(90),math.radians(-90),math.radians(-90),math.radians(90)]
    fractionMaxSpeed  = 0.1

    nao.motion.setAngles(names_init, angles_init, fractionMaxSpeed)
    nao.motion.openHand("RHand")
    nao.motion.openHand("LHand")

    print("Posizione iniziale")
    time.sleep(1.0)


    # Preparazione
    names  = ["RShoulderPitch","LShoulderPitch","RElbowRoll","LElbowRoll",]
    fractionMaxSpeed  = 0.1
    angles_prep = [math.radians(45),math.radians(45),math.radians(45),math.radians(-45)]

    nao.motion.setAngles(names, angles_prep, fractionMaxSpeed)
    time.sleep(1.0)
    print ("Preparazione")

    names_arms = ["RShoulderRoll","LShoulderRoll"]
    angles_arms = [math.radians(0),math.radians(0)]

    nao.motion.setAngles(names_arms, angles_arms, fractionMaxSpeed)
    fractionMaxSpeed  = 0.1
    print ("Chiudo le braccia")

def pushDX ():

    #names  = ["RShoulderPitch","LShoulderPitch","RElbowRoll","LElbowRoll",]
    names  = ["RShoulderPitch","RElbowRoll"]
    fractionMaxSpeed  = 0.6
    #angles_ready = [math.radians(45),math.radians(45),math.radians(45),math.radians(-45)]
    #angles_push = [math.radians(45),math.radians(45),math.radians(30),math.radians(-30)]
    angles_ready = [math.radians(45),math.radians(40)]
    angles_push = [math.radians(45),math.radians(30)]
    
    #Push
    nao.motion.setAngles(names, angles_push, fractionMaxSpeed)
    time.sleep(0.3)
    #print ("Posizione push")

    #Ritorna a ready
    nao.motion.setAngles(names, angles_ready, fractionMaxSpeed)
    #time.sleep(1.0)
    #print ("Posizione ready")

def pushSX ():

    #names  = ["RShoulderPitch","LShoulderPitch","RElbowRoll","LElbowRoll",]
    names = ["LShoulderPitch","LElbowRoll"]
    fractionMaxSpeed = 0.6
    #angles_ready = [math.radians(45),math.radians(45),math.radians(45),math.radians(-45)]
    #angles_push = [math.radians(45),math.radians(45),math.radians(30),math.radians(-30)]
    angles_ready = [math.radians(45),math.radians(-40)]
    angles_push = [math.radians(45),math.radians(-30)]

    #Push
    nao.motion.setAngles(names, angles_push, fractionMaxSpeed)
    time.sleep(0.3)
    #print ("Posizione push")

    #Ritorna a ready
    nao.motion.setAngles(names, angles_ready, fractionMaxSpeed)
    #time.sleep(1.0)
    #print ("Posizione ready")





#for i in range(10):
#    time.sleep(1.0)
#    pushDX ()
#    time.sleep(1.0)
#    pushSX ()

def end_nao():
    #Posizione finale al termine del gioco
    names_closearms = ["RShoulderRoll","LShoulderRoll"]
    fractionMaxSpeed  = 0.1
    angles_closearms = [math.radians(-20),math.radians(20)]
    nao.motion.setAngles(names_closearms, angles_closearms, fractionMaxSpeed)

    names_end = ["RShoulderPitch","LShoulderPitch","RElbowYaw","LElbowYaw","RWristYaw","LWristYaw"]
    angles_end = [math.radians(80),math.radians(80),math.radians(90),math.radians(-90),math.radians(-90),math.radians(90)]
    
    nao.motion.setAngles(names_end, angles_end, fractionMaxSpeed)

    nao.tts.say("Move completed!")
 


