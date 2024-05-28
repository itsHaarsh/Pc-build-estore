from django.shortcuts import render, HttpResponse,redirect
from django.views import View
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from .models import Product,Cart,Order
from django.db.models import Q
import random
import razorpay
from django.core.mail import send_mail
from django.urls import reverse
from django.conf import settings
from django.http import JsonResponse


# Create your views here.
def about(request):
    return HttpResponse("this is about page")

def edit(request,rid):   #rid=3
    print("Id to be edited is:",rid)
    return HttpResponse("Id to be edited is "+ rid)

def delete(request,x1,x2):
    #print("Id to be edited is:",rid)
    #return HttpResponse("Id to be edited is "+ rid)
    z=int(x1)+int(x2)   #rid=3
   # print("Id to be deleted is:",z)
    print("addition is:",z)
    return HttpResponse("addition of x1 and x2 is "+ str(z))

class SimpleView(View):
    def get(self,request):
        return HttpResponse('hello from view class')
    

def hello(request):
    context={}
    context['greet']= 'good evening,we are learning DTL'
    context['x']=100
    context['y']=40
    context['l']=[1,4,2,5,6,7,'hello']
    context['product']=[
        {'id':1,'name':'samsung','cat':'mobile','price':2000},
        {'id':2,'name':'jeans','cat':'clothes','price':700},
        {'id':3,'name':'vivo','cat':'mobile','price':15000},
        {'id':4,'name':'adidas','cat':'shoes','price':3500},
        {'id':5,'name':'oneplus','cat':'mobile','price':35000},
        {'id':6,'name':'iphone','cat':'mobile','price':70000},
    ]
    return render(request,'hello.html',context)

#------------------------estore start
def home(request):
    # userid=request.user.id
    # print(userid)
    context={}
    p=Product.objects.filter(is_active=True)
    print(p)
    context['products']=p
    
    print("Result is:",request.user.is_authenticated)
    return render(request,'index.html',context)

def product_details(request,pid):
    p=Product.objects.filter(id=pid)
    context={}
    context['products']=p
    #print(p)
    return render(request,'product_details.html',context)

def viewcart(request):
    c=Cart.objects.filter(uid=request.user.id)
    np=len(c)
    s=0
    for x in c:
        s=s + x.pid.price* x.qty
        
    context={}
    context['data']=c
    context['total']=s
    context['n']=np
    
    return render(request,'cart.html',context)

def register(request):
    if request.method=='POST':
        uname=request.POST['uname']
        upass=request.POST['upass']
        ucpass=request.POST['ucpass']
        context={}
        if uname=="" or upass=="" or ucpass=="":
            context['errmsg']="Fields cannot be Empty"
        elif upass != ucpass:
            context['errmsg']="Password & confirm password didn't match"
        else:
            try:
                u=User.objects.create(password=upass,username=uname,email=uname)
                u.set_password(upass)
                u.save()
                context['success']="User Created Successfully, Please Login"
            except Exception:
                context['errmsg']="User with same username already exists!!!!"
        #return HttpResponse("User created successfully!!")
        return render(request,'register.html',context)
    else:
        return render(request,'register.html')
    
def user_login(request):
    if request.method=='POST':
        uname=request.POST['uname']
        upass=request.POST['upass']
        #print(uname,'-',upass)
        context={}
        if uname=="" or upass=="" :
            context['errmsg']="Fields cannot be Empty"
            return render(request,'login.html',context)
        else:
            u=authenticate(username=uname,password=upass)
            if u is not None:
                login(request,u)
                return redirect('/')
            else:
                context['errmsg']="invalid username and password"
                return render(request,'login.html',context)
            #print(u)
            # print(u.password)
        
        #return HttpResponse('data is fetched')
    else:
        return render(request,'login.html')
    
    
def user_logout(request):
    logout(request)
    return redirect('/')

def catfilter(request,cv):
    q1=Q(cat=cv)
    q2=Q(is_active=True)
    p=Product.objects.filter(q1&q2)
    print(p)
    context={}
    context['products']=p
    return render(request,'index.html',context)

