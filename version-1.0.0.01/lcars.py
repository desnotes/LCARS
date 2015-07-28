'''LCARS /ˈɛlkɑrz/;'''
'''================'''
'''version 1.0.0.01'''
'''28 Jul 2015'''
''' This is the first LCARS UI'''
from cStringIO import StringIO
import sys,io,os,time,math
global sys,math
import Tkinter as tk
import win32con
from Tkinter import StringVar
from PIL import Image,ImageDraw,ImageFont,ImageTk
import numpy as np
global np,tk,Image,ImageDraw,ImageFont,ImageTk
global win,w,pg_1_text,lcars_pad,lcars_pad2
# from StackOverflow.com Q#7966119 answer by unutbu 1 Nov 2011
class FullScreenApp(object):
	def __init__(self, master, **kwargs):
		self.master=master
		# from StackOverflow.com Q#4481880 answer by user225312 19 Dex 2010
		self.master.wm_state('zoomed')
		self.master.attributes('-fullscreen', True)
		self.state=True
		self.frame=tk.Frame(master=self.master,bg='#000000')
		self.frame.pack(fill='both',expand='yes')
		self.master.bind('<Escape>',self.toggle_geom)
	def toggle_geom(self,event=None):
		# from StackOverflow.com Q#7966119 answer by Shule 24 May 2014
		self.state = not self.state
		self.master.attributes('-fullscreen', self.state)

def lcars_polygon(canvas,x,y,t,x1,y1,t1):
	poly=[]
	jj=(abs(y1-y)-lcars_pad2)*1.00/(abs(x1-x)-lcars_pad2)
	ii=(abs(x1-x)-lcars_pad2)*1.00/(abs(y1-y)-lcars_pad2)
	if x<x1:
		rd=int(20*ii)
		for i in range(abs(x1-x)-lcars_pad2):
			if i>(abs(x1-x)-lcars_pad2)-rd:
				j=int(jj*i)
				r=i-((abs(x1-x)-lcars_pad2)-rd)
				rr=int(math.sqrt((rd*rd*1.00)-(r*r)))
				poly.append((x+lcars_pad)+(rd-rr))
				poly.append((y-j)-lcars_pad)				
			else:
				j=int(jj*i)
				poly.append(x+lcars_pad)
				poly.append((y-j)-lcars_pad)
		for j in range(20,abs(y1-y)-lcars_pad2):
			if j==(abs(y1-y)-lcars_pad2)-1:
				poly.append(x1-lcars_pad)
			else:
				i=int(ii*j)			
				poly.append(x+i+lcars_pad)
			poly.append(y1+lcars_pad)
		poly.append(x1-lcars_pad)
		poly.append(y1+lcars_pad+t1)
		fy=abs(y1-y)-lcars_pad2
		for j in range(20+t,fy):
			if j==fy-1:
				poly.append(x+lcars_pad+t)
			else:
				i=int(ii*j)
				poly.append((x1-(x+i+lcars_pad))+x+lcars_pad)
			poly.append(y1+lcars_pad+t1)
		poly.append(x+lcars_pad+t)
		poly.append(y-lcars_pad)
	elif x>x1:
		rd=int(20*ii)
		for i in range(abs(x1-x)-lcars_pad2):
			if i>(abs(x1-x)-lcars_pad2)-rd:
				j=int(jj*i)
				r=i-((abs(x1-x)-lcars_pad2)-rd)
				rr=int(math.sqrt((rd*rd*1.00)-(r*r)))
				poly.append((x-lcars_pad)-(rd-rr))
				poly.append((y-j)-lcars_pad)				
			else:
				j=int(jj*i)
				poly.append(x-lcars_pad)
				poly.append((y-j)-lcars_pad)
		for j in range(20,abs(y1-y)-lcars_pad2):
			if j==(abs(y1-y)-lcars_pad2)-1:
				poly.append(x1+lcars_pad)
			else:
				i=int(ii*j)			
				poly.append((x-i)-lcars_pad)
			poly.append(y1+lcars_pad)
		poly.append(x1+lcars_pad)
		poly.append(y1+lcars_pad+t1)
		fy=abs(y1-y)-lcars_pad2
		for j in range(20+t,fy):
			if j==fy-1:
				poly.append((x-lcars_pad)-t)
			else:
				i=int(ii*j)
				poly.append(x1+((x-i)-lcars_pad))
			poly.append(y1+lcars_pad+t1)
		poly.append((x-lcars_pad)-t)
		poly.append(y-lcars_pad)
	canvas.create_polygon(poly,activefill='white',outline='white',fill='blue',width=2)
	if x<x1:
		canvas.create_text([(x+lcars_pad)+80,y1+lcars_pad+20],text='LCARS:Right',font='Arialbold 11',fill='white')
	elif x>x1:
		canvas.create_text([(x-lcars_pad)-80,y1+lcars_pad+20],text='LCARS:Left',font='Arialbold 11',fill='white')

