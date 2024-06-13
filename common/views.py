from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
from datetime import datetime
import time
# Create your views here.

from .models import *
import json

register_lock_table = {}


def home(request):
    return HttpResponse("Welcome to the Ocean Bigdata Management System")


def dispatcher(request):
    if request.method == 'GET':
        # GET 代表查询
        request.params = request.GET

    elif request.method in ['POST', 'PUT', 'DELETE']:
        # POST 代表添加 PUT 代表修改 DELETE代表删除
        # request.params = json.loads(request.body)
        request.params = request.POST

    # 要求在传入的json数据中 包含一个action数据项
    action = request.params['action']
    # 在返回结果中若ret返回值为0 表示错误信息 若ret返回值为1 表示正确信息
    if action == 'search_IdentityInfo':
        return search_IdentityInfo(request)
    elif action == "add_IdentityInfo":
        return add_IdentityInfo(request)
    elif action == "search_QueryAssist":
        return search_QueryAssist(request)
    elif action == "update_QueryAssist":
        return update_QueryAssist(request)
    elif action == "search_Patient":
        return search_Patient(request)
    elif action == "add_Patient":
        return add_Patient(request)
    elif action == "update_Patient":
        return update_Patient(request)
    elif action == "search_Doctor":
        return search_Doctor(request)
    elif action == "update_Doctor":
        return update_Doctor(request)
    elif action == "search_Medicine":
        return search_Medicine(request)
    elif action == "search_Score":
        return search_Score(request)
    elif action == "add_Score":
        return add_Score(request)
    elif action == "search_Comment":
        return search_Comment(request)
    elif action == "add_Comment":
        return add_Comment(request)
    elif action == "search_Current_Register":
        return search_Current_Register(request)
    elif action == "add_Current_Register":
        return add_Current_Register(request)
    elif action == "update_Current_Register":
        return update_Current_Register(request)
    elif action == "search_Register":
        return search_Register(request)
    elif action == "add_Register":
        return add_Register(request)
    elif action == "search_Communication":
        return search_Communication(request)
    elif action == "add_Communication":
        return add_Communication(request)
    elif action == "del_Communication":
        return del_Communication(request)
    elif action == "search_Prescription":
        return search_Prescription(request)
    elif action == "add_Prescription":
        return add_Prescription(request)
    elif action == "write_log":
        return write_log(request)
    else:
        return JsonResponse({'ret': 0, 'msg': '不支持该类型http请求'})


'''
    对挂号时每个医生的锁表进行管理
    doc_no: 申请锁的医生账号
    pat_np: 挂号患者账号
    op: 操作类型（读或写） 分别为1 2
    type: 加锁或者释放锁 1 加锁 2 释放锁
    锁分为两种形式：共享锁和排他锁————  共享锁为读锁  排他锁为写锁
    锁表中存储的数据结构 [pat_no, op(锁类型)]
'''


def Lock_Manage(doc_no, pat_no, op, type):
    if type == 2:
        ''' 释放该表的头部位置的锁'''
        while True:
            if register_lock_table[doc_no][0][0] == pat_no and register_lock_table[doc_no][0][1] == op:
                del register_lock_table[doc_no][0]
                break
            time.sleep(0.01)
    elif type == 1:
        ''' 为该操作加锁 其类型可能为共享锁或者排他锁 '''
        ''' 加入读锁 '''
        register_lock_table.setdefault(doc_no, [])
        register_lock_table[doc_no].append([pat_no, op])

        ''' 检查是否会陷入阻塞条件进入等待过程 '''
        while True:
            if op == 1:
                ''' 读锁:其之前不能有写锁即可直接返回 '''
                succ_ret = False
                for i in register_lock_table[doc_no]:
                    if i[0] == pat_no and i[1] == op:
                        succ_ret = True
                        break
                    elif i[1] == 2:
                        break
                if succ_ret:
                    break
            elif op == 2:
                ''' 写锁: 其必须等待锁表之前的锁全部分配才能够返回 '''
                if register_lock_table[doc_no][0][0] == pat_no and register_lock_table[doc_no][0][1] == op:
                    break
            else:
                break
            time.sleep(0.01)


