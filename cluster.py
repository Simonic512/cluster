# -*- coding: utf-8 -*-

"""
cluster algorithm by Clustering by fast search and find of density peaks.
author :simon
date: 3/11/2016

"""

import my_tools
import numpy
import math

import matplotlib
import matplotlib.pyplot as plt

class Point(object):
	"""point class for each feature to draw """

	def __init__(self,name,features,label):
		
		self.name = name
		self.features = features
		self.label = label
		self.density = 0
		self.deta = 0
		self.gama = 0

	def get_label(self):
		return self.label

	def get_features(self):
		return self.features

	def get_density(self):
		return self.density

	def get_name(self):
		return self.name

def distance_cos(point_a,point_b):
	return my_tools.count_cos(point_a.get_features(),point_b.get_features())

def distance_eur(point_a,point_b):
	return my_tools.count_euclidean(point_a.get_features(),point_b.get_features())

def load_points(dataset='iris'):

	# deal new dataset only need add if case. amazing! :)

	points_list = []

	if dataset == 'iris':
		features,labels,_ = my_tools.load_iris()
		if len(features) == len(labels):
			length = len(features)
			for i in range(length):
				points_list.append(Point(str(i), features[i], labels[i]))

	

	if dataset == 'banana':
		pass

	if dataset == 'fig2':

		with open('fig2_panelB.dat') as f:
			count = 0
			for line in f.readlines():
				points_list.append(Point(str(count),[float(line.strip().split(',')[0]),float(line.strip().split(',')[1])],0))
				count += 1

	return points_list
def count_distance(dataset='iris'):

	points_list = load_points(dataset)
	length = len(points_list)

	distance_array = numpy.zeros((length,length))

	for i in range(length-1):
		for j in range(1,length-i):
			dis = distance_eur(points_list[i],points_list[i+j])
			distance_array[int(points_list[i].get_name())][int(points_list[i+j].get_name())] = dis
			distance_array[int(points_list[i+j].get_name())][int(points_list[i].get_name())] = dis

	return distance_array

def _count_density(dataset='iris'):

	# cut-off kernel

	points_list = load_points(dataset)
	distance_array = count_distance(dataset)
	length = len(points_list)

	DC = 0.24494897427831799

	for p in points_list:
		count = 0
		for i in range(length):
			if distance_array[int(p.name)][i] < DC:
				count += 1
		p.density = count

	return points_list

def count_density(dataset='iris'):

	# Gaussian kernel

	points_list = load_points(dataset)
	distance_array = count_distance(dataset)
	length = len(points_list)

	#DC = 0.24494897427831799 iris
	#DC = 0.1732050807568884
	#DC = 0.033261992737589251  

	DC = count_dc(dataset)

	for p in points_list:
		count = 0
		for i in range(length):
			if int(p.name) != i:
				count += math.e**(-(distance_array[int(p.name)][i]/DC)**2)
		p.density = count

	return points_list

def count_deta(dataset='iris'):

	# choose the point who has the bigest density?

	points_list = count_density(dataset)
	distance_array = count_distance(dataset)

	max_point = sorted(points_list,key=lambda x:x.density)[-1]
	max_deta = distance_array[int(max_point.name)].max()
	length = len(points_list)
	
	for i in range(length):
		max_point_list = []
		min_dis_list = []

		if points_list[i] != max_point:
			for p in points_list:
				if points_list[i].density < p.density:
					max_point_list.append(p)

			for k in max_point_list:
				min_dis_list.append(distance_array[i][int(k.name)])

			if len(min_dis_list) > 1:
				points_list[i].deta = sorted(min_dis_list)[1]
			elif len(min_dis_list) == 1:
				points_list[i].deta = min_dis_list[0]

	max_point.deta = max_deta
	
	return points_list

def draw(dataset='iris'):

	# draw a decision picture

	points_list = count_deta(dataset)
	x,y = [],[]

	for p in points_list:
		x.append(p.density)
		y.append(p.deta)

	print(len(x))
	print(len(y))

	my_tools.draw_scatter(x, y)

