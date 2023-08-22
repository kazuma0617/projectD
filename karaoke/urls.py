from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from .views import loginfunc, signupfunc, startfunc, listfunc, logoutfunc, song_detail, createfunc, graphfunc, SongCreate, SongDelete, PointDelete

urlpatterns = [
    path("signup/", signupfunc, name="signup"),
    path("login/", loginfunc, name="login"),
    path("logout/", logoutfunc, name="logout"),
    path("list/", listfunc, name="list"),
    path("detail/<int:pk>", song_detail, name="detail"),
    path("create/", SongCreate.as_view(), name="create"),
    path("create_point/", createfunc, name="createfunc"),
    path("delete/<int:pk>", SongDelete.as_view(), name="delete"),
    path("delete2/<int:pk>", PointDelete.as_view(), name="delete2"),
    path("graph/<int:pk>", graphfunc, name="graphfunc"),
    path("", startfunc, name="start"),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
