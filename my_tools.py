# -*- coding:utf-8 -*-

"""
basic tools about deal data,countdistance etc. 

author: simon
date: 3/11/2016
"""
import matplotlib
import matplotlib.pyplot as plt
import numpy

def load_iris():

	# load iris dataset as float

	with open('iris.data.txt') as f:
		lines = f.readlines()
		length = len(lines)
		label,feature,data = [],[],[]
		x,y,z,w = [],[],[],[]

		for i in range(length):
			label.append(lines[i].strip().split(',')[-1])
			#_data = []
			feature.append([float(l) for l in lines[i].strip().split(',')[:4]])
			data.append([float(l) for l in lines[i].strip().split(',')[:4]]+[lines[i].strip().split(',')[-1]])

		return feature,label,data

def load_banana():

	# load banana dataset as float
	data,x,y = [],[],[]
	with open('banana') as f:
		for line in f.readlines():
			data.append([float(i) for i in line.strip().split(',')])
			x.append(float(line.strip().split(',')[0]))
			y.append(float(line.strip().split(',')[-1]))

	return data,x,y

def load_fig2():

	data,x,y = [],[],[]
	with open('fig2_panelB.dat') as f:
		for line in f.readlines():
			data.append([float(i) for i in line.strip().split(',')])
			x.append(float(line.strip().split(',')[0]))
			y.append(float(line.strip().split(',')[-1]))

	return data,x,y


def draw_scatter(x,y,s=20):

	# draw scatter picture (2D)

	fig = plt.figure()
	ax = fig.add_subplot(111)
	# split the picture to 1 row 1 col ,choose the 1st part.
	# ax.scatter(x, y, c=colors,s=size_of_point)
	ax.scatter(x,y,s)
	plt.show()

def count_cos(list_a,list_b):

	# count cosine distance 

	b,b1,b2,b3 = 0,0,0,0

	if len(list_a) == len(list_b):
		for i in range(len(list_a)):	
			b1 += float(list_a[i])**2 
			b2 += float(list_b[i])**2
			b3 += float(list_a[i])*float(list_b[i])
			b = (b1**(0.5))*(b2**(0.5))

	return b3/b

def count_euclidean(list_a,list_b):

	# count euclidean distance 
	
	a = 0

	if len(list_a) == len(list_b):
		for i in range(len(list_a)):
			a += (float(list_a[i]) - float(list_b[i]))**2

	return a**0.5

def _print():

	# what's this? :)
	
	print('\n'.join([''.join([('complete'[(x-y)%8]if((x*0.05)**2+(y*0.1)**2-1)**3-(x*0.05)**2*(y*0.1)**3<=0 else' ')for x in range(-30,30)])for y in range(15,-15,-1)]))


