# -*- coding: utf-8 -*-
'''LCARS /ˈɛlkɑrz/; '''
'''================='''
'''version 1.0.0.015'''
'''28 Jul 2015'''
''' This is the first LCARS UI'''
from cStringIO import StringIO
import sys,io,os,time,math
global sys,math,spock
import Tkinter as tk
import win32con
from Tkinter import StringVar
from PIL import Image,ImageDraw,ImageFont,ImageTk
import numpy as np
from SimpleCV import Camera
global np,tk,Image,ImageDraw,ImageFont,ImageTk
global win,w,main_X,main_Y,camera_id,Camera,cam
global lcars_holo_cam,holo_recorder,lcars_holo_gram,lcars_holo_gram_tag,lcars_on_cam
global lcars_image,lcars_picture
global lcars_step_line,lcars_read_text,lcars_speed_line,lcars_text_tag
global spock,vector_stack,rewrite_all_vector,move_left,move_right,move_up,move_down
global lcars_xcen,lcars_ycen,lcars_height,lcars_width,lcars_pad,lcars_pad2
global lcars_stack,lcars_stack_button_R,lcars_stack_button_L
global lcars_stack_button_xR,lcars_stack_button_xL
camera_id=0
cam = Camera(camera_id)
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
	global lcars_stack,lcars_stack_button_xR,lcars_stack_button_xL
	poly=[]
	jj=(abs(y1-y)-lcars_pad2)*1.00/(abs(x1-x)-lcars_pad2)
	ii=(abs(x1-x)-lcars_pad2)*1.00/(abs(y1-y)-lcars_pad2)
	if x<x1: #Right Polygon
		lcars_stack_button_xR=lcars_stack_button_xR+t+lcars_pad
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
	elif x>x1: # Left Polygon
		lcars_stack_button_xL=lcars_stack_button_xL+t+lcars_pad
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
	canvas.create_polygon(poly,activefill='white',outline='#FFFFCC',fill='#FF9C00',width=2,tags='lcars_'+str(lcars_stack))
	if x<x1:
		canvas.create_text([(x+lcars_pad)+80,y1+lcars_pad+20],text='LCARS:Right',font='Arialbold 11',fill='white',tags='lcars_'+str(lcars_stack+1))
	elif x>x1:
		canvas.create_text([(x-lcars_pad)-80,y1+lcars_pad+20],text='LCARS:Left',font='Arialbold 11',fill='white',tags='lcars_'+str(lcars_stack+1))
	lcars_stack=lcars_stack+2

def lcars_round_box_R(canvas,w,h,text):
	global lcars_stack,lcars_stack_button_R,lcars_stack_button_xR
	x=lcars_xcen+lcars_stack_button_xR
	y=lcars_height-lcars_stack_button_R
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
	canvas.create_polygon(poly,activefill='white',outline='#FFFFCC',fill='#C198B0',width=2,tags='lcars_'+str(lcars_stack))
	canvas.create_text([x+5,(y-h)+5],anchor='nw',text=text,font='Arialbold 11',fill='black',tags='lcars_'+str(lcars_stack+1))
	lcars_stack_button_R=lcars_stack_button_R+h+lcars_pad
	#lcars_stack_button_xR=lcars_stack_button_xR+w+lcars_pad
	lcars_stack=lcars_stack+2

def lcars_text_R(canvas,w,h,text):
	global lcars_stack,lcars_stack_button_R,lcars_stack_button_xR,lcars_step_line,lcars_read_text,lcars_text_tag
	x=lcars_xcen+lcars_stack_button_xR
	y=lcars_height-lcars_stack_button_R
	f=open(text,'r')
	lcars_read_text=f.readlines()
	f.close()
	out_text=''
	if len(lcars_read_text)>=35:
		for i in range(35):
			out_text=out_text+lcars_read_text[i]
		lcars_step_line=1
	else:
		for i in range(len(read_text)):
			out_text=out_text+read_text[i]
		lcars_step_line=(-1)
	lcars_text_tag='lcars_'+str(lcars_stack)
	canvas.create_text([x,y-h],anchor='nw',text=out_text,font='Arialbold 6',fill='white',tags=lcars_text_tag)
	lcars_stack_button_R=lcars_stack_button_R+h+lcars_pad
	lcars_stack=lcars_stack+1

