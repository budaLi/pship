# from django.forms import ModelForm
# from app.models import Pcargo ,Pship,Pport,Pship_Pport,Fuel_rent,Cost_result,Budget_result
#
# class PshipForm(ModelForm):
#     class Meta:
#         model = Pship  # 根据 Pship模型创建表单
#         fields = ['Pship_name', 'Pship_num', 'Pship_load','Pship_hovel', 'Pship_speed']  # 该表单包含的字段
#
# class PportForm(ModelForm):
#     class Meta:
#         model = Pport
#         fields = ['Pport_name', 'Pport_shipstate','Pport_leisureday', 'Pport_workday','Pport_eta', 'Pport_etd','Pport_cost', 'Pport_range','Pport_shipday']
#
# class Pship_PportForm(ModelForm):
#     class Meta:
#         model = Pship_Pport
#         fields = ['Pship_num', 'Pport_name','Sum_range', 'Sum_day','Pport_lei_worday', 'Pport_range','Start_day', 'End_day']
#
# class Fuel_rentForm(ModelForm):
#     class Meta:
#         model = Fuel_rent
#         fields = ['FO_sea', 'FO_port','FO_price', 'DO_sea','DO_port', 'DO_price','FO', 'DO','Day_rent','Commission']
#
# class Cost_resultForm(ModelForm):
#     class Meta:
#         model = Cost_result
#         fields = ['Pship_num', 'Pport_name','Sum_fuel', 'Sum_Pport_cost','Sum_day_rent', 'Sum_Cost','Day_cost']
#
# class PcargoForm(ModelForm):
#     class Meta:
#         model = Pcargo
#         fields = ['Pcargo_name', 'Pcargo_num','Pcargo_carriage', 'Huikou_commission_p','Agent_commission_p', 'Carriage_tax','Item_tax', 'Carriage_revenue']
#
# class Budget_resultForm(ModelForm):
#     class Meta:
#         model = Budget_result
#         fields = ['Pcargo_name', 'Pship_num','Sum_carriage', 'Profit_loss','Rent_level', 'Huikou_commission_p','Agent_commission_p']
#
