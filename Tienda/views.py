from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required
from .models import Carousel, Category, Product, User, UserProfile, Cart, Reserva, ORDERSTATUS, Feedback
import json
from django.http import HttpResponse

def home(request):
    return render(request, 'home.html')

def index(request):
    return render(request, 'navegacion.html')

def about(request):
    return render(request, 'acerca_de.html')

def main(request):
    data = Carousel.objects.all()
    dic = {'data': data}
    return render(request, 'index.html', dic)

def adminLogin(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None and user.is_staff:
            login(request, user)
            messages.success(request, "Usuario ingresó exitosamente")
            return redirect('admindashboard')
        else:
            messages.error(request, "Credenciales inválidas")
    return render(request, 'admin_login.html')

@staff_member_required
def adminHome(request):
    return render(request, 'admin_inicio.html')

@staff_member_required
def admin_dashboard(request):
    user = UserProfile.objects.filter()
    category = Category.objects.filter()
    product = Product.objects.filter()
    new_order = Reserva.objects.filter(estado=1)  
    dispatch_order = Reserva.objects.filter(estado=2) 
    way_order = Reserva.objects.filter(estado=3) 
    deliver_order = Reserva.objects.filter(estado=4) 
    cancel_order = Reserva.objects.filter(estado=5)
    return_order = Reserva.objects.filter(estado=6) 
    order = Reserva.objects.filter()
    read_feedback = Feedback.objects.filter(status=1)
    unread_feedback = Feedback.objects.filter(status=2)
    return render(request, 'admin_dashboard.html', locals())


@staff_member_required
def add_category(request):
    if request.method == "POST":
        name = request.POST['name']
        Category.objects.create(name=name)
        messages.success(request, "Categoría agregada")
        return redirect('view_category')
    return render(request, 'agregar_categoria.html')

@staff_member_required
def view_category(request):
    category = Category.objects.all()
    return render(request, 'lista_categorias.html', {'category': category})

@staff_member_required
def edit_category(request, pid):
    category = Category.objects.get(id=pid)
    if request.method == "POST":
        name = request.POST['name']
        category.name = name
        category.save()
        messages.success(request, "Categoría actualizada")
        return redirect('view_category')
    return render(request, 'editar_categoria.html', {'category': category})

@staff_member_required
def delete_category(request, pid):
    category = Category.objects.get(id=pid)
    category.delete()
    messages.success(request, "Categoría eliminada")
    return redirect('view_category')

@staff_member_required
def add_product(request):
    category = Category.objects.all()
    if request.method == "POST":
        name = request.POST['name']
        price = request.POST['price']
        cat = request.POST['category']
        discount = request.POST['discount']
        desc = request.POST['desc']
        image = request.FILES['image']
        catobj = Category.objects.get(id=cat)
        Product.objects.create(name=name, price=price, discount=discount, category=catobj, description=desc, image=image)
        messages.success(request, "Producto agregado")
        return redirect('view_product')
    return render(request, 'agregar_producto.html', locals())

@staff_member_required
def view_product(request):
    product = Product.objects.all()
    return render(request, 'lista_productos.html', locals())

@staff_member_required
def edit_product(request, pid):
    product = Product.objects.get(id=pid)
    category = Category.objects.all()
    if request.method == "POST":
        name = request.POST['name']
        price = request.POST['price']
        cat = request.POST['category']
        discount = request.POST['discount']
        desc = request.POST['desc']
        try:
            image = request.FILES['image']
            product.image = image
            product.save()
        except:
            pass
        catobj = Category.objects.get(id=cat)
        Product.objects.filter(id=pid).update(name=name, price=price, discount=discount, category=catobj, description=desc)
        messages.success(request, "Producto actualizado")
        return redirect('view_product')
    return render(request, 'editar_producto.html', locals())

@staff_member_required
def delete_product(request, pid):
    product = Product.objects.get(id=pid)
    product.delete()
    messages.success(request, "Producto eliminado")
    return redirect('view_product')

def registration(request):
    if request.method == "POST":
        fname = request.POST['fname']
        lname = request.POST['lname']
        email = request.POST['email']
        password = request.POST['password']
        address = request.POST['address']
        mobile = request.POST['mobile']
        image = request.FILES['image']
        user = User.objects.create_user(username=email, first_name=fname, last_name=lname, email=email, password=password)
        UserProfile.objects.create(user=user, mobile=mobile, address=address, image=image)
        messages.success(request, "Registro exitoso")
    return render(request, 'registro.html', locals())

def userlogin(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user:
            login(request, user)
            messages.success(request, "Usuario ingresó exitosamente")
            return redirect('home')
        else:
            messages.success(request, "Credenciales inválidas")
    return render(request, 'login.html', locals())

def profile(request):
    data = UserProfile.objects.get(user=request.user)
    if request.method == "POST":
        fname = request.POST['fname']
        lname = request.POST['lname']
        email = request.POST['email']
        address = request.POST['address']
        mobile = request.POST['mobile']
        try:
            image = request.FILES['image']
            data.image = image
            data.save()
        except:
            pass
        user = User.objects.filter(id=request.user.id).update(first_name=fname, last_name=lname)
        UserProfile.objects.filter(id=data.id).update(mobile=mobile, address=address)
        messages.success(request, "Perfil actualizado")
        return redirect('profile')
    return render(request, 'perfil.html', locals())

from django.contrib.auth import authenticate, login, logout

def logoutuser(request):
    logout(request)
    messages.success(request, "Cierre de sesión exitoso")
    return redirect('main')

def change_password(request):
    if request.method == 'POST':
        o = request.POST.get('old')
        n = request.POST.get('new')
        c = request.POST.get('confirm')
        user = authenticate(username=request.user.username, password=o)
        if user:
            if n == c:
                user.set_password(n)
                user.save()
                messages.success(request, "Contraseña cambiada")
                return redirect('main')
            else:
                messages.success(request, "Las contraseñas no coinciden")
                return redirect('change_password')
        else:
            messages.success(request, "Contraseña inválida")
            return redirect('change_password')
    return render(request, 'cambiar_contraseña.html')

def user_product(request,pid):
    if pid == 0:
        product = Product.objects.all()
    else:
        category = Category.objects.get(id=pid)
        product = Product.objects.filter(category=category)
    allcategory = Category.objects.all()
    return render(request, "producto_usuarios.html", locals())

def product_detail(request, pid):
    product = Product.objects.get(id=pid)
    latest_product = Product.objects.filter().exclude(id=pid).order_by('-id')[:10]
    return render(request, "detalles_producto.html", locals())

@login_required(login_url='userlogin')
def addToCart(request, pid):
    myli = {"objects": []}
    try:
        cart = Cart.objects.get(user=request.user)
        myli = json.loads((str(cart.product)).replace("'", '"'))
        try:
            myli['objects'][0][str(pid)] = myli['objects'][0].get(str(pid), 0) + 1
        except:
            myli['objects'].append({str(pid): 1})
        cart.product = myli
        cart.save()
    except Cart.DoesNotExist:
        myli['objects'].append({str(pid): 1})
        cart = Cart.objects.create(user=request.user, product=myli)
    return redirect('cart')
def incredecre(request, pid):
    cart = Cart.objects.get(user=request.user)
    if request.GET.get('action') == "incre":
        myli = json.loads((str(cart.product)).replace("'", '"'))
        myli['objects'][0][str(pid)] = myli['objects'][0].get(str(pid), 0) + 1
    if request.GET.get('action') == "decre":
        myli = json.loads((str(cart.product)).replace("'", '"'))
        if myli['objects'][0][str(pid)] == 1:
            del myli['objects'][0][str(pid)]
        else:
            myli['objects'][0][str(pid)] = myli['objects'][0].get(str(pid), 0) - 1
    cart.product = myli
    cart.save()
    return redirect('cart')

def cart(request):
    try:
        cart = Cart.objects.get(user=request.user)
        product = (cart.product).replace("'", '"')
        myli = json.loads(str(product))
        product = myli['objects'][0]
        empty_cart = len(product) == 0  # Check if cart is empty
    except:
        product = []
        empty_cart = True  # Cart is empty

    lengthpro = len(product)
    
    context = {
        'cart': cart,
        'product': product,
        'lengthpro': lengthpro,
        'empty_cart': empty_cart
    }

    return render(request, 'carrito.html', context)



def deletecart(request, pid):
    cart = Cart.objects.get(user=request.user)
    product = (cart.product).replace("'", '"')
    myli = json.loads(str(product))
    del myli['objects'][0][str(pid)]
    cart.product = myli
    cart.save()
    messages.success(request, "Eliminado exitosamente")
    return redirect('cart')

def booking(request):
    user = UserProfile.objects.get(user=request.user)
    cart = Cart.objects.get(user=request.user)
    total = 0
    deduction = 0
    discounted = 0
    productid = (cart.product).replace("'", '"')
    productid = json.loads(str(productid))

    try:
        productid = productid['objects'][0]
    except:
        messages.success(request, "El carrito está vacío. Por favor, añade productos al carrito.")
        return redirect('cart')

    for i, j in productid.items():
        product = Product.objects.get(id=i)
        total += int(j) * float(product.price)
        price = float(product.price) * (100 - float(product.discount)) / 100
        discounted += int(j) * price
    deduction = total - discounted

    if request.method == "POST":
        return redirect('/payment/?total=' + str(total) + '&discounted=' + str(discounted) + '&deduction=' + str(deduction))
    
    context = {
        'user': user,
        'cart': cart,
        'total': total,
        'deduction': deduction,
        'discounted': discounted
    }
    
    return render(request, "reserva.html", context)

    
    return render(request, "reserva.html", context)

def myOrder(request):
    order = Reserva.objects.filter(usuario=request.user)
    return render(request, "mi-orden.html", locals())

def user_order_track(request, pid):
    order = Reserva.objects.get(id=pid)
    orderstatus = ORDERSTATUS
    return render(request, "seguimiento-orden.html", locals())

def change_order_status(request, pid):
    order = Reserva.objects.get(id=pid)
    status = request.GET.get('status')
    if status:
        order.estado = status
        order.save()
        messages.success(request, "Estado de la orden cambiado.")
    return redirect('myorder')

STATUS = (
    (1, "Leído"),
    (2, "No Leído")
)
def user_feedback(request):
    user = UserProfile.objects.get(user=request.user)
    if request.method == "POST":
        Feedback.objects.create(user=request.user, message=request.POST['feedback'])
        messages.success(request, "Comentario enviado exitosamente.")
    return render(request, "comentarios.html", locals())

def manage_feedback(request):
    action = request.GET.get('action', 0)
    feedback = Feedback.objects.filter(status=int(action))
    return render(request, 'admin_comentarios.html', locals())

def delete_feedback(request, pid):
    feedback = Feedback.objects.get(id=pid)
    feedback.delete()
    messages.success(request, "Eliminado exitosamente.")
    return redirect('manage_feedback')

def payment(request):
    total = request.GET.get('total')
    discounted = request.GET.get('discounted')
    deduction = request.GET.get('deduction')
    cart = Cart.objects.get(user=request.user)

    context = {
        'total': total,
        'discounted': discounted,
        'deduction': deduction,
        'cart': cart,
    }
    
    if request.method == "POST":
        book = Reserva.objects.create(user=request.user, product=cart.product, total=total)
        cart.product = {'objects': []}
        cart.save()
        messages.success(request, "Book Order Successfully")
        return redirect('myorder')
    
    return render(request, 'pago.html', context)


def read_feedback(request, pid):
    feedback = Feedback.objects.get(id=pid)
    feedback.status = 1
    feedback.save()
    return HttpResponse(json.dumps({'id':1, 'Estado':'Leido'}), content_type="application/json")

def manage_order(request):
    action = request.GET.get('action', 0)
    order = Reserva.objects.filter(estado=int(action))
    order_status = ORDERSTATUS[int(action)-1][1]
    if int(action) == 0:
        order = Reserva.objects.all()
        order_status = 'Todos'
    return render(request, 'admin_ordenes.html', locals())

def delete_order(request, pid):
    order = Reserva.objects.get(id=pid)
    order.delete()
    messages.success(request, 'Order Deleted')
    return redirect('/manage-order/?action='+request.GET.get('action'))

def admin_order_track(request, pid):
    order = Reserva.objects.get(id=pid)
    orderstatus = ORDERSTATUS
    status = int(request.GET.get('status',0))
    if status:
        order.estado = status
        order.save()
        return redirect('admin_order_track', pid)
    return render(request, 'admin_rastreo_ordenes.html', locals()) 

def manage_user(request):
    user = UserProfile.objects.all()
    return render(request, 'admin_usuario.html', locals()) 

def delete_user(request, pid):
    user = User.objects.get(id=pid)
    user.delete()
    messages.success(request, "Usuario eliminado correctamente")
    return redirect('manage_user') 

def admin_change_password(request):
    if request.method == 'POST':
        o = request.POST.get('currentpassword')
        n = request.POST.get('newpassword')
        c = request.POST.get('confirmpassword')
        user = authenticate(username=request.user.username, password=o)
        if user:
            if n == c:
                user.set_password(n)
                user.save()
                messages.success(request, "Password Changed")
                return redirect('main')
            else:
                messages.success(request, "Password not matching")
                return redirect('admin_change_password')
        else:
            messages.success(request, "Invalid Password")
            return redirect('admin_change_password')
    return render(request, 'admin_cambiar_contraseña.html')

def contact(request):
    return render(request, 'contacto.html')