def choose_cluster_centers(dataset='iris'):

	# just test.

	points_list = count_deta(dataset)

	for p in points_list:
		p.gama = p.deta*p.density

	points_list.sort(key = lambda x:x.gama)

	print('first point: '+str(points_list[-1].name)+','+str(points_list[-1].label)+'gama: '+str(points_list[-1].gama))
	print('second point: '+str(points_list[-2].name)+','+str(points_list[-2].label)+'gama: '+str(points_list[-2].gama))
	print('third point: '+str(points_list[-3].name)+','+str(points_list[-3].label)+'gama: '+str(points_list[-3].gama))
	print('4th point: '+str(points_list[-4].name)+','+str(points_list[-4].label)+'gama: '+str(points_list[-4].gama))
	print('5th point: '+str(points_list[-5].name)+','+str(points_list[-5].label)+'gama: '+str(points_list[-5].gama))

def count_dc(dataset='iris'):

	# count DC by auto.

	PERCENT = .02

	distance_array = count_distance(dataset)
	distanceset = set()

	for i in distance_array:
		for j in i:
			distanceset.add(j)

	cut = round(len(distanceset)*PERCENT)
	distance_list = list(distanceset)
	distance_list.sort()
	dc = distance_list[cut]

	return dc

def auto_choose_center(dataset='iris'):

	num = int(input('input the number of cluster center: (9)'))
	points_list = count_deta(dataset)
	distance_array = count_distance(dataset)
	DC = count_dc(dataset)
	points_list.sort(key=lambda x:x.density*x.deta)

	# draw picture of deta and density
	# has some bug.
	# filter
	temp_list = []
	count = 1
	for p in points_list[::-1]:
		boolean = 0
		if temp_list == []:
			temp_list.append(p)
		elif count < num and temp_list != []:
			for t in temp_list:
				if distance_array[int(p.name)][int(t.name)] < DC:
					boolean = 1
			if boolean == 0:
				temp_list.append(p)
				count += 1
					
	return temp_list
	

def draw4center(dataset='iris'):

	# just draw pic for n center.

	center_list = auto_choose_center(dataset)
	points_list = count_deta(dataset)

	center_x,center_y = [],[]

	for center in center_list:
		center_x.append(center.density)
		center_y.append(center.deta)

	x,y = [],[]

	for p in points_list:
		x.append(p.density)
		y.append(p.deta)

	fig = plt.figure()
	ax = fig.add_subplot(111)
	# split the picture to 1 row 1 col ,choose the 1st part.
	# ax.scatter(x, y, c=colors,s=size_of_point)
	ax.scatter(x,y)
	ax.scatter(center_x,center_y,color='r',s=10)
	plt.show()

def cluster(dataset='iris'):

	# cluster by centers
	center_list = auto_choose_center(dataset)
	points_list = count_deta(dataset)
	distance_array = count_distance(dataset)
	class_num = len(center_list)

	# emus = ['*r','*g','*b','or','og','ob','+r','+g','+b']
	count = 0

	# label the center point
	for cp in center_list:
		cp.label = count
		count += 1
	# label the other point
	for p in points_list:
		r = 10000
		for cp in center_list:
			if distance_array[int(p.name)][int(cp.name)]<r:
				r = distance_array[int(p.name)][int(cp.name)]
				p.label = cp.label
				print(str(p.name)+','+str(p.label)+','+str(r))
			else:
				pass

	return class_num,points_list

def draw_clustered(dataset='iris'):

	class_num,points_list = cluster(dataset)
	emus = ['#faebd7','#000000','#0000ff','#7cfc00','#ffff00','#ff0000','#d2691e','#9400d3','#ff4500','#4682b4'][:class_num]

	fig = plt.figure()
	ax = fig.add_subplot(111)

	for i in range(class_num):
		x,y = [],[]
		l_list = _draw_clustered(points_list,i)
		for l in l_list:
			x.append(l.features[0])
			y.append(l.features[1])
		
		ax.scatter(x,y,color=emus[i])

	plt.show()

def _draw_clustered(points_list,num):
	l_list = []
	for p in points_list:
		if int(p.label) == int(num):
			l_list.append(p)
			#print('bcds')

	return l_list

def _test(s=20):

	# just for test

	_,x,y = my_tools.load_fig2()
	my_tools.draw_scatter(x, y,s)

def _draw_center(dataset='iris'):
	center_list = auto_choose_center(dataset)
	points_list = count_deta(dataset)
	cx,cy = [],[]
	px,py = [],[]
	fig = plt.figure()
	ax = fig.add_subplot(111)

	for cp in center_list:
		cx.append(cp.features[0])
		cy.append(cp.features[1])
		

	for p in points_list:
		if p not in center_list:
			px.append(p.features[0])
			py.append(p.features[1])

	
	ax.scatter(px,py,color='b')
	ax.scatter(cx,cy,color='r')
	plt.show()


	



