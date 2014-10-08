#!/usr/bin/python2.6
import numpy as np
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import sys

#Script needs to be given the input file when called

fig = plt.figure()
ax= fig.add_subplot(111)

#FPGA
RF = open(str(sys.argv[1]),'r')
FLINES = RF.readlines()
time=np.array(range(len(FLINES)))
sunX=np.array(range(len(FLINES)))
sunY=np.array(range(len(FLINES)))
earthX=np.array(range(len(FLINES)))
earthY=np.array(range(len(FLINES)))
jupiterX=np.array(range(len(FLINES)))
jupiterY=np.array(range(len(FLINES)))
saturnX=np.array(range(len(FLINES)))
saturnY=np.array(range(len(FLINES)))
labels = FLINES[0].split()
print "labels: ", labels
for i in range(1,len(FLINES)):

		#				time[i] = float(FLINES[i].split()[0])
				sunX[i] = float(FLINES[i].split()[1])
				sunY[i] = float(FLINES[i].split()[2])
				earthX[i] = float(FLINES[i].split()[3])
				earthY[i] = float(FLINES[i].split()[4])
				jupiterX[i] = float(FLINES[i].split()[5])
				jupiterY[i] = float(FLINES[i].split()[6])
				saturnX[i] = float(FLINES[i].split()[7])
				saturnY[i] = float(FLINES[i].split()[8])
RF.close()

### Double precision
#RD = open(str(sys.argv[2]),'r')
#DLINES = RD.readlines()
#xd=np.array(range(len(DLINES)))
#yd=np.array(range(len(DLINES)))
#zd=np.array(range(len(DLINES)))
#for i in range(len(DLINES)):
#
#				xd[i] = float(DLINES[i].split(',')[0])
#				yd[i] = float(DLINES[i].split(',')[1])
#				zd[i] = float(2)
#RD.close()

#Plot the values
#for x,y,z,c,m,s in [(xf,yf,zf,'b','o',1),(xd,yd,zd,'r','^',2)]:
#		ax.scatter(x,y,z,c=c,marker=m,s=s,edgecolors='none')


#ax.plot(xf,yf)
ax.plot(sunX,sunY)
ax.plot(earthX,earthY)
ax.plot(jupiterX,jupiterY)
ax.plot(saturnX,saturnY)
#ax.set_xlabel('X Label')
#ax.set_ylabel('Y Label')
#ax.set_zlabel('Z Label')

plt.show()
