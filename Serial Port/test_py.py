"""\ Some tests for the serial module. Part of pyserial=20
(http://pyserial.sf.net) (C)2001-2009 cliechti@gmx.net Intended to be =
run on=20
different platforms, to ensure portability of the code. For all these =
tests a=20
simple hardware is required. Loopback HW adapter: Shortcut these pin =
pairs: TX=20
&lt;-&gt; RX RTS &lt;-&gt; CTS DTR &lt;-&gt; DSR On a 9 pole DSUB these =
are the=20
pins (2-3) (4-6) (7-8) """ import unittest import threading import time =
import=20
sys import serial # on which port should the tests be performed: PORT =
=3D 0 if=20
sys.version_info &gt;=3D (3, 0): def data(string): return bytes(string, =
'latin1')=20
bytes_0to255 =3D bytes(range(256)) else: def data(string): return string =

bytes_0to255 =3D ''.join([chr(x) for x in range(256)]) def =
segments(data,=20
size=3D16): for a in range(0, len(data), size): yield data[a:a+size] =
class=20
Test4_Nonblocking(unittest.TestCase): """Test with timeouts""" timeout =
=3D 0 def=20
setUp(self): self.s =3D serial.serial_for_url(PORT, =
timeout=3Dself.timeout) def=20
tearDown(self): self.s.close() def test0_Messy(self): """NonBlocking=20
(timeout=3D0)""" # this is only here to write out the message in verbose =
mode #=20
because Test3 and Test4 print the same messages def =
test1_ReadEmpty(self):=20
"""timeout: After port open, the input buffer must be empty"""=20
self.failUnlessEqual(self.s.read(1), data(''), "expected empty buffer") =
def=20
test2_Loopback(self): """timeout: each sent character should return =
(binary=20
test). this is also a test for the binary capability of a port.""" for =
block in=20
segments(bytes_0to255): length =3D len(block) self.s.write(block) # =
there might be=20
a small delay until the character is ready (especially on win32)=20
time.sleep(0.05) self.failUnlessEqual(self.s.inWaiting(), length, =
"expected=20
exactly %d character for inWainting()" % length)=20
self.failUnlessEqual(self.s.read(length), block)#, "expected a %r which =
was=20
written before" % block) self.failUnlessEqual(self.s.read(1), data(''),=20
"expected empty buffer after all sent chars are read") def=20
test2_LoopbackTimeout(self): """timeout: test the timeout/immediate =
return.=20
partial results should be returned.""" self.s.write(data("HELLO"))=20
time.sleep(0.1) # there might be a small delay until the character is =
ready=20
(especially on win32 and rfc2217) # read more characters as are =
available to run=20
in the timeout self.failUnlessEqual(self.s.read(10), data('HELLO'), =
"expected=20
the 'HELLO' which was written before") =
self.failUnlessEqual(self.s.read(1),=20
data(''), "expected empty buffer after all sent chars are read") class=20
Test3_Timeout(Test4_Nonblocking): """Same tests as the NonBlocking ones =
but this=20
time with timeout""" timeout =3D 1 def test0_Messy(self): """Blocking=20
(timeout=3D1)""" # this is only here to write out the message in verbose =
mode #=20
because Test3 and Test4 print the same messages class=20
SendEvent(threading.Thread): def __init__(self, serial, delay=3D3):=20
threading.Thread.__init__(self) self.serial =3D serial self.delay =3D =
delay self.x =3D=20
threading.Event() self.stopped =3D 0 self.start() def run(self):=20
time.sleep(self.delay) self.x.set() if not self.stopped:=20
self.serial.write(data("E")) self.serial.flush() def isSet(self): return =

self.x.isSet() def stop(self): self.stopped =3D 1 self.x.wait() class=20
Test1_Forever(unittest.TestCase): """Tests a port with no timeout. These =
tests=20
require that a character is sent after some time to stop the test, this =
is done=20
through the SendEvent class and the Loopback HW.""" def setUp(self): =
self.s =3D=20
serial.serial_for_url(PORT, timeout=3DNone) self.event =3D =
SendEvent(self.s) def=20
tearDown(self): self.event.stop() self.s.close() def =
test2_ReadEmpty(self):=20
"""no timeout: after port open, the input buffer must be empty (read). a =

character is sent after some time to terminate the test (SendEvent).""" =
c =3D=20
self.s.read(1) if not (self.event.isSet() and c =3D=3D data('E')):=20
self.fail("expected marker (evt=3D%r, c=3D%r)" % (self.event.isSet(), =
c)) class=20
Test2_Forever(unittest.TestCase): """Tests a port with no timeout""" def =

setUp(self): self.s =3D serial.serial_for_url(PORT, timeout=3DNone) def=20
tearDown(self): self.s.close() def test1_inWaitingEmpty(self): """no =
timeout:=20
after port open, the input buffer must be empty (inWaiting)"""=20
self.failUnlessEqual(self.s.inWaiting(), 0, "expected empty buffer") def =

test2_Loopback(self): """no timeout: each sent character should return =
(binary=20
test). this is also a test for the binary capability of a port.""" for =
block in=20
segments(bytes_0to255): length =3D len(block) self.s.write(block) # =
there might be=20
a small delay until the character is ready (especially on win32 and =
rfc2217)=20
time.sleep(0.05) self.failUnlessEqual(self.s.inWaiting(), length)#, =
"expected=20
exactly %d character for inWainting()" % length)=20
self.failUnlessEqual(self.s.read(length), block) #, "expected %r which =
was=20
written before" % block) self.failUnlessEqual(self.s.inWaiting(), 0, =
"expected=20
empty buffer after all sent chars are read") class=20
Test0_DataWires(unittest.TestCase): """Test modem control lines""" def=20
setUp(self): self.s =3D serial.serial_for_url(PORT) def tearDown(self):=20
self.s.close() def test1_RTS(self): """Test RTS/CTS""" self.s.setRTS(0)=20
time.sleep(1.1) self.failUnless(not self.s.getCTS(), "CTS -&gt; 0")=20
self.s.setRTS(1) time.sleep(1.1) self.failUnless(self.s.getCTS(), "CTS =
-&gt; 1")=20
def test2_DTR(self): """Test DTR/DSR""" self.s.setDTR(0) time.sleep(1.1) =

self.failUnless(not self.s.getDSR(), "DSR -&gt; 0") self.s.setDTR(1)=20
time.sleep(1.1) self.failUnless(self.s.getDSR(), "DSR -&gt; 1") def=20
test3_RI(self): """Test RI""" self.failUnless(not self.s.getRI(), "RI =
-&gt; 0")=20
class Test_MoreTimeouts(unittest.TestCase): """Test with timeouts""" def =

setUp(self): # create an closed serial port self.s =3D =
serial.serial_for_url(PORT,=20
do_not_open=3DTrue) def tearDown(self): self.s.close() def=20
test_WriteTimeout(self): """Test write() timeout.""" # use xonxoff =
setting and=20
the loop-back adapter to switch traffic on hold self.s.port =3D PORT=20
self.s.writeTimeout =3D 1 self.s.xonxoff =3D 1 self.s.open()=20
self.s.write(serial.XOFF) time.sleep(0.5) # some systems need a little =
delay so=20
that they can react on XOFF t1 =3D time.time()=20
self.failUnlessRaises(serial.SerialTimeoutException, self.s.write, =
data("timeout=20
please"*200)) t2 =3D time.time() self.failUnless( 0.9 &lt;=3D (t2-t1) =
&lt; 2.1,=20
"Timeout not in the given interval (%s)" % (t2-t1)) if __name__ =3D=3D =
'__main__':=20
import sys sys.stdout.write(__doc__) if len(sys.argv) &gt; 1: PORT =3D =
sys.argv[1]=20
sys.stdout.write("Testing port: %r\n" % PORT) sys.argv[1:] =3D ['-v'] # =
When this=20
module is executed from the command-line, it runs all its tests =
unittest.main()=20
</BODY></HTML>