'''
    写入日志文件
    action: write_log
    data: 登陆时间
'''


def write_log(request):
    no = request.params.get('no', None)
    date = request.params.get('date', None)
    try:
        f = open("log.txt", "a")
        f.write(date + ' login ' + no + '\n')
        f.close()
        return JsonResponse({'ret': 1})
    except:
        return JsonResponse({'ret': 0})


'''
    对于改变数据库的情况写入日志文件
'''


def change_log(log_str):
    f = open("log.txt", "a")
    f.write(datetime.now().strftime('%Y-%m-%d %H:%M:%S') + ' ' + log_str + '\n')
    f.close()


def Permission_detect(no_op, perstr):
    if no_op:
        per_res = Permission.objects.filter(p_no=no_op[0], p_depict=perstr)
        if len(list(per_res)) == 0:
            return False
        else:
            return True
    else:
        return False


'''
    根据输入的身份属于、编号 返回其姓名和密码
    注意网址的url必须在/后添加?
    多个参数是?no=300&belong=P   即多个参数间用&连接
    action: search_IdentityInfo
    data: 所要筛选的信息
'''


def search_IdentityInfo(request):

    no_op = request.POST.get('no_op', None)  # 使用 GET 方法获取参数
    print(f"Received no_op: {no_op}")

    if not Permission_detect(no_op, 'search_IdentityInfo'):
        print("Permission denied")
        return JsonResponse({'ret': 0})

    qs = IdentityInfo.objects.values()
    try:
        _belong = request.POST.get('belong', None)  # 使用 GET 方法获取参数
        if _belong:
            qs = qs.filter(belong=_belong)
        _no = request.POST.get('no', None)  # 使用 GET 方法获取参数
        if _no:
            qs = qs.filter(no=_no)
        return JsonResponse({'ret': 1, 'retlist': list(qs)})
    except Exception as e:
        print(f"Error: {e}")
        return JsonResponse({'ret': 0})


'''
    为身份信息表添加数据
    action: add_IdentityInfo
    data: 数据
'''


def add_IdentityInfo(request):
    # 添加权限判断操作
    no_op = request.params.get('no_op', None)
    if not Permission_detect(no_op, 'add_IdentityInfo'):
        return JsonResponse({'ret': 0})
    info = request.params
    try:
        IdentityInfo.objects.create(
            no=info['no'], password=info['password'], belong=info['belong'])
        change_log("add_IdentityInfo " + info['no'] + " " + info['belong'])
        return JsonResponse({'ret': 1})
    except:
        return JsonResponse({'ret': 0})


'''
    根据输入的咨询人员编号返回咨询人员的姓名和在线状态
    action: search_QueryAssist
    data: 所要筛选的信息
'''


def search_QueryAssist(request):
    # 添加权限判断操作
    no_op = request.params.get('no_op', None)
    if not Permission_detect(no_op, 'search_QueryAssist'):
        return JsonResponse({'ret': 0})
    qs = QueryAssist.objects.values()
    _no = request.params.get('no', None)
    if _no:
        qs = qs.filter(no=_no)
    return JsonResponse({'ret': 1, 'retlist': list(qs)})


'''
    对咨询人员的在线状态进行修改
    action: update_QueryAssist
    data: 新数据
'''


def update_QueryAssist(request):
    # 添加权限判断操作
    no_op = request.params.get('no_op', None)
    if not Permission_detect(no_op, 'update_QueryAssist'):
        return JsonResponse({'ret': 0})
    info = request.params
    query_no = info['no']
    try:
        query = QueryAssist.objects.get(no_id=query_no)
        if 'name' in info:
            query.name = info['name']
        if 'state' in info:
            query.state = info['state']
        # !!! 不能忘记save
        query.save()
        change_log("update_QueryAssist " + info['no'] + ' ' + info['state'])
        return JsonResponse({'ret': 1})
    except:
        return JsonResponse({'ret': 0, 'msg': f'no为{query_no}的服务人员不存在'})


