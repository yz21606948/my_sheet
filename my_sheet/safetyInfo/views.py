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
	year=int(strftime("%Y",localtime()))
	month=int(strftime("%m",localtime()))
	start_day,end_day=compute_current_day(year,month)


	date_from=datetime.date(year,month,start_day)
	date_to=datetime.datetime(year,month,end_day)
	problem_attr_count=get_attr_count(date_from,date_to)[0]
	prevent_attr_count=get_attr_count(date_from,date_to)[1]
	if not prevent_attr_count:
		errors.append("当月尚未有预警记录!")
	return render(request,'tendency.html',{'problem_attr_count':problem_attr_count,'prevent_attr_count':prevent_attr_count,'errors':errors})

def get_tendency_table(request):
	errors=[]
	problem_attr_count={}
	prevent_attr_count={}
	errors,problem_attr_count,prevent_attr_count=get_tendency_data(request)
	return render(request,'tendency_table.html',{'errors':errors,'problem_attr_count':problem_attr_count,'prevent_attr_count':prevent_attr_count})

def get_tendency_chart(request):
	errors=[]
	problem_attr_count={}
	prevent_attr_count={}
	errors,problem_attr_count,prevent_attr_count=get_tendency_data(request)
	return render(request,'tendency_chart.html',{'errors':errors,'problem_attr_count':problem_attr_count,'prevent_attr_count':prevent_attr_count})

def implement(request):
	alarm_list=[]
	errors=[]
	year=int(strftime("%Y",localtime()))
	month=int(strftime("%m",localtime()))
	start_day,end_day=compute_current_day(year,month)

	date_from=datetime.date(2017,2,1)
	date_to=datetime.date(2017,2,28)

	alarm_attr_count=get_attr_count(date_from,date_to)[2]
	for attr in alarm_attr_count.keys():
		alarm_list.extend(SafeInformation.objects.filter(problem_attribute__contains=attr))

	if not alarm_list:
			errors.append('所查区间内尚未有预警记录!')

	#分页
	paginator=Paginator(alarm_list,2)
	page=request.GET.get('page')
	try:
		contacts=paginator.page(page)
	except PageNotAnInteger:
		contacts=paginator.page(1)
	except EmptyPage:
		contacts=paginator.page(paginator.num_pages)


	return render(request,'implement.html',{'contacts':contacts,"errors":errors})

def information(request):
	if 'q' in request.GET and request.GET['q']:
		problem_id=request.GET['q']
		problem=SafeInformation.objects.get(id=problem_id)
	return render(request,'information.html',{'problem':problem})





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


def get_tendency_data(request):
	errors=[]
	if request.method == 'POST':
		date_from=request.POST['date_from']
		date_to=request.POST['date_to']
		problem_attr_count=get_attr_count(date_from,date_to)[0]
		prevent_attr_count=get_attr_count(date_from,date_to)[1]
		if not prevent_attr_count:
			errors.append('所查区间内尚未有预警记录!')
	else:
		errors.append('查询未完成，请重新查询!')
	return (errors,problem_attr_count,prevent_attr_count)



def compute_current_day(year,month):
	start_day,end_day=1,0
	
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
	return (start_day,end_day)