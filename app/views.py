
from django.http import HttpResponse
from app.models import Pport ,Pship,Cost_result,Fuel_rent,Pcargo,Pship_Pport,Budget_result
from django.utils.translation import ugettext as _
from django.forms import widgets as wid  #因为重名，所以起个别名
from django.shortcuts import render,redirect,reverse,HttpResponseRedirect
from django.forms import ModelForm
from django.views.decorators.csrf import csrf_exempt
import json
from django.db.models import Sum

def index(request):
    return render(request,"templete.html")


class PshipList(ModelForm):
    class Meta:
        model = Pship  #对应的Model中的类
        fields = "__all__"      #字段，如果是__all__,就是表示列出所有的字段
        exclude = None          #排除的字段
        help_texts = None       #帮助提示信息

# def show_ship(request):
#     pshiplist = Pship.objects.all()
#     return redirect(hangcheng)

def select_pship(request):
    pship_list = Pship.objects.all()
    pshiplist = Pship.objects.all()
    pportlist = Pport.objects.all().order_by("Pport_order")
    return render(request, 'hangcheng.html', {'pship_list':pship_list,"pportlist" :pportlist,"pshiplist":pshiplist})

def cost_budget_selectship(request):
    fuelrent_list=Fuel_rent.objects.all()
    pshiplist = Pship.objects.all()
    return render(request,"cost_budget.html",{"fuelrentlist":fuelrent_list,"pshiplist":pshiplist})

def total_budget_selectship(request):
    pcargolist=Pcargo.objects.all()
    pshiplist = Pship.objects.all()
    return render(request,"budget_result.html",{"pcargolist":pcargolist,"pshiplist":pshiplist})

#得到编号为id的航次所对应的航程
def hangcheng(request,id):
    pportlist = Pport.objects.filter(Pship_number=id).all()     #查询该航次经过的所有港口
    pship_portlist=Pship_Pport.objects.filter(Pship_number_id=id).all()[:1]     #bug。。
    hangci=Pship.objects.filter(pk=id).first()
    return render(request, 'hangcheng.html', {'pship_list':pship_list,"pportlist" :pportlist,"pship_portlist":pship_portlist,'hangci':hangci.id})

def hangcheng_del(request,id):
    obj = Pship_Pport.objects.filter(pk=id).first()
    hangci=Pship.objects.filter(Pship_number=obj.Pship_number).first()
    obj.delete()

    return redirect(hangcheng,hangci.id)




def hangcheng_edit(request,id):
    obj = Pship_Pport.objects.filter(pk=id).first()
    if not obj:
        return redirect(hangcheng)
    if request.method == "GET":
        hangchenglist = Pship_Hangcheng(instance=obj)
        return render(request,'hangcheng_edit.html',{'hangchenglist':hangchenglist})
    else:
        hangchenglist = Pship_Hangcheng(request.POST,instance=obj)
        if hangchenglist.is_valid():
            hangchenglist.save()
        return reverse(hangcheng)

def pship_list(request):
    pship_list = Pship.objects.all()
    return render(request,'pship.html',{"pship_list":pship_list})

def pship_add(request):
    if request.method == 'GET':
        pship_list = PshipList()
        return render(request,'pship_add.html',{'pship_list':pship_list})
    if request.method == 'POST':
        pship=PshipList(request.POST)
        if pship.is_valid():
            pship.save()
            return redirect("pship_list")
        else:
            pship_list = PshipList()
            return render(request,'pship_add.html',{'pship_list':pship_list,'pship_errors':"该航次已经存在！"})

def pship_edit(request,id):
    obj = Pship.objects.filter(id=id).first()
    if not obj:
        return redirect(hangcheng)
    if request.method == "GET":
        pshiplist = PshipList(instance=obj)
        return render(request,'pship_edit.html',{'pshiplist':pshiplist})
    else:
        pshiplist = PshipList(request.POST,instance=obj)
        if pshiplist.is_valid():
            pshiplist.save()
            return  redirect(pship_list)
        else:
            pshiplist = PshipList(instance=obj)
            return render(request,'pship_add.html',{'pship_list':pshiplist,'pship_errors':"该航次已经存在！"})

