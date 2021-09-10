from django.urls import path, include
from . import views

urlpatterns = [
    path('logout/', views.logoutPage, name="logout"),
    path('accounts/login/', views.loginPage, name='login'),
    path('accounts/', views.loginPage, name='login'),
    path('ppid/', views.loginPage, name='login'),
    path('login/', views.loginPage, name="login"),

    path('register/', views.registerPage, name="register"),
    path('dashboard/', views.dashboard, name="dashboard"),
    path('data-ppid/', views.data_ppid, name="datappid"),
    path('profile-admin/<int:pk>', views.profile, name="profile"),

    path('create-data/', views.create_data, name="create"),
    path('update-data/<int:pk>', views.update_data, name="update"),
    path('delete-data/<int:pk>', views.delete_data, name="delete"),

    path('permohonan/', views.permohonan_data, name="permohonan"),
    path('proses-permohonan/<int:pk>', views.proses_permohonan, name="prosespermohonan"),
    path('delete-permohonan/<int:pk>', views.delete_permohonan, name="deletepermohonan"),
    
    path('change-password/', views.MyPasswordChangeView.as_view(), name="change-password-view"),
    

    #     path('dashboard/', v.index, name='index'),
    # path('', v.indexuser, name='indexuser'),
    # path('register/', vr.register, name='register' ),
    # path('account/', include('django.contrib.auth.urls')),

    # path('login/', vr.login_redirect, name='login'),
    # path('account/', vr.login_redirect, name='login'),
]
