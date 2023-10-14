from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_view
from . forms import LoginForm, MyPasswordResetForm, MyPasswordChangeForm, MySetPasswordForm
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path("category/<slug:val>", views.CategoryView.as_view(), name="category"),
    path("category-title/<val>",
         views.CategoryTitle.as_view(), name="category-title"),
    path("product-detail/<int:pk>",
         views.ProductDetail.as_view(), name="product-detail"),

    path('profile/', views.ProfileView.as_view(), name='profile'),
    path('address/', views.address, name='address'),
    path('updateAddress/<int:pk>',
         views.updateAddress.as_view(), name='updateAddress'),
    # product add to cart and payment
    path('add-to-cart/', views.add_to_cart, name='add-to-cart'),
    path('cart/', views.show_cart, name='showcart'),
    path("pluscart/", views.plus_cart),
    path("minuscart/", views.minus_cart),
    path("removecart/", views.remove_cart),
    # login and authenticaion
    path('registration/', views.CustomerRegistrationView.as_view(),
         name='customaerregistraion'),
    path('accounts/login/', auth_view.LoginView.as_view(template_name='basic/login.html',
         authentication_form=LoginForm), name='login'),

    path('password_change/', auth_view.PasswordChangeView.as_view(template_name='basic/changepassword.html',
         form_class=MyPasswordChangeForm, success_url='/password_change_done'), name='password_change'),

    path('password_change_done/', auth_view.PasswordChangeDoneView.as_view(
        template_name='basic/passwordchangedone.html'), name='password_change_done'),
    path('logout/', auth_view.LogoutView.as_view(next_page='login'), name='logout'),

    # password reset url
    path('password_reset/', auth_view.PasswordResetView.as_view(template_name='basic/password_reset.html',
                                                                form_class=MyPasswordResetForm), name='password_reset'),

    path('password_reset_done/', auth_view.PasswordResetDoneView.as_view(
        template_name='basic/password_reset_done.html'), name='password_reset_done'),

    path('password_reset_confirm/<uidb64>/<token>', auth_view.PasswordResetConfirmView.as_view(
        template_name='basic/password_reset_confirm.html', form_class=MySetPasswordForm), name='password_reset_confirm'),

    path('password_reset_complete/', auth_view.PasswordResetCompleteView.as_view(
        template_name='basic/password_reset_complete.html'), name='password_reset_complete'),


]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
