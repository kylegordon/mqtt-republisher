## A mocker test rig for mqtt-republisher, from Kevin McDermott.
## Some things I should read...
## http://www.python.org/dev/peps/pep-0008/
## http://www.python.org/dev/peps/pep-3101/
## http://www.python.org/dev/peps/pep-0257/

from mocker import MockerTestCase

from republisher import MQTTRepublisher


class MQTTRepublisherTestCase(MockerTestCase):

  def test_instantiation(self):
    """
    An MQTTRepublisher can be instantiated
    """
    republisher = MQTTRepublisher("192.168.1.2")
    self.assertEqual("192.168.1.2", republisher.host)

  def test_instantiation_default_port(self):
    """
    The port should default to 1883, the default port for Mosquitto.
    """
    republisher = MQTTRepublisher("192.168.1.2")
    self.assertEqual(1883, republisher.port)

  def test_instantiation_set_the_port(self):
    """
    It should be possible to define a custom port to connect to.
    """
    republisher = MQTTRepublisher("192.168.1.2", port=1234)
    self.assertEqual(1234, republisher.port)

  def test_default_logfile(self):
    """
    The logfile should default to /var/log/mqtt-republisher.log.
    """
    republisher = MQTTRepublisher("192.168.1.2")
    self.assertEqual("/var/log/mqtt-republisher.log", republisher.logfile)

  def test_instantiation_set_the_logfile(self):
    """
    It should be possible to define a logfile name.
    """
    republisher = MQTTRepublisher("192.168.1.2", logfile="/tmp/logfile")
    self.assertEqual("/tmp/logfile", republisher.logfile)