def lcars_round_box_R(canvas,x,y,w,h,text):
	x=x+(lcars_pad*3)
	y=y-lcars_pad
	poly=[]
	for i in range(w):
		poly.append(x+i)
		poly.append(y)
	for j in range(h):
		if j<h-10:
			poly.append(x+w)
			poly.append(y-j)
	for i in range(w):
		poly.append((x+w)+i)
		if i<10:
			rr=10-int(math.sqrt((10*10)-((10-i)*(10-i))))
			poly.append((y-h)+rr)
		else:
			poly.append(y-h)
	for j in range(h):
		poly.append(x)
		poly.append((y-h)+j)
	canvas.create_polygon(poly,activefill='white',outline='white',fill='yellow',width=2)
	canvas.create_text([x+5,(y-h)+5],anchor='nw',text=text,font='Arialbold 11',fill='black')

def lcars_round_box_L(canvas,x,y,w,h,text):
	x=x-(lcars_pad*3)
	y=y-lcars_pad
	poly=[]
	for i in range(w):
		poly.append((x-w)+i)
		poly.append(y)
	for j in range(h):
		if j<h-10:
			poly.append(x-w)
			poly.append(y-j)
	for i in range(w):
		poly.append((x-w)+i)
		if i<10:
			rr=10-int(math.sqrt((10*10)-((10-i)*(10-i))))
			poly.append((y-h)+rr)
		else:
			poly.append(y-h)
	for j in range(h):
		poly.append(x)
		poly.append((y-h)+j)
	canvas.create_polygon(poly,activefill='white',outline='white',fill='yellow',width=2)
	canvas.create_text([(x-w)+5,(y-h)+5],anchor='nw',text=text,font='Arialbold 11',fill='black')

win=tk.Tk()
win.title('LCARS 1.0.0.01 pre-edition')
lcars=FullScreenApp(win)
lcars_width=win.winfo_screenwidth()
lcars_height=win.winfo_screenheight()
lcars_xcen=int(lcars_width/2)
lcars_ycen=int(lcars_height/2)
lcars_pad=10
lcars_pad2=lcars_pad*2
lcars_width1=10
lcars_height1=400
w=tk.Canvas(lcars.frame,width=lcars_width,height=lcars_height,bg='#000000')
w.create_line(lcars_xcen,0,lcars_xcen,lcars_height,fill='red',dash=(4,4))
w.create_polygon([10,50,50,10,150,10,150,200,50,200],activefill='white',outline='white',fill='blue',width=2)
lcars_polygon(w,lcars_xcen,lcars_height,10,lcars_width,lcars_ycen,40)
lcars_polygon(w,lcars_xcen,lcars_height,10,0,lcars_ycen,40)
lcars_round_box_R(w,lcars_xcen,lcars_height,120,40,'Button 1')
lcars_round_box_L(w,lcars_xcen,lcars_height,120,40,'Button 1')
lcars_round_box_L(w,lcars_xcen,lcars_height-50,120,40,'Button 2')
lcars_round_box_L(w,lcars_xcen,lcars_height-100,120,40,'Button 3')
lcars_round_box_L(w,lcars_xcen,lcars_height-150,120,40,'Button 4')
def pg_1_on(self):
	global pg_1_text
	w.delete(pg_1_text)
	pg_1_text=w.create_text([100,100],text='Polygon1',fill='white')

def pg_1_off(self):
	global pg_1_text
	w.delete(pg_1_text)
	pg_1_text=w.create_text([100,100],text='',fill='white')

pg_1_text=w.create_text([100,100],text='',fill='white')
p0_X=lcars_xcen-lcars_pad
p0_Y=lcars_height-lcars_pad
p1_X=lcars_xcen-(lcars_pad+lcars_width1)
p1_Y=lcars_height-lcars_pad
p2_X=lcars_xcen-(lcars_pad+lcars_width1)
p2_Y=lcars_height-(lcars_pad+lcars_height1)
p3_X=lcars_xcen-lcars_pad
p3_Y=lcars_height-(lcars_pad+lcars_height1)
p_XY=[p0_X,p0_Y,p1_X,p1_Y,p2_X,p2_Y,p3_X,p3_Y]
#pg_1=w.create_polygon(p_XY,activefill='white',outline='white',fill='blue',width=2,tag='pg_1w')
#w.tag_bind(pg_1,'<Enter>',pg_1_on)
#w.tag_bind(pg_1,'<Leave>',pg_1_off)
w.pack()
win.mainloop()
