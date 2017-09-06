from django.db import models

# Create your models here.
class User_Info(models.Model):
    """用户信息表"""
    username = models.CharField(max_length=32)
    password = models.CharField(max_length=32)
    email = models.EmailField(max_length=64, db_index=True)
    class Meta:
        db_table = "user_info"
        unique_together =(("username", "password"),)


class Product(models.Model):
    """产品表"""
    name = models.CharField(max_length=64, db_index=True)
    class Meta:
        db_table = 'product_names'


class Domain_info(models.Model):
    """新业务上线表"""
    project_name = models.CharField(max_length=64, null=True)
    domain = models.CharField(max_length=64)
    online_date = models.CharField(max_length=64, db_index=True)
    https = models.CharField(max_length=32, null=True)  # 0是http, 1是https
    state = models.CharField(max_length=128)
    author = models.CharField(max_length=32)
    status = models.CharField(max_length=4)     # 0 是进行中，1是已完成
    apply_date = models.CharField(max_length=64)
    product = models.ForeignKey("Product", to_field="id")
    ops = models.ForeignKey('User_Info', to_field="id")
    class Meta:
        db_table = 'domain_info'


class Op_domain(models.Model):
    """域名解析表"""
    domain = models.CharField(max_length=64, db_index=True)
    IP = models.CharField(max_length=64)
    internal = models.CharField(max_length=32)
    online_date = models.CharField(max_length=64, db_index=True)
    state = models.CharField(max_length=128)
    author = models.CharField(max_length=32)
    status = models.CharField(max_length=4)  # 0 是进行中，1是已完成
    apply_date = models.CharField(max_length=64)
    ops = models.ForeignKey('User_Info', to_field="id")
    product = models.ForeignKey("Product", to_field="id")

    class Meta:
        db_table = 'op_domain'