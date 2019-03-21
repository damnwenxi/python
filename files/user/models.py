from django.db import models
# Create your models here.

def get_folder(instance,filename):
    return '{0}/{1}'.format(instance.folder, filename)

# 用户信息表
class User(models.Model):

    name = models.CharField(max_length=100,null=False,unique=True)
    password = models.CharField(max_length=256,null=False)
    email = models.EmailField(null=True)
    phone = models.CharField(max_length=11,null=True)
    # 属于哪个班级
    belong = models.CharField(max_length=100,null=True)
    class_id = models.CharField(max_length=100,null=True)
    ip = models.CharField(max_length=20,null=True)
    gender = models.CharField(max_length=10, null=True)
    # 角色
    role = models.CharField(max_length=10,null=True,default="student")
    # head = models.ImageField(null=True)
    c_time = models.DateTimeField(auto_now_add=True)
    # 自我介绍
    description = models.TextField(null=True)


# 班级信息表
class Classes(models.Model):

    name = models.CharField(max_length=100, null=False, unique=True)
    c_time = models.DateTimeField(auto_now_add=True)
    # 学委
    manager = models.CharField(max_length=100, null=False)
    # 班级人数
    size = models.IntegerField(default=0,null=True)
    # 班级描述
    description = models.TextField(null=True)
    # 班级码
    class_code = models.CharField(max_length=6,null=False,unique=True)


# 作业任务表
class Mission(models.Model):

    # 任务目录
    folder = models.CharField(max_length=255,null=True,unique=True)
    # 作业名称
    name = models.CharField(max_length=100,null=False,unique=False)
    # title 命名格式
    title = models.CharField(max_length=100,null=True,unique=False)
    # 创建时间
    c_time = models.DateTimeField(auto_now_add=True)
    # 截止时间
    f_time = models.DateTimeField(null=True)
    # 学委id
    manager_id = models.CharField(max_length=100, null=False)
    # 总人数
    full = models.IntegerField(default=0,null=True)
    # 已完成人数
    done = models.IntegerField(default=0,null=True)
    # 作业描述 要求
    description = models.TextField(null=True)
    # 作业模版 存放在file_db/missions中
    example = models.FileField(null=True,upload_to=get_folder)
    # 班级
    class_id = models.CharField(max_length=100,null=False)
    # 是否完成
    finished = models.CharField(max_length=1,null=True,default=0)


# 作业表
class Work(models.Model):

    # 文件所在目录
    folder = models.CharField(max_length=255,null=True)
    # 作者id
    author_id = models.CharField(max_length=100,null=False)
    # 作业名称
    name = models.CharField(max_length=100, null=False, unique=False)
    # 创建时间
    c_time = models.DateTimeField(auto_now_add=True)
    # 截止时间
    f_time = models.DateTimeField(null=True)
    # 哪一次作业
    mission_id = models.CharField(max_length=10,null=False)
    # 作业描述 要求
    description = models.TextField(null=True)
    # 作业文件 存放在file_db/works中
    files = models.FileField(null=False,upload_to=get_folder)
    # 是否上传到服务器
    onload = models.CharField(max_length=1,null=False,default=0)
    # 班级
    class_id = models.CharField(max_length=100,null=False)

class Messages(models.Model):
    ip = models.CharField(max_length=100,null=True)
    c_time = models.DateTimeField(auto_now_add=True)
    last_mess = models.TextField(null=True)



