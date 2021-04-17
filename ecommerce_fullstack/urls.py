from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from ecommerce_fullstack import settings
from store import views
from authentication import views as authviews
from cart import views as cartviews

urlpatterns = [

    # Admin Views
    path('jet/', include('jet.urls', 'jet')),
    path('admin/', admin.site.urls),
    
    # Shop Views
    path('', views.index, name='index'),
    path('about', views.about, name='about'),
    path('updateshop', views.updateShop, name='updateShop'),
    path('shop', views.shop, name='shop'),
    path('contact', views.contact, name='contact'),
    path('item/<int:productid>', views.item, name='item'),

    # Authentication Views
    path('login', authviews.login, name='login'),
    path('signup', authviews.signup, name='signup'),
    path('forgot_password', authviews.forgotPassword, name='forgot'),
    path('reset_password', authviews.resetPassword, name='reset'),
    path('logout', authviews.logout, name="logout"),
    path('profile', authviews.profile, name="profile"),

    # Cart views
    path('cart', cartviews.index, name="cart"),
    path('add', cartviews.add, name="add_to_cart"),
    path('remove', cartviews.remove, name="remove_from_cart"),
    path('decrease', cartviews.decreaseQuantity, name="decrease"),
    path('increase', cartviews.increaseQuantity, name="increase"),
    path('change-size/<str:size>', cartviews.changeSize, name="change-size")


] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
