from django.db import models

# Create your models here.
# 商场商铺的价位表
class rent(models.Model):
    id=models.IntegerField("租商铺价位id",primary_key=True)
    price=models.DecimalField("价格",max_digits=7,decimal_places=2)

# 商场表，可以看到所有商铺的状态
class market(models.Model):
    pos=models.CharField("商铺位置",max_length=100,default='')
    # 商铺租金外键
    rent=models.ForeignKey(rent,on_delete=models.CASCADE)
    is_rented=models.BooleanField("是否租出",null=False,default=False)

# 水费价位表
class paywater(models.Model):
    id=models.IntegerField("水费价位id",primary_key=True)
    money=models.DecimalField("费用",max_digits=7,decimal_places=2)

# 电费价位表
class payelec(models.Model):
    id=models.IntegerField("电费价位id",primary_key=True)
    money=models.DecimalField("费用",max_digits=7,decimal_places=2)    

# 商户表
class merchant(models.Model):
    name=models.CharField("商户名",max_length=25,null=False,default='')
    username=models.CharField("用户名",max_length=12,null=True)
    password=models.CharField("密码",max_length=12,null=True)
    tel=models.CharField(max_length=11,null=True)
    balance=models.DecimalField("余额",max_digits=7,decimal_places=2)

# 商铺种类表，与缴费相关
class type(models.Model):
    typename=models.CharField(max_length=10,null=False,default='')
    paywater=models.ForeignKey(paywater,on_delete=models.CASCADE,null=True)
    payelec=models.ForeignKey(payelec,on_delete=models.CASCADE,null=True)

# 商铺表，这是所有租出去的商铺的详细信息
class shop(models.Model):
    name=models.CharField("商铺名称",max_length=25,default='',null=False)
    # 关联种类表
    type=models.ForeignKey(type,on_delete=models.CASCADE)
    # 关联market表，用于修改is_rented字段
    market=models.OneToOneField(market,on_delete=models.CASCADE)
    # 关联商户，一对多关系
    merchant=models.ForeignKey(merchant,null=True,on_delete=models.CASCADE)

# 商品表
class goods(models.Model):
    name=models.CharField("商品名",max_length=25,default='')
    detail=models.CharField("商品描述",max_length=255,default="")
    price=models.DecimalField("商品价格",max_digits=7,decimal_places=2)
    img=models.CharField("商品图片",max_length=100,default='')
    shop=models.ForeignKey(shop,on_delete=models.CASCADE,null=True)

# 订单表
class order(models.Model):
    # 关联商铺，表明这是哪家商铺的订单
    shop=models.ForeignKey(shop,on_delete=models.CASCADE)
    # 关联商品，获取商品名和商品价格
    goods=models.ForeignKey(goods,on_delete=models.CASCADE)
    amount=models.IntegerField("商品数量",default=1)
    time=models.DateTimeField("订单创建时间",auto_now_add=True)

class user(models.Model):
    username=models.CharField("用户名",max_length=12,null=False)
    password=models.CharField("密码",max_length=12,null=False)
    sex=models.BooleanField(null=True)
    tel=models.CharField(max_length=11,null=True)

def scheduled():
    mers=merchant.objects.all()
    for mer in mers:
        money=0
        for shop in mer.shop_set:
            money+=shop.type.paywater.money+shop.type.payelec.money+shop.market.rent.price
        mer.balance-=money
        mer.save()