from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path, include

from users import urls as user_urls
from users.views import login_page, home, logout_page

urlpatterns = [
    path('', home, name='home'),
    path('user/', include(user_urls)),
    path('login/', login_page, name='login'),
    path('logout/', logout_page, name='logout'),
    path('admin/', admin.site.urls),

    path('reset_password/',
         auth_views.PasswordResetView.as_view(template_name='registration/reset_password.html'),
         name='reset_password'),
    path('reset_password_sent/',
         auth_views.PasswordResetDoneView.as_view(template_name='registration/reset_password_sent.html'),
         name='password_reset_done'),
    path('reset/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(template_name='registration/reset_password_form.html'),
         name='password_reset_confirm'),
    path('reset_password_complete/',
         auth_views.PasswordResetCompleteView.as_view(template_name='registration/reset_password_done.html'),
         name='password_reset_complete'),

]
