from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from .import views

urlpatterns = [

    path("register/", views.sign_up, name="signup"),

    path("login/", views.user_login, name="login"),

    path("logout/", views.user_logout, name="logout"),
    path("about/",views.about,name="about"),
    path("return-policy/", views.return_policy, name="return"),
    path("blog",views. blog_view,name="blog")

]

