from django import forms
from django.forms import widgets
from django.forms import fields
from work import models

class Products(forms.Form):

    products = fields.ChoiceField(
        choices=[],
        widget=widgets.Select(attrs={'name': "product"})
    )

    def __init__(self, *args, **kwargs):
        super(Products, self).__init__(*args, **kwargs)

        self.fields['products'].choices = models.Product.objects.values_list('id', 'name')


# 注册 forms
class FM_REGISTER(forms.Form):
    username = fields.CharField(
        min_length=6,
        max_length=30,
        error_messages={'required': '用户名不能为空' ,'min_length': '用户名长度不能小于6', 'max_length': '用户名长度不能大于12'},
        widget=widgets.TextInput(attrs={'class': 'form-control','id':'name','name':'username','placeholder': 'NAME','autocomplete':'off'}), # 设置样式
        label="用户名",
    )
    password = fields.CharField(
        min_length=6,
        max_length=12,
        error_messages={'required': '密码不能为空', 'min_length': '密码长度不能小于6', 'max_length': '密码长度不能大于12'},
        widget=widgets.PasswordInput(attrs={"class":"form-control", 'id':"email", "name":"email", "placeholder":"PASSWORD", "autocomplete":"off"}),
        label='密码'
    )
    email = fields.EmailField(
        error_messages={'required': '邮箱不能为空', 'invalid': '邮箱格式错误'},
        widget=widgets.EmailInput(attrs={"class":"form-control", "id":"password", "name":"password", "placeholder":"EMAIL", "autocomplete":"off"}),
        label = '邮箱'
    )