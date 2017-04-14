# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render_to_response
from safetyInfo.models import SafeInformation
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger
from time import strftime,localtime
import datetime

#问题属性
problem_attrs=[
	'持单作业',
	'劳动保护',
	'工具设备借用',
	'安全管理',
	'生产控制',
	'机库管理',
	'维修记录',
	'数据采集',
	'人员资质',
	'工具设备控制',
	'培训管理',
	'其他',
]

def home(request):
	return render(request,'home.html')

def tendency(request):
	errors=[]
	start_day,end_day=1,0

	#显示当前时间
	year=int(strftime("%Y",localtime()))
	month=int(strftime("%m",localtime()))
	if month in [1,3,5,7,8,10,12]:
		end_day=31
	elif month in [2,4,6,9,11]:
		end_day=30
	else:
		if (year % 4) == 0:
			if (year % 100) == 0:
				if (year % 400) == 0:
					end_day=29
				else:
					end_day=28
			else:
				end_day=29
		else:
			end_day=28
	
	date_from=datetime.date(2017,1,1)
	date_to=datetime.datetime(2017,1,31)
	problem_attr_count=get_attr_count(date_from,date_to)[0]
	prevent_attr_count=get_attr_count(date_from,date_to)[1]
	if not prevent_attr_count:
		errors.append("当月尚未有预警记录!")
	print problem_attr_count
	print prevent_attr_count
	return render(request,'tendency.html',{'problem_attr_count':problem_attr_count,'prevent_attr_count':prevent_attr_count,'errors':errors})

def get_attr_count(date_from,date_to):
	problem_attr_count={}
	prevent_attr_count={}
	alarm_attr_count={}

	for attr in problem_attrs:
		problem_attr_count[attr]=SafeInformation.objects.problem_attr_count(attr,date_from,date_to)

	for key,value in problem_attr_count.items():
		if value > 0 and value < 3:
			prevent_attr_count[key]=value
		elif value > 2:
			alarm_attr_count[key]=value
	return (problem_attr_count,prevent_attr_count,alarm_attr_count) 