def pship_del(request,id):
    obj = Pship.objects.filter(pk=id).first()
    obj.delete()
    return redirect('pship_list')



class PportList(ModelForm):

    class Meta:
        model = Pport  #对应的Model中的类
        fields = "__all__"      #字段，如果是__all__,就是表示列出所有的字段
        exclude = ('Pship_number' ,'Pport_order')         #排除的字段
        help_texts = None       #帮助提示信息
        #error_messages用法：
        # error_messages = {
        #     'name':{'required':"用户名不能为空",},
        #     'age':{'required':"年龄不能为空",},
        # }
        # widgets = {
        #     'Pport_eta': wid.DateTimeInput(attrs={'type':"datetime-local" ,"class":"col-md-9",),
        #     'Pport_etd': wid.DateTimeInput(attrs={'type':"datetime-local" ,"class":"col-md-9","pattern":"yyyy-MM-dd HH:mm:ss"}),
        #
        # }

# def pportlist(request):
#     pportlist = Pport.objects.all()
#     return render(request, 'pportlist.html', {'pportlist':pportlist})



def pport_add(request,id):
    hangci=Pship.objects.filter(pk=id).first()
    if request.method == 'GET':
        pportlist = PportList()
        return render(request,'pport_add.html',{'pportlist':pportlist,'hangci':hangci.Pship_number})
    if request.method == 'POST':
        pportlist=PportList(request.POST)
        print(hangci.Pship_number)
        count=Pport.objects.filter(Pship_number=hangci.id).count()
        print(count)
        if pportlist.is_valid():
            instance=pportlist.save(commit=False)
            instance.Pship_number=hangci
            instance.Pport_order=count+1
            pportlist.save()
        else:
            print(pportlist.errors)
    return redirect(hangcheng,id)

def pport_edit(request,id):
    obj = Pport.objects.filter(pk=id).first()
    hangci=Pship.objects.filter(Pship_number=obj.Pship_number).first()

    if not obj:
        return redirect(hangcheng,id)
    if request.method == "GET":
        pportlist = PportList(instance=obj)
        return render(request,'pport_edit.html',{'pportlist':pportlist,'hangci':hangci.Pship_number})
    else:
        pportlist = PportList(request.POST,instance=obj)
        if pportlist.is_valid():
            instance=pportlist.save(commit=False)
            instance.Pship_number=hangci
            pportlist.save()
    return  redirect(hangcheng,hangci.id)

def pport_del(request,id):
    obj = Pport.objects.filter(pk=id).first()
    obj.delete()
    hangci=Pship.objects.filter(Pship_number=obj.Pship_number).first()
    return redirect(hangcheng,hangci.id)



class Fuel_rentList(ModelForm):

    class Meta:
        model = Fuel_rent  #对应的Model中的类
        fields = "__all__"      #字段，如果是__all__,就是表示列出所有的字段
        exclude = ('Pship_number' ,)           #排除的字段
        help_texts = None       #帮助提示信息


#给某个航次添加燃油
def fuelrent_add(request,id):
    hangci=Pship.objects.filter(pk=id).first()
    if request.method == 'GET':
        fuelrentlist = Fuel_rentList()
        return render(request, 'fuelrent_add.html', {'fuelrentlist':fuelrentlist,'hangci':hangci.Pship_number})
    if request.method == 'POST':
        fuelrentlist=Fuel_rentList(request.POST)
        if fuelrentlist.is_valid():
            instance=fuelrentlist.save(commit=False)
            instance.Pship_number=hangci
            fuelrentlist.save()
        return redirect(cost_budget,hangci.id)


def fuelrent_edit(request,id):
    obj = Fuel_rent.objects.filter(pk=id).first()
    hangci=Pship.objects.filter(Pship_number=obj.Pship_number).first()
    if not obj:
        return redirect(cost_budget,hangci.id)
    if request.method == "GET":
        fuelrent_list = Fuel_rentList(instance=obj)
        return render(request,'fuelrent_edit.html',{'fuelrent_list':fuelrent_list,'hangci':hangci})
    else:
        fuelrent_list = Fuel_rentList(request.POST,instance=obj)
        if fuelrent_list.is_valid():
            instance=fuelrent_list.save(commit=False)
            instance.Pship_number=hangci
            fuelrent_list.save()
        return redirect(cost_budget,hangci.id)