'''
    根据输入的患者编号返回患者信息
    action: search_Patient
    data: 所要筛选的信息
'''


def search_Patient(request):
    # 添加权限判断操作
    no_op = request.params.get('no_op', None)
    if not Permission_detect(no_op, 'search_Patient'):
        return JsonResponse({'ret': 0})
    qs = Visitor.objects.values()
    _no = request.params.get('no', None)
    if _no:
        qs = qs.filter(no=_no)
    return JsonResponse({'ret': 1, 'retlist': list(qs)})


'''
    添加患者
    action: add_Patient
    data: 添加的数据
'''


def add_Patient(request):
    # 添加权限判断操作
    no_op = request.params.get('no_op', None)
    if not Permission_detect(no_op, 'add_Patient'):
        return JsonResponse({'ret': 0})
    info = request.params
    try:
        Visitor.objects.create(no_id=info['no'], name=info['name'], v_age=info['v_age'],
                               v_gender=info['v_gender'], v_aim=info['v_aim'])
        change_log('add_Patient ' + info['no'] + ' ' + info['name'] +
                   ' ' + info['v_age'] + ' ' + info['v_gender'])
        return JsonResponse({'ret': 1})
    except:
        return JsonResponse({'ret': 0})


'''
    对患者个人信息进行修改
    action: update_Patient
    data: 新数据
'''


def update_Patient(request):
    # 添加权限判断操作
    no_op = request.params.get('no_op', None)
    if not Permission_detect(no_op, 'update_Patient'):
        return JsonResponse({'ret': 0})
    info = request.params
    update_no = info['no']
    try:
        _patient = Visitor.objects.get(no_id=update_no)
        if 'name' in info:
            _patient.name = info['name']
        if 'v_age' in info:
            _patient.v_age = info['v_age']
        if 'v_gender' in info:
            _patient.v_gender = info['v_gender']
        if 'v_aim' in info:
            _patient.v_aim = info['v_aim']
        # !!! 不能忘记save
        _patient.save()
        change_log('update_Patient ' + info['no'] + ' ' +
                   info['name'] + ' ' + info['v_age'] + ' ' + info['v_gender'])
        return JsonResponse({'ret': 1})
    except:
        return JsonResponse({'ret': 0, 'msg': '患者信息修改失败'})


'''
    根据输入的医生编号返回医生信息
    action: search_Doctor
    data: 所要筛选的信息
    可根据账号或者科室信息进行查询
'''


def search_Doctor(request):
    # 添加权限判断操作
    no_op = request.params.get('no_op', None)
    if not Permission_detect(no_op, 'search_Doctor'):
        return JsonResponse({'ret': 0})
    qs = Staff.objects.values()
    _no = request.params.get('no', None)
    if _no:
        qs = qs.filter(no=_no)
    _depart = request.params.get('s_depart', None)
    if _depart:
        qs = qs.filter(s_depart=_depart)
    return JsonResponse({'ret': 1, 'retlist': list(qs)})


'''
    更新医生信息
    action: update_Doctor
    data: 所要更新的医生信息
'''


def update_Doctor(request):
    # 添加权限判断操作
    no_op = request.params.get('no_op', None)
    if not Permission_detect(no_op, 'update_Doctor'):
        return JsonResponse({'ret': 0})
    info = request.params
    doc_no = info['no']
    try:
        _doctor = Staff.objects.get(no_id=doc_no)
        if 'name' in info:
            _doctor.name = info['name']
        if 's_profession' in info:
            _doctor.s_profession = info['s_profession']
        if 's_depart' in info:
            _doctor.s_depart = info['s_depart']
        if 's_index' in info:
            _doctor.s_index = info['s_index']
        if 's_time_begin' in info:
            _doctor.s_time_begin = info['s_time_begin']
        if 's_time_end' in info:
            _doctor.s_time_end = info['s_time_end']
        # !!! 不能忘记save
        _doctor.save()
        if 's_index' in info:
            change_log('update_Doctor ' + info['no'] + ' ' + info['s_index'])
        else:
            change_log('update_Doctor ' + info['no'] + ' ' +
                       info['s_time_begin'] + ' ' + info['s_time_end'])
        return JsonResponse({'ret': 1})
    except:
        return JsonResponse({'ret': 0, 'msg': f'no为{doc_no}的医生信息不存在'})


