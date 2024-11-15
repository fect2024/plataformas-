from django import template
from Tienda.models import *
import json
register = template.Library()

@register.filter()
def applydiscount(pid):
    data = Product.objects.get(id=pid)
    price = float(data.price) * (100 - int(data.discount))/100
    return price

@register.filter()
def productimage(pid):
    data = Product.objects.get(id=pid)
    return data.image.url

@register.filter()
def productname(pid):
    data = Product.objects.get(id=pid)
    return data.name

@register.filter()
def productprice(pid):
    data = Product.objects.get(id=pid)
    return data.price

@register.simple_tag()
def producttotalprice(data, qty):
    product = Product.objects.get(id=data)
    price = float(product.price) * (100 - float(product.discount)) / 100
    return int(qty) * price

@register.filter()
def get_product(productli):
    try:
        productli = productli.replace("'", '"')
        myli = json.loads(str(productli))['objects'][0]
        print(myli)
        pro_li = []
        for i, j in myli.items():
            pro_li.append(int(i))
        product = Product.objects.filter(id__in=pro_li)
        print(product)
        return product
    except:
        return None

@register.simple_tag
def get_qty(pro, bookid):
    try:
        book = Reserva.objects.get(id=bookid)
        productli = book.product.replace("'", '"')
        myli = json.loads(str(productli))['objects'][0]
        return myli[str(pro)]
    except:
        return 0