def fuelrent_delete(request,id):
    obj = Fuel_rent.objects.filter(pk=id).first()
    hangci=Pship.objects.filter(Pship_number=obj.Pship_number).first()
    obj.delete()
    return redirect(cost_budget,hangci.id)



class PcargoList(ModelForm):

    class Meta:
        model = Pcargo  #对应的Model中的类
        fields = "__all__"      #字段，如果是__all__,就是表示列出所有的字段
        exclude = ('Pship_number' ,)           #排除的字段
        help_texts = None       #帮助提示信息


#为某航次添加货物
def pcargo_add(request,id):
    hangci=Pship.objects.filter(pk=id).first()
    if request.method == 'GET':
        pcargolist = PcargoList()
        return render(request, 'pcargo_add.html', {'pcargolist':pcargolist,'hangci':hangci})
    if request.method == 'POST':
        pcargolist=PcargoList(request.POST)
        if pcargolist.is_valid():
            instance=pcargolist.save(commit=False)
            instance.Pship_number=hangci
            pcargolist.save()
            return redirect(budget_result,hangci.id)
        else:
            return redirect(pcargo_add,hangci.id)



def pcargo_edit(request,id):
    obj = Pcargo.objects.filter(pk=id).first()
    hangci=Pship.objects.filter(Pship_number=obj.Pship_number).first()
    if not obj:
        return redirect(budget_result,id)
    if request.method == "GET":
        pcargolist = PcargoList(instance=obj)
        return render(request,'pcargo_edit.html',{'pcargolist':pcargolist,'hangci':hangci.Pship_number})
    else:
        pcargolist = PcargoList(request.POST,instance=obj)
        if pcargolist.is_valid():
            instance=pcargolist.save(commit=False)
            instance.Pship_number=hangci
            pcargolist.save()
        return redirect(budget_result,hangci.id)


def pcargo_del(request,id):
    obj = Pcargo.objects.filter(pk=id).first()
    hangci=Pship.objects.filter(Pship_number=obj.Pship_number).first()
    obj.delete()
    return redirect(budget_result,hangci.id)


#某个航次的成本预算
def cost_budget(request,id):
    hangci=Pship.objects.filter(pk=id).first()
    fuelrent_list=Fuel_rent.objects.filter(Pship_number=hangci.id).all()
    can_add=True if len(fuelrent_list)==0 else False
    costresultlist=Cost_result.objects.filter(Pship_number=hangci.id).all()
    return render(request,"cost_budget.html",{"fuelrentlist":fuelrent_list,"costresultlist":costresultlist,'hangci':hangci,'pship_id':hangci.id,'can_add':can_add})
def budgetresult_del(request,id):
    obj = Budget_result.objects.filter(pk=id).first()
    hangci=Pship.objects.filter(Pship_number=obj.Pship_number).first()
    obj.delete()

    return redirect(budget_result,hangci.id)

def cost_del(request,id):
    obj = Cost_result.objects.filter(pk=id).first()
    obj.delete()
    return redirect(cost_budget)



