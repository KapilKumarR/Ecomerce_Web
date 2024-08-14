from django.urls import path
from AccountsApp import views

urlpatterns = [
    path('',views.dashboard,name='dashboard'),
    path('dashboard/',views.dashboard,name='dashboard'),
    path('register/',views.register,name='register'),
    path('login/',views.login,name ='login'),
    path('logout/',views.logout,name='logout'),
    path('activate/<uidb64>/<token>',views.activate,name="activate"), 
    
    #reset pass url routing
    path('forgotPassword/',views.forgotPassword,name="forgotPassword"),
    path('resetPassword_validate/<uidb64>/<token>',views.resetPassword_validate,name="resetPassword_validate"), 
    path('resetPassword/',views.resetPassword,name='resetPassword'),
]