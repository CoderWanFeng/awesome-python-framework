from mall.models import *

# 商铺价位表的数据
r1=rent.objects.create(id=1,price=4000)
r2=rent.objects.create(id=2,price=5000)
r3=rent.objects.create(id=3,price=6000)
r4=rent.objects.create(id=4,price=7000)

# 商场表
m1=market.objects.create(pos="A区101",is_rented=True,rent=r4)
m2=market.objects.create(pos="A区102",is_rented=True,rent=r4)
m3=market.objects.create(pos="A区103",is_rented=False,rent=r4)
m4=market.objects.create(pos="A区104",is_rented=True,rent=r3)
m5=market.objects.create(pos="A区201",is_rented=True,rent=r3)
m6=market.objects.create(pos="A区202",is_rented=False,rent=r3)
m7=market.objects.create(pos="A区203",is_rented=True,rent=r3)
m8=market.objects.create(pos="A区204",is_rented=False,rent=r2)
m9=market.objects.create(pos="B区101",is_rented=True,rent=r2)
m10=market.objects.create(pos="B区102",is_rented=False,rent=r2)
m11=market.objects.create(pos="B区103",is_rented=True,rent=r2)
m12=market.objects.create(pos="B区104",is_rented=False,rent=r2)
m13=market.objects.create(pos="B区201",is_rented=True,rent=r1)
m14=market.objects.create(pos="B区202",is_rented=True,rent=r1)
m15=market.objects.create(pos="B区203",is_rented=False,rent=r1)
m16=market.objects.create(pos="B区204",is_rented=True,rent=r1)

# 水费价位表
p1=paywater.objects.create(id=1,money=40)
p2=paywater.objects.create(id=2,money=60)
p3=paywater.objects.create(id=3,money=80)
p4=paywater.objects.create(id=4,money=100)
p5=paywater.objects.create(id=5,money=120)

# 电费价位表
pe1=payelec.objects.create(id=1,money=100)
pe2=payelec.objects.create(id=2,money=120)
pe3=payelec.objects.create(id=3,money=140)
pe4=payelec.objects.create(id=4,money=160)
pe5=payelec.objects.create(id=5,money=180)

# 商户表
u1=merchant.objects.create(name="葛二蛋",username='ai',password='123',tel='13798638123',balance=20000)
u2=merchant.objects.create(name="吴三桂",username='van',password='456',tel='13798618323',balance=13000)
u3=merchant.objects.create(name="竹牛逼",username='ia',password='789',tel='13868618323',balance=15000)

# 种类表
t1=type.objects.create(typename="品牌服装",paywater=p1,payelec=pe2)
t2=type.objects.create(typename="休闲零食",paywater=p2,payelec=pe3)
t3=type.objects.create(typename="恰饭管饱",paywater=p5,payelec=pe4)
t4=type.objects.create(typename="美容美发",paywater=p4,payelec=pe1)
t5=type.objects.create(typename="购物百货",paywater=p3,payelec=pe3)
t6=type.objects.create(typename="娱乐聚会",paywater=p1,payelec=pe5)
t7=type.objects.create(typename="电影院",paywater=p1,payelec=pe5)

# 商铺表
s1=shop.objects.create(name="七号小铺",market=m1,merchant=u1,type=t1)
s2=shop.objects.create(name="良品铺子",market=m2,merchant=u2,type=t2)
s3=shop.objects.create(name="南北零食",market=m4,merchant=u3,type=t2)
s4=shop.objects.create(name="牛鼎烧烤",market=m5,merchant=u1,type=t3)
s5=shop.objects.create(name="日式小料",market=m7,merchant=u2,type=t3)
s6=shop.objects.create(name="层层发艺",market=m9,merchant=u3,type=t4)
s7=shop.objects.create(name="俏佳人",market=m11,merchant=u1,type=t4)
s8=shop.objects.create(name="杰哥商超",market=m13,merchant=u2,type=t5)
s9=shop.objects.create(name="阿伟电动",market=m14,merchant=u3,type=t6)
s10=shop.objects.create(name="猫眼电影",market=m16,merchant=u1,type=t7)

# 商品表
g1=goods.objects.create(name="耐克凉鞋",detail="耐克最新款凉鞋",price=100,img="",shop=s1)
g2=goods.objects.create(name="阿迪达斯短袖",detail="阿迪达斯最新款短袖",price=80,img="",shop=s1)
g3=goods.objects.create(name="Peak短裤",detail="Peak最新款短裤",price=70,img="",shop=s1)
g4=goods.objects.create(name="安踏运动鞋",detail="安踏最新款运动鞋",price=150,img="",shop=s1)
g5=goods.objects.create(name="手撕面包",detail="敲好吃的面包",price=20,img="",shop=s2)
g6=goods.objects.create(name="海苔肉松卷",detail="敲好吃的海苔肉松卷",price=12.9,img="",shop=s2)
g7=goods.objects.create(name="猪肉脯",detail="敲好吃的猪肉脯",price=30.9,img="",shop=s2)
g8=goods.objects.create(name="多味花生",detail="敲好吃的多为花生",price=8.8,img="",shop=s2)
g9=goods.objects.create(name="绿豆饼",detail="网红绿豆饼",price=5.9,img="",shop=s3)
g10=goods.objects.create(name="烤馍片",detail="网红烤馍片",price=8.9,img="",shop=s3)
g11=goods.objects.create(name="威化饼干",detail="网红威化饼干",price=14.8,img="",shop=s3)
g12=goods.objects.create(name="里脊肉",detail="香喷喷的里脊肉",price=15,img='',shop=s4)
g13=goods.objects.create(name="火腿肠",detail="香喷喷的火腿肠",price=12,img='',shop=s4)
g14=goods.objects.create(name="肥牛卷",detail="香喷喷的肥牛卷",price=20,img='',shop=s4)
g15=goods.objects.create(name="味增汤",detail="和风味的味增汤",price=8,img='',shop=s5)
g16=goods.objects.create(name="筑前煮",detail="和风味的筑前煮",price=12,img='',shop=s5)
g17=goods.objects.create(name="大和煮",detail="和风味的大和煮",price=12,img='',shop=s5)
g18=goods.objects.create(name="唐扬饭",detail="和风味的唐扬饭",price=15,img='',shop=s5)