#计算预算成本 包括燃油费 总港口费用 总船舶租金 总成本 每日成本
def cost(request,id):
    #燃油费 （在航消耗量（FO_sea）*总在航时间（Pport_range）*油价（FO_price））+（在港消耗量（FO_port）*总在港时间（Pport_lei_worday）*油价（DO_price））
    hangci=Pship.objects.filter(pk=id).first()
    res=Pship_Pport.objects.filter(Pship_number=hangci.id).first()
    if res:
        pport_range=res.Pport_range      #总在航时间
        pport_lei_worday=res.Pport_lei_worday  #总在港时间
    else:
        pport_range=0
        pport_lei_worday=0
    fo_sea=0
    fo_port=0
    do_price=0
    fo_price=0
    do_sea=0
    do_port=0
    try:        #防止未添加燃油出错
        res=Fuel_rent.objects.filter(Pship_number=hangci).first()
        fo_sea=int(res.FO_sea)   #在航消耗量
        fo_port=int(res.FO_port)   #在港消耗量
        do_sea=int(res.DO_sea)
        fo_price=int(res.FO_price)
        do_price=int(res.DO_price) #油价
        do_port=int(res.DO_port)
    except Exception as e:
        print('没有燃油怎么计算成本呢？')

    sum_fuel=(fo_sea*pport_range*fo_price+fo_port*pport_lei_worday*fo_price)+(do_sea*pport_range*do_price+do_port*pport_lei_worday*do_price)


    #总港口费用
    res=Pport.objects.filter(Pship_number=hangci.id).aggregate(Sum("Pport_cost"))
    print(res)
    try:
        sum_pport_cost=res['Pport_cost__sum'] if res['Pport_cost__sum'] else 0
    except:
        print('港口费用有毛病了')
        sum_pport_cost=0

    #总船舶租金  日租金*总在航在港时间-佣金
    fuel=Fuel_rent.objects.filter(Pship_number=hangci.id).first()
    tem=Pship_Pport.objects.filter(Pship_number=hangci.id).first()
    if fuel:
        sum_day_rent=int(fuel.Day_rent)*int(tem.Pport_lei_worday+tem.Pport_range)-int(fuel.Commission)
    else:
        sum_day_rent=0
    #总船舶费用
    sum_cost=sum_fuel+sum_pport_cost+sum_day_rent

    #每日成本  （燃油费+总港口费用)/总航行时间
    try:
        day_cost=round((sum_fuel+sum_pport_cost)/(pport_range+pport_lei_worday),5)      #小数点后五位
    except:
        day_cost=0


    #这儿应该是某一条船的总预算费用 没有插入 有则更改数据
    # cursor=connection.cursor()
    # sql="insert into app_cost_result(sum_fuel,sum_pport_cost,sum_day_rent,sum_cost,day_cost,pship_num_id) VALUES ({},{},{},{},{},{})".format(sum_fuel,sum_pport_cost,sum_day_rent,sum_cost,day_cost,id)+\
    #     "ON DUPLICATE KEY UPDATE sum_fuel=VALUES(sum_fuel),sum_pport_cost=VALUES(sum_pport_cost),sum_day_rent=VALUES(sum_day_rent),sum_cost=VALUES(sum_cost),day_cost=VALUES(day_cost)"
    # cursor.execute(sql)

    try:
        if not Cost_result.objects.filter(Pship_number=hangci.id).exists():   #没有则插入
            Cost_result.objects.filter(Pship_number=hangci.id).create(
                Pship_number=hangci,
                Sum_fuel=sum_fuel,
                Sum_Pport_cost=sum_pport_cost,
                Sum_day_rent=sum_day_rent,
                Sum_Cost=sum_cost,
                Day_cost=day_cost,
            )
        else:
                Cost_result.objects.filter(Pship_number=hangci.id).update(
                Sum_fuel=sum_fuel,
                Sum_Pport_cost=sum_pport_cost,
                Sum_day_rent=sum_day_rent,
                Sum_Cost=sum_cost,
                Day_cost=day_cost,
            )
    except Exception as e:
        print(e)
        print(u"总预算计算错误")
    return redirect(cost_budget,hangci.id)




class Pship_Hangcheng(ModelForm):
    class Meta:
        model =Pship_Pport   #对应的Model中的类
        fields = "__all__"      #字段，如果是__all__,就是表示列出所有的字段
        exclude = None          #排除的字段
        help_texts = None       #帮助提示信息




