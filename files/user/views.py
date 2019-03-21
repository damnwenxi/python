from django.shortcuts import render,redirect,reverse
from django.utils.http import urlquote

from .models import User,Classes,Mission,Work,Messages
from django.http import StreamingHttpResponse
import os,time,zipfile
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# Create your views here.

import hashlib
# MD5加密密码
def hash_code(s, salt='mysite'):    # 加点盐
    h = hashlib.sha256()
    s += salt
    h.update(s.encode())  # update方法只接收bytes类型
    return h.hexdigest()


# 首页
def index(request):
    if request.method == 'GET':

        class_num = Classes.objects.count()
        user_num = User.objects.count()
        work_num = Work.objects.count()

        mess_list = Messages.objects.all().values('ip','last_mess','c_time')


        try:
            user = User.objects.get(id=request.session['user_id'])
            return render(request, 'index.html', context={'rows':mess_list,"role": user.role, "class_num": class_num,
                                                          "user_num": user_num, "work_num": work_num})

        except:
            return render(request, 'index.html', context={'rows':mess_list,"class_num": class_num,
                                                          "user_num": user_num, "work_num": work_num})
    else:
        # 获取IP

        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]  # 所以这里是真实的ip
        else:
            ip = request.META.get('REMOTE_ADDR')  # 这里获得代理ip

        mess = request.POST.get('mess')

        # 那到IP对象
        new_mess = Messages(ip=ip,last_mess=mess)
        new_mess.save()

        return redirect(reverse('index'))

# 注册
def register(request):
    if request.method == 'GET':
        return render(request,'register.html')
    else:
        name = request.POST.get("name")
        password = request.POST.get("password")
        email = request.POST.get("email")
        phone = request.POST.get("phone")
        sex = request.POST.get("sex")
        role = request.POST.get("role")
        desc = request.POST.get("desc")

        if name and password and email:
            same_name_user = User.objects.filter(name=name)
            if same_name_user:  # 用户名唯一
                return render(request, 'register.html', context={"tips":"该用户名已被占用！请重新输入。"})

            user = User(name=name,password=hash_code(password),email=email,phone=phone,gender=sex,role=role,description=desc)
            user.save()

            # 保存session 登录状态在线
            request.session['is_login'] = True
            request.session['user_id'] = user.id
            request.session['user_name'] = user.name

            return render(request,'user/tips.html',context={'tips':"用户注册成功！",'url':"/index/"})
        else:
            return render(request,'register.html',context={'tips':"用户名和密码不得为空！"})

# 登录
def login(request):
    # 不允许重复登录
    if request.session.get('is_login', None):
        return redirect("index")

    if request.method == 'GET':
        return render(request,'login.html')
    else:
        name = request.POST.get("name")
        password = request.POST.get("password")

        # print(name,password)

        try:
            user = User.objects.get(name=name)
            if user.password == hash_code(password):
                # 获取用户名session 登录状态在线
                request.session['is_login'] = True
                request.session['user_id'] = user.id
                request.session['user_name'] = user.name
                return redirect('index')
            else:
                message = "密码不正确！"
        except:
            message = "用户不存在！"
        return render(request,'login.html',context={'tips':message})

# 注销
def logout(request):
    if not request.session.get('is_login', None):
        # 如果本来就未登录，也就没有登出一说
        return redirect("index")
    request.session.flush()
    # 或者使用下面的方法
    # del request.session['is_login']
    # del request.session['user_id']
    # del request.session['user_name']
    return redirect("index")


# 布置作业
def mission(request):
    try:
        user = User.objects.get(id=request.session['user_id'])
    except:
        return render(request,'user/tips.html',context={"tips":"请登录后再进行相关操作！",'url':"/index/"})
    if user.role == 'manager':

        if request.method == 'GET':
            rows = Mission.objects.filter(manager_id=request.session['user_id']).values('id','name','title','c_time','done').order_by('-c_time')

            return render(request, 'user/manager.html',context={'is_join':user.belong,'username':user.name,'rows':rows})

        else:
            name = request.POST.get('name')
            user = User.objects.get(id=request.session['user_id'])

            class_id = user.class_id
            title = request.POST.get('title')
            date = request.POST.get('date')
            num = request.POST.get('num')
            description = request.POST.get('description')
            files = request.FILES.get("files",None)

            # 创建一个文件夹用于存放当前任务的文件夹
            dir = time.strftime('%Y-%m-%d-%H-%M-%S', time.localtime())
            file_folder = BASE_DIR + '/file_db/works/' + dir + name
            mkdir(file_folder)

            mission = Mission(name=name,class_id=class_id,title=title,f_time=date,manager_id=request.session['user_id'],
                              full=num,description=description,example=files,folder=file_folder)
            mission.save()

            return render(request,'user/tips.html',context={"tips":"作业已成功发布啦，快去通知同学们吧！",'url':"/mission/"})
    else:
        return render(request,'user/tips.html',context={"tips":"清醒一点，只有学委才能布置作业！",'url':"/index/"})


