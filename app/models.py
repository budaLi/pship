from django.db import models
import time,datetime
from django.db import models
from django.utils.translation import ugettext_lazy as _


class Pship(models.Model):
    #Pship_id=models.IntegerField(_('船主id'))     #一个船主登陆后可以看多个船只的信息 这里以后可以作为外键更改
    Pship_number=models.CharField(_('航次'),max_length=200,unique=True)
    Pship_name = models.CharField(_('船舶名'),max_length=20)
    Pship_load=models.FloatField(_('载重吨'),max_length=20)
    Pship_hovel=models.FloatField(_('舱容'),max_length=20)
    Pship_speed=models.FloatField(_('默认航速'),default=12,null=True,blank=True)

    def __str__(self):
        return self.Pship_number

    class Meta:

        verbose_name = _('船舶信息')
        verbose_name_plural = _('船舶信息')


class Pport(models.Model):
     Pship_number=models.ForeignKey('Pship',on_delete=models.CASCADE,verbose_name='航次')
     Pport_order=models.IntegerField(_('顺序编号'))
     Pport_name=models.CharField(_('港口名'),max_length=50)
     Pport_shipstate=models.CharField(_('船舶状态'),max_length=100,choices=(('0', _('装货')), ('1', _('卸货')), ('3', _('加油'))))
     Pport_leisureday=models.IntegerField(_('空闲天数'))
     Pport_workday=models.IntegerField(_('工作天数'))
     Pport_eta=models.DateTimeField(_('ETA'),max_length=20)
     Pport_etd=models.DateTimeField(_('ETD'),max_length=20)
     Pport_cost=models.IntegerField(_('港口费用'))
     Pport_range=models.IntegerField(_('航程距离'),null=True,blank=True)
     Pport_shipday=models.IntegerField(_('在航天数'),null=True,blank=True)

     def __str__(self):
        return self.Pport_name

     class Meta:
        ordering=['Pport_order']
        verbose_name = _('港口信息')
        verbose_name_plural = _('港口信息')


class Pship_Pport(models.Model):
    Pship_number= models.ForeignKey("Pship",on_delete=models.CASCADE,verbose_name='航次')
    Pport_order=models.CharField(_('经过港口顺序'),max_length=20)
    Sum_range=models.IntegerField(_('总航行距离'))
    Sum_day=models.IntegerField(_('总航行时间'))
    Pport_lei_worday=models.IntegerField(_('总在港时间'))
    Pport_range=models.IntegerField(_('总在航时间'))
    Start_day=models.CharField(_('开始时间'),max_length=50)
    End_day=models.CharField(_('结束时间'),max_length=50)

    def __str__(self):
        return self.Pport_order
    class Meta:
        verbose_name = _('计算航程信息')
        verbose_name_plural = _('计算航程信息')

class Fuel_rent(models.Model):
    Pship_number= models.ForeignKey("Pship",on_delete=models.CASCADE,verbose_name='航次')
    FO_sea=models.CharField(_('FO在航消耗油量'),max_length=20)
    FO_port=models.CharField(_('FO在港消耗油量'),max_length=20)
    FO_price=models.CharField(_('FO油价'),max_length=20)
    DO_sea=models.CharField(_('DO在航消耗油量'),max_length=20)
    DO_port=models.CharField(_('DO在港消耗油量'),max_length=20)
    DO_price=models.CharField(_('DO油价'),max_length=20)
    FO=models.CharField(_('fO价格参考'),max_length=20)
    DO=models.CharField(_('DO价格参考'),max_length=20)
    Day_rent=models.CharField(_('日租金'),max_length=20)
    Commission=models.CharField(_('佣金'),max_length=20)

    class Meta:
        verbose_name = _('燃烧费及租金')
        verbose_name_plural = _('燃烧费及租金')


class Cost_result(models.Model):
    Pship_number= models.ForeignKey("Pship",on_delete=models.CASCADE,verbose_name='航次')
    #Pport_name=models.ForeignKey("Pport",on_delete=models.CASCADE)
    Sum_fuel=models.CharField(_('燃油费'),max_length=20)
    Sum_Pport_cost=models.CharField(_('总港口费用'),max_length=20)
    Sum_day_rent=models.CharField(_('总船舶租金（净）'),max_length=20)
    Sum_Cost=models.CharField(_('总成本'),max_length=20)
    Day_cost=models.CharField(_('每日成本'),max_length=20)

    class Meta:
        verbose_name = _('成本预算结果')
        verbose_name_plural = _('成本预算结果')


class Pcargo(models.Model):
    Pship_number= models.ForeignKey("Pship",on_delete=models.CASCADE,verbose_name='航次')
    Pcargo_name=models.CharField(_('货物名'),max_length=30,)
    Pcargo_num=models.IntegerField(_('货物量'))
    Pcargo_carriage=models.IntegerField(_('运费'),max_length=20)
    Huikou_commission_p=models.IntegerField(_('回扣佣金'),max_length=20)
    Agent_commission_p=models.IntegerField(_('代理人佣金 '),max_length=20)
    Carriage_tax=models.IntegerField(_('运费税'),max_length=20)
    Item_tax=models.IntegerField(_('其他扣除项'),max_length=20)
    Carriage_revenue=models.IntegerField(_('运费收益'),max_length=20)

    def __str__(self):
        return self.Pcargo_name
    class Meta:
        verbose_name = _('运费收益')
        verbose_name_plural = _('运费收益')


#每条船经过所有港口的结果

class Budget_result(models.Model):
    #Pcargo_name=models.ForeignKey("Pcargo",on_delete=models.CASCADE)
    Pship_number= models.ForeignKey("Pship",on_delete=models.CASCADE,verbose_name='航次')
    Sum_carriage=models.CharField(_('总运费收入'),max_length=20)
    Profit_loss=models.CharField(_('利润/亏损 '),max_length=20)
    Rent_level=models.CharField(_('相当租金水平'),max_length=20)
    Huikou_commission_p=models.CharField(_('回扣佣金'),max_length=20)
    Agent_commission_p=models.CharField(_('经纪人佣金'),max_length=20)

    class Meta:
        verbose_name = _('预算结果')
        verbose_name_plural = _('预算结果')