'''
    根据输入的药物名称，返回药物信息
    action: search_Medicine
    data: 所要筛选的信息
'''


def search_Medicine(request):
    # 添加权限判断操作
    no_op = request.params.get('no_op', None)
    if not Permission_detect(no_op, 'search_Medicine'):
        return JsonResponse({'ret': 0})
    qs = Dataset.objects.values()
    _mname = request.params.get('d_name', None)
    if _mname:
        qs = qs.filter(d_name=_mname)
    return JsonResponse({'ret': 1, 'retlist': list(qs)})


'''
    根据输入的医生编号，返回其评分信息
    action: search_Score
    data: 筛选信息
'''


def search_Score(request):
    # 添加权限判断操作
    no_op = request.params.get('no_op', None)
    if not Permission_detect(no_op, 'search_Score'):
        return JsonResponse({'ret': 0})
    qs = Score.objects.values()
    _no = request.params.get('no', None)
    if _no:
        qs = qs.filter(no=_no)
    return JsonResponse({'ret': 1, 'retlist': list(qs)})


'''
    增加评分信息
    action: add_Score
    data: 所要新增的评分信息  其中f_time: 年-月-日T时-分-秒-Z
'''


def add_Score(request):
    # 添加权限判断操作
    no_op = request.params.get('no_op', None)
    if not Permission_detect(no_op, 'add_Score'):
        return JsonResponse({'ret': 0})
    info = request.params
    try:
        Score.objects.create(f_no=info['f_no'], f_score=info['f_score'],
                             f_time=info['f_time'], no_id=info['no'])
        change_log('add_Score ' + info['f_score'] + ' ' + info['no'])
        return JsonResponse({'ret': 1})
    except:
        return JsonResponse({'ret': 0})


'''
    根据输入的医生编号，返回其意见信息
    action: search_Comment
    data: 所要筛选信息
'''


def search_Comment(request):
    # 添加权限判断操作
    no_op = request.params.get('no_op', None)
    if not Permission_detect(no_op, 'search_Comment'):
        return JsonResponse({'ret': 0})
    qs = Comment.objects.values()
    _no = request.params.get('no', None)
    if _no:
        qs = qs.filter(no=_no)
    return JsonResponse({'ret': 1, 'retlist': list(qs)})


'''
    增加意见信息
    action: add_Comment
    data: 所要新增的意见信息
'''


def add_Comment(request):
    # 添加权限判断操作
    no_op = request.params.get('no_op', None)
    if not Permission_detect(no_op, 'add_Comment'):
        return JsonResponse({'ret': 0})
    info = request.params
    try:
        Comment.objects.create(cc_no=info['cc_no'], cc_content=info['cc_content'],
                               cc_time=info['cc_time'], no_id=info['no'])
        change_log('add_Comment ' + info['cc_content'] + ' ' + info['no'])
        return JsonResponse({'ret': 1})
    except:
        return JsonResponse({'ret': 0})


'''
    根据当天日期和医生编号，返回当前到号信息
    action: search_Current_Register
    data: 筛选信息
'''


def search_Current_Register(request):
    # 添加权限判断操作
    no_op = request.params.get('no_op', None)
    if not Permission_detect(no_op, 'search_Current_Register'):
        return JsonResponse({'ret': 0})
    qs = Current_Apply.objects.values()
    _rnodoctor = request.params.get('a_no_staff', None)
    if _rnodoctor:
        qs = qs.filter(a_no_staff=_rnodoctor)
    _rdate = request.params.get('a_date', None)
    if _rdate:
        qs = qs.filter(a_date=_rdate)
    return JsonResponse({'ret': 1, 'retlist': list(qs)})


