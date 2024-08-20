#coding=utf-8
from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect
from django.template import RequestContext
from django import forms
from app01.models import User
from app01.request_api import ShenKangRequest
from app01.sqlserver import SQLServerDB
import pyodbc  
import configparser
import sys
config = configparser.ConfigParser()
config.read('app01/conf/config.ini', encoding='utf-8')
items = config.items('ShenKang_Get_Token')
def get_upload_log():
    SKReq = ShenKangRequest(config)
    token_response = SKReq.request_token()
    if not token_response:    
        print ('未获取到token！')
        return
    get_upload_log_response = SKReq.request_upload_log(token_response)
    return get_upload_log_response

def upload_disease_data(start_date, end_date):
    server = config.get('Database', 'server')
    port = config.get('Database', 'port')
    database = config.get('Database', 'database')
    username = config.get('Database', 'username')
    password = config.get('Database', 'password')
    db = SQLServerDB(server, port, database, username, password)  
    db_connect = db.connect()  
    result = db.first_visit(start_date, end_date)
    return result
#Create your views here.
class UserForm(forms.Form):    
	username = forms.CharField(label='username',max_length=50)
	password = forms.CharField(label='password',widget=forms.PasswordInput())
    
class UploadDataForm(forms.Form):
    start_date = forms.CharField(label='start_date',max_length=50)
    end_date = forms.CharField(label='end_date',max_length=50)
    model_type = forms.CharField(label='model_type',max_length=50)


#登录
def login(request):
	if request.method == 'POST':
		userform = UserForm(request.POST)
		if userform.is_valid():
			username = userform.cleaned_data['username']
			password = userform.cleaned_data['password']
			user = User.objects.filter(username=username,password=password)
			
			if user:
				request.session['username'] = username
				nextfullurl = request.get_full_path()
				if nextfullurl.find('?next=') != -1:
					R_url = nextfullurl.split('?next=')[1]
				else:
					R_url = '/index/'
				return HttpResponseRedirect(R_url, {'userform':userform})
			else:
				status="用户名/密码错误"
				return render(request, 'login.html', {'userform':userform,'status':status})

	else:
		userform = UserForm()
	return render(request, 'login.html',{'userform':userform})

#登陆后主页显示
def index(request):
    
    username = request.session.get('username')
    uploadForm = UploadDataForm(request.POST)
    if username:  
        if request.method == 'POST':   
            if uploadForm.is_valid():
                start_date = uploadForm.cleaned_data['start_date']
                end_date = uploadForm.cleaned_data['end_date']
                model_type = uploadForm.cleaned_data['model_type']
                print (start_date, end_date, model_type)
            print ('test')
            status = upload_disease_data(start_date, end_date)
            return render(request, 'index.html', {'username':username, 'status':status})
        return render(request, 'index.html', {'username':username})
    else:
        return  HttpResponseRedirect('/login/?next=/index/', {'username':username})
"""
#登陆后主页显示
def index(request):
    
    username = request.session.get('username')
    userform = UserForm(request.POST)
    if username:
        
        if request.method == 'POST':   
            print ('test')
            response_data = get_upload_log()
            if response_data and response_data['code'] == 200:
                status = ''
                is_success = response_data['data']['items'][0]['isSuccess']
                if is_success == '成功':
                    status = '上传状态：成功！'
                else:
                    status = '上传数据失败，错误信息： %s' % response_data['data']['items'][0]['erroDetail'][0]['detail']

                #status = response_data
                return render(request, 'index.html', {'username':username, 'status':status})
            else:
                status = '请求失败，请查看日志获取详细信息！'
                return render(request, 'index.html', {'username':username, 'status':status})
        return render(request, 'index.html', {'username':username})
    else:
        return  HttpResponseRedirect('/login/?next=/index/', {'userform':userform})
"""
#登出
def logout(request):
	try:
		del request.session['username']
	except KeyError:
		pass
	return HttpResponseRedirect('/index')

#账户界面
def account(request):
	username = request.session.get('username')
	if username:
		user = User.objects.get(username=username)
		user.is_changed = False
		email = user.email
		user.save()
		return render(request, 'account.html', {'username':username, 'user':user})
	else:
		userform = UserForm(request.POST)
		return HttpResponseRedirect('/login/?next=/account/', {'userform':userform})


#修改密码页面
def show_change_password(request):
	username = request.session.get('username')
	if username:
		user = User.objects.get(username__exact=username)
		# user.is_changed = False
		# user.save()
		return render(request, 'change_password.html', {'username':username, 'user':user})
	else:
		userform = UserForm(request.POST)
		return HttpResponseRedirect('/login/?next=/account/change_password', {'userform':userform})

#修改密码
def change_password(request):
	username = request.session.get('username')

	if username:
		user = User.objects.get(username__exact=username)
		if request.method == 'POST':
			password_1 = request.POST.get("password1")
			password_2 = request.POST.get("password2")

			if password_1 == password_2:
				user.password = password_1
				user.is_changed = True
				user.save()
				return HttpResponseRedirect('/account/change_password', {'username':username, 'user':user})
			else:
				msg = "两次输入不一致"
				return render(request, 'change_password.html', {'username':username, 'msg':msg, 'user':user})
	else:
		userform = UserForm(request.POST)
		return HttpResponseRedirect('/login', {'userform':userform})