#  上传作业
def upload(request):

    if request.method == 'GET':
        # 拿到当前用户登录信息
        user = User.objects.get(id=request.session['user_id'])
        # 判断当前用户是否加入班级
        if user.belong:
            # missions_front
            class_id = user.class_id
            missions = list(Mission.objects.filter(class_id=class_id,finished=0).values('name','title','id'))
            # print(missions)

            # 个人所有作业
            rows = Work.objects.filter(author_id=request.session['user_id']).values('id','name','c_time','onload')

            return render(request,'user/upload.html',context={'is_join':user.belong,'username':user.name,'missions':missions,'rows':rows})
        else:
            return render(request,'user/upload.html')
    else:
        user = User.objects.get(id=request.session['user_id'])
        name = request.POST.get('title')
        mission_id = request.POST.get('mission_id')
        # 拿到任务的文件路径
        folder = Mission.objects.get(id=mission_id)
        # print("______________________")
        # print(folder.folder)

        files = request.FILES.get('files',None)
        desc = request.POST.get('desc')
        author_id = request.session['user_id']

        # print(files.size)
        # 判断文件
        if not files:   #如果上传内容为空
            return render(request, 'user/manager.html', context={'tips': "请选择文件！"})

        else:
            if files.size > 104857600:
                return render(request, 'user/manager.html', context={'tips': "文件超过10M，无法上传，请你谅解，试试QQ邮箱吧^_^"})
                # print(files.size)
            else:

                work = Work(name=name,author_id=author_id,mission_id=mission_id,description=desc, files=files,
                                  class_id=user.class_id, onload=1,folder=folder.folder)
                work.save()

                # mission中done+1
                new_done = Mission.objects.get(id=mission_id).done + 1
                Mission.objects.filter(id=mission_id).update(done = new_done)

                return render(request,'user/tips.html',context={"tips":"作业已成功提交！",'url':"/upload/"})



# 所有班级
def classes(request):

    if request.method == 'GET':
        rows = Classes.objects.values('id','name','c_time','manager','size')
        # print(rows)
        return render(request,'user/classes.html',context={'rows':rows})
    else:
        try:
            user_id = request.session['user_id']
            # 加入班级
            class_id = request.POST.get("class_id")
            class_name = Classes.objects.get(id=class_id).name
            User.objects.filter(id=user_id).update(belong=class_name, class_id=class_id)
            rows = Classes.objects.values('id', 'name', 'c_time', 'manager', 'size')
            return render(request, 'user/classes.html', context={'tips': "加入班级成功！", 'rows': rows})
        except:
            return redirect(reverse('login'))


# 文件下载页面
def download(request):
    id = request.GET.get('id')

    mission = Mission.objects.get(id=id)

    # 文件夹路径
    folder = mission.folder

    # print(folder)
    # print(BASE_DIR)
    base = os.path.join(BASE_DIR,'file_db','works')
    # print(base)
    new_folder = folder.replace(base+'/','')+'.zip'
    # print(new_folder)

    file_news = folder+'.zip'  # 要压缩的文件名

    z = zipfile.ZipFile(file_news,'w',zipfile.ZIP_DEFLATED)
    for dirpath, dirnames, filenames in os.walk(folder):
        fpath = dirpath.replace(folder, '')  # 这一句很重要，不replace的话，就从根目录开始复制
        fpath = fpath and fpath + os.sep or ''  # 这句话理解我也点郁闷，实现当前文件夹以及包含的所有文件的压缩
        for filename in filenames:
            z.write(os.path.join(dirpath, filename), fpath + filename)
    z.close()

    response = StreamingHttpResponse(file_iterator(file_news))
    response['Content-Type'] = 'application/zip'
    response['Content-Disposition'] = 'attachment;filename="%s"' % (urlquote(new_folder))

    # response["Content-Disposition"] = "attachment; filename={0}{1}".format(name.encode('utf8'))

    return response

# 迭代器下载
def file_iterator(file_name, chunk_size=512):
    with open(file_name, 'rb') as f:
        while True:
            c = f.read(chunk_size)
            if c:
                yield c
            else:
                break


# 定义一个类获取当前时间并创建以时间为名的目录
def mkdir(path):

    folder = os.path.exists(path)
    if not folder:
        os.makedirs(path)

# 创建班级

def create_class(request):
    try:
        user = User.objects.get(id=request.session['user_id'])
    except:
        return render(request,'user/tips.html',context={"tips":"请登录后再进行相关操作！",'url':"/index/"})

    if user.role == 'manager':
        if request.method == 'GET':
            return render(request,'user/create_class.html')
        else:
            name = request.POST.get('name')
            code = request.POST.get('code')
            manager_name = request.POST.get('manager_name')
            num = request.POST.get('num')
            desc = request.POST.get('desc')

            new_class = Classes(name=name,class_code=code,manager=manager_name,size=num,description=desc)
            new_class.save()

            User.objects.filter(id=request.session['user_id']).update(belong=name,class_id=new_class.id)
            return render(request,'user/tips.html',context={"tips":"添加班级成功！",'url':"/mission/"})
    else:
        return render(request,'user/tips.html',context={"tips":"清醒一点，只有学委才能创建班级！",'url':"/index/"})









import requests
from bs4 import BeautifulSoup

def dbview(request):
    score = []
    title = []
    for i in range(10):
        num = i*25
        url = "https://movie.douban.com/top250?start=%d&filter=" % num

        con = requests.get(url).content.decode()

        soup = BeautifulSoup(con)

        ul = soup.find(class_="grid_view")

        infos = ul.find_all(class_="info")

        for info in infos:

            title.append(info.find(class_='title').text)

            score.append(info.find(class_='rating_num').text)

    # print(title,score)

    return render(request,'db250.html',context={'score':score,'title':title})


# print(infos)