'''
    新增当前叫号信息 主要用于初始化操作
    action: add_Current_Register
    data: 新增信息
'''


def add_Current_Register(request):
    # 添加权限判断操作
    no_op = request.params.get('no_op', None)
    if not Permission_detect(no_op, 'add_Current_Register'):
        return JsonResponse({'ret': 0})
    info = request.params
    try:
        Current_Apply.objects.create(a_index=info['a_index'], a_date=info['a_date'],
                                     a_no_staff_id=info['a_no_staff'])
        change_log('add_Current_Register ' +
                   info['a_no_staff'] + ' ' + info['a_date'] + ' ' + info['a_index'])
        return JsonResponse({'ret': 1})
    except:
        return JsonResponse({'ret': 0})


'''
    根据医生编号 更新当前叫号
    action: update_Current_Register
    data: 更新信息
'''


def update_Current_Register(request):
    # 添加权限判断操作
    no_op = request.params.get('no_op', None)
    if not Permission_detect(no_op, 'update_Current_Register'):
        return JsonResponse({'ret': 0})
    info = request.params
    _doctor = info['a_no_staff']
    try:
        current_reg = Current_Apply.objects.get(
            a_no_staff_id=_doctor, a_date=info['a_date'])
        if 'a_index' in info:
            current_reg.a_index = info['a_index']
        # !!! 不能忘记save
        current_reg.save()
        change_log('update_Current_Register ' +
                   info['a_no_staff'] + ' ' + info['a_date'] + ' ' + info['a_index'])
        return JsonResponse({'ret': 1})
    except:
        return JsonResponse({'ret': 0, 'msg': f'no为{_doctor}的医生不存在'})


'''
    查询当前挂号信息 患者根据自身编号 挂号医生编号 以及挂号日期 查询挂号号码
    action: search_Register
    data: 筛选信息
'''


def search_Register(request):
    # 添加权限判断操作
    no_op = request.params.get('no_op', None)
    if not Permission_detect(no_op, 'search_Register'):
        return JsonResponse({'ret': 0})
    _rdate = request.params.get('a_date', None)
    _rdoctor = request.params.get('a_no_staff', None)
    _rpatient = request.params.get('a_no_visitor', None)
    _rindex = request.params.get('a_index', None)
    ''' 为挂号加读锁 '''
    Lock_Manage(_rdoctor, no_op, 1, 1)
    qs = Apply.objects.values()
    ''' 解锁 '''
    Lock_Manage(_rdoctor, no_op, 1, 2)
    if _rdate:
        qs = qs.filter(a_date=_rdate)
    if _rdoctor:
        qs = qs.filter(a_no_staff_id=_rdoctor)
    if _rpatient:
        qs = qs.filter(a_no_visitor_id=_rpatient)
    if _rindex:
        qs = qs.filter(a_index=_rindex)
    return JsonResponse({'ret': 1, 'retlist': list(qs)})


'''
    新增挂号信息 根据当天日期 医生编号 患者编号 新增挂号号码
    action: add_Register
    data: 新增
    !!! 多对多关系插入方式不同
'''


def add_Register(request):
    # 添加权限判断操作
    no_op = request.params.get('no_op', None)
    if not Permission_detect(no_op, 'add_Register'):
        return JsonResponse({'ret': 0})
    info = request.params
    try:
        ''' 为挂号加写锁 '''
        Lock_Manage(info['a_no_staff'], info['a_no_visitor'], 2, 1)
        Apply.objects.create(a_index=info['a_index'], a_date=info['a_date'],
                             a_no_staff_id=info['a_no_staff'], a_no_visitor_id=info['a_no_visitor'])
        ''' 解锁 '''
        Lock_Manage(info['a_no_staff'], info['a_no_visitor'], 2, 2)
        change_log('add_Register ' + info['a_no_staff'] + ' ' + info['a_no_visitor'] + ' ' + info['a_date']
                   + ' ' + info['a_index'])
        return JsonResponse({'ret': 1})
    except:
        return JsonResponse({'ret': 0})


