from os.path import dirname

from adapt.intent import IntentBuilder
from mycroft.skills.core import MycroftSkill
from mycroft.util.log import getLogger

from urllib2 import urlopen
import paho.mqtt.client as mqtt

__author__ = 'jamiehoward430/bkmar1192'

LOGGER = getLogger(__name__)

class mymqttskill(MycroftSkill):

    def __init__(self):
        super(mymqttskill, self).__init__(name="mymqttskill")
       
        self.protocol = self.config["protocol"]
	self.mqttssl = self.config["mqtt-ssl"]
	self.mqttca = self.config["mqtt-ca-cert"]
	self.mqtthost = self.config["mqtt-host"]
	self.mqttport = self.config["mqtt-port"]
	self.mqttauth = self.config["mqtt-auth"]
	self.mqttuser = self.config["mqtt-user"]
	self.mqttpass = self.config["mqtt-pass"]
	self.mqttname = self.config["mqtt-name"]
    
    def initialize(self):
        self.load_data_files(dirname(__file__))
        self. __build_complex_command_1()
        
    def __build_complex_command_1(self):
        intent = IntentBuilder("mymqttIntent").require("CommandKeyword").optionally("ZoneKeyword").require("ModuleKeyword").require("ActionKeyword").build()
        self.register_intent(intent, self.handle_single_command)

    def handle_single_command(self, message):
        cmd_name = message.data.get("CommandKeyword")
        mdl_name = message.data.get("ModuleKeyword")
        act_name = message.data.get("ActionKeyword")
        zkw_name = message.data.get("ZoneKeyword")

	zon_name = "/z_empty"
	if zkw_name:
            zon_name = "/z_" + zkw_name.replace(' ', '_') 

        #if act_name:
        #    cmd_name += '_' + act_name

        if (self.protocol == "mqtt"):
	    mqttc = mqtt.Client("MycroftAI")
	    if (self.mqttauth == "yes"):
	        mqttc.username_pw_set(self.mqttuser,self.mqttpass)
	    if (self.mqttssl == "yes"):
		mqttc.tls_set(self.mqttca) #/etc/ssl/certs/ca-certificates.crt
            mqttc.connect(self.mqtthost,self.mqttport) 
	    LOGGER.info("*************************"+ str(message))
	    mqtt_cmd = "/mycroft/" + self.mqttname + "/c_" + cmd_name + zon_name + "/m_" +  mdl_name + "/a_" + act_name
            LOGGER.info("--------" + mqtt_cmd)
	    mqttc.publish(mqtt_cmd, act_name) 
            mqttc.disconnect()
	    self.speak_dialog("cmd.sent")

	else:
            self.speak_dialog("not.found", {"command": cmd_name, "action": act_name, "module": dev_name})
            LOGGER.error("Error: {0}".format(e))
        
    def stop(self):
        pass
        
def create_skill():
    return mymqttskill()