def lcars_round_box_L(canvas,w,h,text):
	global lcars_stack,lcars_stack_button_L,lcars_stack_button_xL
	x=lcars_xcen-lcars_stack_button_xL
	y=lcars_height-lcars_stack_button_L
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
	canvas.create_polygon(poly,activefill='white',outline='#FFFFCC',fill='#C198B0',width=2,tags='lcars_'+str(lcars_stack))
	canvas.create_text([(x-w)+5,(y-h)+5],anchor='nw',text=text,font='Arialbold 11',fill='black',tags='lcars_'+str(lcars_stack+1))
	lcars_stack_button_L=lcars_stack_button_L+h+lcars_pad
	#lcars_stack_button_xL=lcars_stack_button_xL+w+lcars_pad
	lcars_stack=lcars_stack+2

def romulan(w,poly,x,y):
	global lcars_stack
	poly1=[]
	for i in range(0,len(poly),2):
		xx=poly[i]+x+lcars_xcen
		yy=poly[i+1]+y+lcars_ycen
		poly1.append(xx)
		poly1.append(yy)
	w.create_polygon(poly1,activefill='white',outline='white',fill='blue',width=2,tags='lcars_'+str(lcars_stack))
	lcars_stack=lcars_stack+1

def collect_all_vector():
	global vector_stack
	for i in range(lcars_stack):
		core=w.coords('lcars_'+str(i))
		vector_stack.append(core)

def rewrite_all_vector(xx,yy):
	global main_X,main_Y
	main_X=main_X+xx
	main_Y=main_Y+yy
	for i in range(lcars_stack):
		core=vector_stack[i]
		if len(core)==2:
			if (core[0]+main_X<lcars_pad or core[0]+main_X>lcars_width-lcars_pad or \
				core[1]+main_Y<lcars_pad or core[1]+main_Y>lcars_height-lcars_pad):
				w.itemconfig('lcars_'+str(i),state=tk.HIDDEN)
				continue
			w.itemconfig('lcars_'+str(i),state=tk.NORMAL)
		newcore=[]
		for c in range(0,len(core),2):
			core_x=core[c]
			core_y=core[c+1]
			if core_x>lcars_pad and core_x<lcars_width-lcars_pad:
				core_x=core_x+main_X
			if core_y>lcars_pad and core_y<lcars_height-lcars_pad-1:
				core_y=core_y+main_Y
			if core_x>lcars_width: core_x=lcars_width
			if core_x<0: core_x=0
			if core_y>lcars_height: core_y=lcars_height
			if core_y<0: core_y=0
			newcore.append(int(core_x))
			newcore.append(int(core_y))
		w.coords('lcars_'+str(i),tk._flatten(newcore))

def holo_recorder():
	image_sim = cam.getImage()
	I = image_sim.getNumpy()
	image_pil = Image.fromarray(np.uint8(I))	
	image_pil = image_pil.rotate(270)
	w,h = image_pil.size
	image_pil = image_pil.resize((int(w/4),int(h/4)),Image.ANTIALIAS)
	tkim = ImageTk.PhotoImage(image_pil)
	return tkim

def lcars_holo_cam(canvas,x,y):
	global lcars_stack,lcars_holo_gram,lcars_holo_gram_tag
	lcars_holo_gram = holo_recorder()
	lcars_holo_gram_tag = 'lcars_'+str(lcars_stack)
	canvas.create_image([x,y],anchor='nw',image=lcars_holo_gram,tags=lcars_holo_gram_tag)
	lcars_stack=lcars_stack+1

def lcars_speed_line():
	global lcars_step_line
	if lcars_step_line>=len(lcars_read_text):
		lcars_step_line=0
	out_text=''
	count=0
	for i in range(lcars_step_line,len(lcars_read_text)):
		out_text=out_text+lcars_read_text[i]
		count=count+1
		if count==35: break
	if count<35:
		out_text=out_text+'<EOF>\n\n'
		count=count+2
		if count+lcars_step_line>=len(lcars_read_text):
			ccount=lcars_step_line*(-1)
		else: ccount=count
		for i in range(ccount+lcars_step_line,len(lcars_read_text)):
			out_text=out_text+lcars_read_text[i]
			count=count+1
			if count==35: break
	lcars_step_line=lcars_step_line+1
	w.itemconfig(lcars_text_tag,text=out_text)