'''
    查询当前聊天信息  根据发送者编号 接收者编号 发送信息时间 查看信息内容
    action: search_Communication
    data: 筛选信息
'''


def search_Communication(request):
    # 添加权限判断操作
    no_op = request.params.get('no_op', None)
    if not Permission_detect(no_op, 'search_Communication'):
        return JsonResponse({'ret': 0})
    qs = Communication.objects.values()
    _csno = request.params.get('cs_no', None)
    if _csno:
        qs = qs.filter(cs_no=_csno)
    _crno = request.params.get('cr_no', None)
    if _crno:
        qs = qs.filter(cr_no=_crno)
    _cstime = request.params.get('cs_time', None)
    if _cstime:
        qs = qs.filter(cs_time=_cstime)
    return JsonResponse({'ret': 1, 'retlist': list(qs)})


'''
    增加聊天信息
    action: add_Communication
    data: 增加信息
'''


def add_Communication(request):
    # 添加权限判断操作
    no_op = request.params.get('no_op', None)
    if not Permission_detect(no_op, 'add_Communication'):
        return JsonResponse({'ret': 0})
    info = request.params
    try:
        Communication.objects.create(cs_time=info['cs_time'], content=info['content'],
                                     cs_no_id=info['cs_no'], cr_no_id=info['cr_no'])
        change_log('add_Communication ' +
                   info['cs_no'] + ' ' + info['cr_no'] + ' ' + info['content'])
        return JsonResponse({'ret': 1})
    except:
        return JsonResponse({'ret': 0})


'''
    删除聊天信息
    action: del_Communication
    data: 删除信息  给出发送者编号 接收者编号 发送时间 
'''


def del_Communication(request):
    # 添加权限判断操作
    no_op = request.params.get('no_op', None)
    if not Permission_detect(no_op, 'del_Communication'):
        return JsonResponse({'ret': 0})
    info = request.params
    del_crno = info['cr_no']
    del_csno = info['cs_no']
    del_time = info['cs_time']

    comm = Communication.objects.filter(
        cr_no=del_crno, cs_no=del_csno, cs_time=del_time)
    try:
        comm.delete()
        change_log('del_Communication ' + info['cs_no'] + ' ' + info['cr_no'])
        return JsonResponse({'ret': 1})
    except:
        return JsonResponse({'ret': 0, 'msg': f'聊天信息删除失败'})


'''
    根据挂号日期，挂号号码，患者编号 查询药物数量和药物信息
    action: search_Prescription
    data: 筛选信息
'''


def search_Prescription(request):
    # 添加权限判断操作
    no_op = request.params.get('no_op', None)
    if not Permission_detect(no_op, 'search_Prescription'):
        return JsonResponse({'ret': 0})
    qs = Authorization.objects.values()
    _prindex = request.params.get('Au_index', None)
    if _prindex:
        qs = qs.filter(Au_index=_prindex)
    _prdate = request.params.get('Au_date', None)
    if _prdate:
        qs = qs.filter(Au_date=_prdate)
    _prno = request.params.get('Au_no', None)
    if _prno:
        qs = qs.filter(Au_no=_prno)
    return JsonResponse({'ret': 1, 'retlist': list(qs)})


'''
    增加新的处方信息
    action: add_Prescription
    data: 新的处方信息
'''


def add_Prescription(request):
    # 添加权限判断操作
    no_op = request.params.get('no_op', None)
    if not Permission_detect(no_op, 'add_Prescription'):
        return JsonResponse({'ret': 0})
    info = request.params
    _prno = Visitor.objects.get(no_id=info['Au_no'])
    reg = Authorization.objects.create(Au_num=info['Au_num'], Au_index=info['Au_index'],
                                       Au_date=info['Au_date'], d_name_id=info['d_name'])
    try:
        reg.Au_no.add(_prno)
        change_log('add_Prescription ' + info['Au_no'] + ' ' + info['Au_index'] + ' ' +
                   info['d_name'] + ' ' + info['Au_num'])
        return JsonResponse({'ret': 1})
    except:
        return JsonResponse({'ret': 0})