def sort(request,sv):
    if sv=='0':
        #ascending
        col='price'
    else:
        #descending order
        col='-price'
    
    p=Product.objects.order_by(col)
    context={}
    context['products']=p
    return render(request,'index.html',context)

def range(request):
    min=request.GET['min']
    max=request.GET['max']
    # print(min)
    # print(max)
    q1=Q(price__gte=min)
    q2=Q(price__lte=max)
    q3=Q(is_active=True)
    p=Product.objects.filter(q1&q2&q3)
    context={}
    context['products']=p
    return render(request,'index.html',context)

def addtocart (request,pid):
    if request.user.is_authenticated:
        userid=request.user.id
        #print(pid)
    # print(userid)
        u=User.objects.filter(id=userid)   #4th object
        #print(u[0])
        p=Product.objects.filter(id=pid)   #6th object
        #print(p[0])
        q1=Q(uid=u[0])
        q2=Q(pid=p[0])
        c=Cart.objects.filter(q1 & q2)
        print(c)  # queryset[<object 3>] 
        n=len(c)   # 1
        context={}
        if n == 1: 
            context['msg']="Product Already Exist in cart!!"
        else:
            c=Cart.objects.create(uid=u[0],pid=p[0])
            c.save()
            context['success']="Product Added Successfully to Cart!!"
        context['products']=p
        
        return render(request,'product_details.html',context)
    else:
        return redirect('/login')
    
    
    
def remove(request,cid):   #cid=10
    c=Cart.objects.filter(id=cid)   #id=10
    c.delete()
    return redirect('/viewcart')


def updateqty(request,qv,cid):
    c=Cart.objects.filter(id=cid)
    if qv=='1':
        t=c[0].qty + 1
        c.update(qty=t)
        
    else:
        if c[0].qty + 1:
            t=c[0].qty-1
            c.update(qty=t)
    return redirect('/viewcart')

def placeorder(request):
    userid=request.user.id
    c=Cart.objects.filter(uid=userid)
    #print(c)
    oid=random.randrange(1000,9999)
    #print(oid)
    for x in c:
        #print(x)  #object
        #print(x.pid,"=",x.uid,"-",x.qty)
        o=Order.objects.create(order_id=oid,pid=x.pid,uid=x.uid,qty=x.qty)
        o.save()
        x.delete()
    context={}
    orders=Order.objects.filter(uid=request.user.id)
    np=len(orders)
    context['data']=orders
    context['n']=np
    s=0
    for x in orders:
        s=s+x.pid.price*x.qty
        context['total']=s
    
    return render(request,'placeorder.html',context)

def makepayment(request):
    orders=Order.objects.filter(uid=request.user.id)
    s=0
    for x in orders:
        s=s+x.pid.price*x.qty
        oid=x.order_id
    
    client = razorpay.Client(auth=("rzp_test_hKGMw2c7ye5tsv", "PbO5475XA8DAOPTdKkTDGA48"))

    data = { "amount": s*100, "currency": "INR", "receipt": oid }
    payment = client.order.create(data=data)
    #print(payment)
    context={}
    context['data']=payment
    uemail=request.user.email
    context['uemail']=uemail

    return render(request,'pay.html',context)

def sendusermail(request,uemail):
    msg="order detail are:---"
    send_mail(
        "ekart-order placed successfully",
        msg,
        "minetech991@gmail.com",
        [uemail],
        fail_silently=False,
        )
    return HttpResponse("mail send successfully")

def about(request):
    return render(request,'about.html')

def contact_view(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')

        if not name or not email or not message:
            return JsonResponse({'error': 'All fields are required.'})

        subject = f"Contact Form Submission from {name}"
        message_body = f"Name: {name}\nEmail: {email}\n\nMessage:\n{message}"
        from_email = settings.EMAIL_HOST_USER
        recipient_list = [settings.EMAIL_HOST_USER]

        try:
            send_mail(subject, message_body, from_email, recipient_list)
            return JsonResponse({'success': 'Thank you for contacting us! Your message has been sent.'})
        except Exception as e:
            return JsonResponse({'error': f'An error occurred: {e}'})

    return render(request, 'contact.html')
    
