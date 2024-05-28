
from django.urls import path
from ecomm_app import views
from django.conf.urls.static import static
from ecomm import settings

urlpatterns = [
    path('about/', views.about ,name="about"),
    path('', views.home ,name="home"),
    path('edit/<rid>',views.edit),
    path('delete/<x1>/<x2>',views.delete),
    path('myview',views.SimpleView.as_view()),
    path('hello',views.hello),
    path('pdetails/<pid>',views.product_details),
    path('viewcart',views.viewcart),
    path('register',views.register),
    path('login',views.user_login),
    path('logout',views.user_logout),
    path('catfilter/<cv>',views.catfilter),
    path('sort/<sv>',views.sort),
    path('range',views.range),
    path('addtocart/<pid>',views.addtocart),
    path('remove/<cid>',views.remove),
    path('updateqty/<qv>/<cid>',views.updateqty),
    path('placeorder',views.placeorder),
    path('makepayment',views.makepayment),
    path('sendmail/<uemail>',views.sendusermail),
    path('about',views.about),
    path('contact', views.contact_view, name='contact'),
    
    
    
]

if settings.DEBUG:
    
    urlpatterns+= static(settings.MEDIA_URL,
                        document_root=settings.MEDIA_ROOT)
