from .models import *

def scheduled():
    mers=merchant.objects.all()
    for mer in mers:
        money=0
        for shop in mer.shop_set:
            money+=shop.type.paywater.money+shop.type.payelec.money+shop.market.rent.price
        mer.balance-=money
        mer.save()