#接受前端传回来的顺序 返回列表形式 更改数据库中对应的字段。。
@csrf_exempt
def Get_pport_order(request,id):    #id为航次
    order=''
    try:
        data=json.loads(request.body)
        print(data)
        order=data['xh']
    except Exception as e:
        print('json解析错误')
        print(e)

    sum_range=0     #航程距离
    sum_day=0
    pport_lei_worday=0
    pport_range=0
    id_list=[]
    start_day=0
    end_day=0

    print(order)
    for one in order:
        res=Pport.objects.filter(Pship_number=id).filter(Pport_order=int(one)).first()
        print(1,res)
        try:
            id_list.append(res.id)   #获取港口Id
            sum_range+=int(res.Pport_range)   #航程距离'
            sum_day+=int(res.Pport_leisureday)+int(res.Pport_workday)+int(res.Pport_shipday)   #总航行时间
            pport_lei_worday+=int(res.Pport_leisureday)+int(res.Pport_workday)     #总在港时间
            pport_range+=int(res.Pport_shipday)                 #总在航时间
        except Exception as e:
            print("索引错误")


    #修改开始时间和结束时间
    time_list=[]
    for i in [0,-1]:
        try:
            port=Pport.objects.filter(id=id_list[i]).first()
            time_list.append(port.Pport_eta)
            time_list.append(port.Pport_etd)
        except Exception as e:
            print('没有港口信息')
            import datetime
            time_list=[0,0]     #如果时间有问题设为当前时间
    if time_list!=[0,0]:
        start_day=time_list[0].strftime("%Y-%m-%d %H:%M:%S")
        end_day=time_list[-1].strftime("%Y-%m-%d %H:%M:%S")


    #修改港口的顺序
    tem=[]
    for i,one in enumerate(id_list):
        try:
            Pport.objects.filter(id=one).update(Pport_order=i)
        except Exception as e:
            print("修改顺序错误")


    orde="-".join(tem)
    orde="'"+orde+"'"
    pship=Pship.objects.filter(pk=id).first()
    print("该航次存在么?",Pship_Pport.objects.filter(Pship_number=pship.id).exists())
    if Pship_Pport.objects.filter(Pship_number=id).exists():
        print('该航次已经有信息，正在更新')
        try:
            Pship_Pport.objects.filter(Pship_number=id).update(
                Pship_number=pship.id,
                Pport_order=orde,
                Sum_range=sum_range,
                Sum_day=sum_day,
                Pport_lei_worday=pport_lei_worday,
                Pport_range=pport_range,
                Start_day=start_day,
                End_day=end_day,
            )
        except Exception as e:
            print(u"航程信息错误")
            print(e)
    else:
        print('生成该航次的航程信息')
        try:
            Pship_Pport.objects.create(
                Pship_number=pship,
                Pport_order=orde,
                Sum_range=sum_range,
                Sum_day=sum_day,
                Pport_lei_worday=pport_lei_worday,
                Pport_range=pport_range,
                Start_day=start_day,
                End_day=end_day,
            )
        except Exception as e:
            print(u"航程信息错误")
            print(e)

    return redirect(hangcheng,id)


#某条船的预算结果
#总预算
# 1.总运费收入：货物运费收益（Carriage_revenue）之和
# 2.利润/亏损：总运费收益-总成本（Sum_Cost）
# 3.相当租金水平：(总运费收益-燃油费-总港口费用)/总航行时间
# 4.回扣佣金：
# 5.经纪人佣金：
def budget_result(request,id):
    hangci=Pship.objects.filter(pk=id).first()

    pcargolist=Pcargo.objects.filter(Pship_number=hangci.id).all()
    costresult=Cost_result.objects.filter(Pship_number=hangci.id).first()
    hangchengresult=Pship_Pport.objects.filter(Pship_number=hangci.id).first()


    carriage_revenue=0  #总运费收入
    Profitorloss=0      #利润/亏损
    Equivalent_rent_level=0 #相当租金水平
    Rebate_commission=0 #回扣佣金
    Broker_commission=0 #经纪人佣金

    if pcargolist:
        tem=pcargolist.aggregate(Sum('Carriage_revenue'))  #总运费收入
        carriage_revenue=float(tem['Carriage_revenue__sum'])
    if costresult:
        Profitorloss=carriage_revenue-float(costresult.Sum_Cost)  #利润/亏损

    if hangchengresult:
        try:
            Equivalent_rent_level=round((carriage_revenue-float(costresult.Sum_fuel)-float(costresult.Sum_Pport_cost))/float(hangchengresult.Sum_day),5)  #相当租金水平
        except:
            print("除数不能为0")

    if Budget_result.objects.filter(Pship_number=hangci.id).count()>=1:
        print('总预算已经有信息，正在更新')
        try:
            Budget_result.objects.update(
                Pship_number=hangci,
                Sum_carriage=carriage_revenue,
                Profit_loss=Profitorloss,
                Rent_level=Equivalent_rent_level,
                Huikou_commission_p=Rebate_commission,
                Agent_commission_p= Broker_commission,
            )
        except Exception as e:
            print(u"总预算信息错误")
            print(e)
    else:
        print('生成总预算信息')
        try:
            Budget_result.objects.create(
                Pship_number=hangci,
                Sum_carriage=carriage_revenue,
                Profit_loss=Profitorloss,
                Rent_level=Equivalent_rent_level,
                Huikou_commission_p=Rebate_commission,
                Agent_commission_p= Broker_commission,
            )
        except Exception as e:
            print(u"总预算信息错误")
    budget_resultlist=Budget_result.objects.filter(Pship_number=hangci.id).all()[:1]
    return render(request,"budget_result.html",{"pcargolist":pcargolist,"budget_resultlist":budget_resultlist,'hangci':hangci})

