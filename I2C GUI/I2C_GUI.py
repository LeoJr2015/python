from Tkinter import *
import quick2wire.i2c as i2c
import time
import math

adc_address1 = 0x68
adc_address2 = 0x69

varDivisior = 64 # from pdf sheet on adc addresses and config
varMultiplier = (2.4705882/varDivisior)/1000

class App(Frame):
	def __init__(self,parent=None, **kw):
		"""Initalise the app"""
		Frame.__init__(self,parent,**kw)
		self.parent = parent
		self.flowVel = StringVar()
		self.wcInch = StringVar()
		self.flowVel.set("0.0")
		self.wcInch.set("0.0")
		Label(self, text="Flow Velocity").grid(row=0,column=0)
		self.flowVelBox = Entry(self, text=self.flowVel)
		self.flowVelBox.grid(row=0,column=1)
		Label(self, text="WC Inch").grid(row=1,column=0)
		self.wcInchBox = Entry(self, text=self.wcInch)
		self.wcInchBox.grid(row=1,column=1)
		self.initialiseADC()
		self.update()
		
	def getValues(self):
		#Read the values from the I2C ADC and update the Entry boxes
		self.flowVel.set(str(calcCFM(getadcreading(adc_address1))))
		self.wcInch.set(str(calcWc(getadcreading(adc_address1))))
		pass
	
	def initialiseADC(self):
		#Anything you need to do to get the ADC Values.
		pass

	def update(self):
		"""Runs every 500ms to update the values"""
		self._getValues()
		self._timer = self.after(500,self.update)
        
with i2c.I2CMaster() as bus:
   def changechannel(address, adcConfig):
      bus.transaction(i2c.writing_bytes(address, adcConfig))
      
   def getadcreading(address):
      h, m, l ,s = bus.transaction(i2c.reading(address,4))[0]
      while (s & 128):
         h, m, l, s  = bus.transaction(i2c.reading(address,4))[0]
      # shift bits to product result
      t = ((h & 0b00000001) << 16) | (m << 8) | l
      # check if positive or negative number and invert if needed
      if (h > 128):
         t = ~(0x020000 - t)
      return t * varMultiplier
   
   changechannel(adc_address2, 0xBC)
   VoltSup = getadcreading(adc_address2)
   
   def calcCFM(inval):
      return (((((((inval) / VoltSup ) - 0.04) / 0.09) / 0.249088908333)**(.5)) * 4005) * 0.2; #0.2 is orifice area in sq ft set to variable in real world use
   def calcWc(inval):
      return ((((inval) / VoltSup ) - 0.04) / 0.09) / 0.249088908333;
        

def main():
    root = Tk()
    root.title("Flow and WC Inch Dialog")
    a = App(root)
    a.grid()
    root.mainloop()
   

if __name__ == '__main__':
    main()