def lcars_on_cam():
	global spock,lcars_holo_gram
	if lcars_step_line!=(-1): lcars_speed_line()
	if lcars_holo_gram_tag=='None': 
		spock=win.after(500,lcars_on_cam)
		return
	lcars_holo_gram = holo_recorder()
	w.itemconfig(lcars_holo_gram_tag,image=lcars_holo_gram)
	spock=win.after(500,lcars_on_cam)

def lcars_picture(canvas,x,y,picture):
	global lcars_stack,lcars_image
	image_pil=Image.open(picture)	
	lcars_image.append(ImageTk.PhotoImage(image_pil))
	canvas.create_image([x,y],anchor='nw',image=lcars_image[len(lcars_image)-1],tags='lcars_'+str(lcars_stack))
	lcars_stack=lcars_stack+1

def move_left(self):
	rewrite_all_vector(-100,0)

def move_right(self):
	rewrite_all_vector(100,0)

def move_up(self):
	rewrite_all_vector(0,-50)

def move_down(self):
	rewrite_all_vector(0,50)

def on_closing():
	global spock
	win.after_cancel(spock)
	win.destroy()
#==========================================================================
# Initial section
#==========================================================================
main_X=0
main_Y=0
vector_stack=[]
win=tk.Tk()
win.title('LCARS 1.0.0.015 pre-edition')
lcars=FullScreenApp(win)
lcars_width=win.winfo_screenwidth()
lcars_height=win.winfo_screenheight()
lcars_xcen=int(lcars_width/2)
lcars_ycen=int(lcars_height/2)
lcars_pad=5
lcars_pad2=lcars_pad*2
lcars_width1=10
lcars_height1=400
lcars_stack=0
lcars_stack_button_R=lcars_pad
lcars_stack_button_L=lcars_pad
lcars_stack_button_xR=lcars_pad
lcars_stack_button_xL=lcars_pad
w=tk.Canvas(lcars.frame,width=lcars_width,height=lcars_height,bg='#000000')
w.create_line(lcars_xcen,0,lcars_xcen,lcars_height,fill='red',dash=(4,4))
#===========================================================================
# Romulan Polygon section
#===========================================================================
romulan(w,[10,50,50,10,150,10,150,200,50,200],-400,-250)
#===========================================================================
# ARC polyline section
#===========================================================================
lcars_polygon(w,lcars_xcen,lcars_height,5,lcars_width,lcars_ycen,40)
lcars_polygon(w,lcars_xcen,lcars_height,5,0,lcars_ycen,40)
#===========================================================================
# R Button section
#===========================================================================
#lcars_round_box_R(w,120,40,'Button 1')
lcars_step_line=(-1)
lcars_text_R(w,400,350,'lcars.py')
#===========================================================================
# L Button section
#===========================================================================
lcars_round_box_L(w,120,40,'Button 1')
lcars_round_box_L(w,120,40,'Button 2')
lcars_round_box_L(w,120,40,'Button 3')
lcars_round_box_L(w,120,40,'Button 4')
#===========================================================================
# Webcam image section
#===========================================================================
lcars_holo_gram_tag='None'
#lcars_holo_cam(w,lcars_xcen+100,100)
#===========================================================================
# Still image section
#===========================================================================
lcars_image=[]
lcars_picture(w,lcars_xcen+100,100,'C:/Users/wisoot/Desktop/spock.jpg')
# Collect all vector 
collect_all_vector()

w.pack()
# from StackOverflow.com Q#22161794 answer by Bryan Oakley 4 Mar 2014
w.focus_set()
win.bind('<Left>',move_left)
win.bind('<Right>',move_right)
win.bind('<Up>',move_up)
win.bind('<Down>',move_down)
spock=win.after(500,lcars_on_cam)
win.protocol("WM_DELETE_WINDOW", on_closing)
win.mainloop()