#显示所有航次的具体信息
def all_info(request):
    infolist=[]
    pshiplist=Pship.objects.all()
    for pship in pshiplist:
        tem=[]
        tem.append(pship.Pship_number)  #航次

        #该航次经过的所有港口
        portlist=Pport.objects.filter(Pship_number=pship.id).all().order_by("Pport_order")
        if portlist:    #可能存在航次还没有经过港口
            s=list(map(''.join,list(portlist.values_list("Pport_name"))))
            port='-'.join(s)       #经过港口顺序
        else:
            port='暂无港口信息'
        tem.append(port)

        # #航程信息
        # hangchenginfo=Pship_Pport.objects.filter(Pship_number=pship.id).first()
        # if hangchenginfo:
        #     #总航行距离 总航行时间 总在港时间 总在航时间
        #     hangc=[hangchenginfo.Sum_range,hangchenginfo.Sum_day,hangchenginfo.Pport_lei_worday,hangchenginfo.Pport_range]
        #     tem.extend(hangc)
        # else:
        #     tem.extend([0,0,0,0])

        #燃油信息
        fuellist=Fuel_rent.objects.filter(Pship_number=pship.id).first()
        if fuellist:
            #fo在航消耗量 在港消耗量 do在航 在港
            fuel=[fuellist.FO_sea,fuellist.FO_port,fuellist.DO_sea,fuellist.DO_port]
            tem.extend(fuel)
        else:
            tem.extend([0,0,0,0])

        #成本预算
        costlist=Cost_result.objects.filter(Pship_number=pship.id).first()
        if costlist:
            #燃油费 总港口费用 总船舶租金  总成本  每日成本
            cost=[costlist.Sum_fuel,costlist.Sum_Pport_cost,costlist.Sum_day_rent,costlist.Sum_Cost,costlist.Day_cost]
            tem.extend(cost)
        else:
            tem.extend([0,0,0,0,0])

        #货物信息
        pcargolist=Pcargo.objects.filter(Pship_number=pship.id).all()
        if pcargolist:
            #显示该航次所有的货物名称
            s=list(map(''.join,list(pcargolist.values_list("Pcargo_name"))))
            pcargo='-'.join(s)
            tem.append(pcargo)
        else:
            tem.append('无')

         #总预算结果
        budgetlist=Budget_result.objects.filter(Pship_number=pship.id).first()
        if budgetlist:
            #总运费收入 利润/亏损  相当租金水平  回扣佣金  经纪人佣金
            budget=[budgetlist.Sum_carriage,budgetlist.Profit_loss,budgetlist.Rent_level,budgetlist.Huikou_commission_p,budgetlist.Agent_commission_p]
            tem.extend(budget)
        else:
            tem.extend([0,0,0,0,0])
        infolist.append(tem)

    return render(request,'all_info.html',{'infolist':infolist})