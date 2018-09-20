from django.shortcuts import render,HttpResponse,redirect
from django import http
# Create your views here.
from app01.models import *

# def index(req):
#     if req.COOKIES.get("username",None) == "lv":
#         name = req.COOKIES.get("username",None)
#         return render(req,"index.html",locals())
#     else:
#         return redirect("/login/")
#
#     # return HttpResponse("hello word! Django")
#
#
# info_list = []

# def user_info(req):
#     if req.method == "POST":
#         username = req.POST.get("username",None)
#         sex = req.POST.get("sex",None)
#         email = req.POST.get('email',None)
#
#         info = {"username": username,
#                 "sex":sex,
#                 "email":email}
#         info_list.append(info)
#     return render(req,"student.html",{"info_list":info_list})
#
# def haha(req):
#     if req.method == "POST":
#         username = req.POST.get("username",None)
#         sex = req.POST.get("sex",None)
#         email = req.POST.get('email',None)
#
#     #插入表数据
#     models.UserInfo.objects.create()

def index(request):


    return render(request,"index.html")

# class SshUpFile:
#
#     def __init__(self,hostname,username,password,port=22):
#
#         self.hostname = hostname
#         self.port = port
#         self.username =username
#         self.password = password
#
#     def up_file(self,file):
#         import datetime
#         import paramiko
#         print('上传开始')
#         # begin = datetime.datetime.now()
#
#         #ssh控制台
#         ssh = paramiko.SSHClient()
#         ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy)
#         ssh.connect(hostname=self.hostname,port=self.port)
#
#         #ssh传输
#         # transport = paramiko.Transport(self.hostname,self.port)
#         # transport.connect(username=self.username,password=self.password)
#         sftp = paramiko.SFTPClient.from_transport(ssh)
#         try:
#             sftp.put(file,remotepath="/root/")
#         except Exception:
#             print("报错了")
#
#         sftp.close()
#         ssh.close()

def upload(request):
    from common import common
    if request.method == "POST":
        file_obj = request.FILES.get('file')
        print(file_obj)
        # print(request.POST.host)
        host = request.POST.get("host")
        pwd = request.POST.get("pwd")
        user = request.POST.get("user")
        print(host,pwd,user)
        with open("upload/"+file_obj.name,'wb') as f:
            for line in file_obj:
                f.write(line)
        a = common.SshUpFile(hostname=host,username=user,password=pwd)
        res = a.up_file("upload/"+file_obj.name,remotepath="/root/%s" %file_obj.name)
        print(res)
        return HttpResponse("ok")
    return render(request,'upload.html')