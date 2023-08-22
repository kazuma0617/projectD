from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.contrib.auth import authenticate, login, logout
from .models import SongModel, PointModel
from django.contrib.auth.decorators import login_required
from django.views.generic import CreateView, DeleteView, DetailView
from django.urls import reverse_lazy
from .forms import PointModelForm

import matplotlib.pyplot as plt
from io import BytesIO
import base64
import matplotlib
matplotlib.use('Agg')  # バックエンドを指定 (Aggは非表示)
import matplotlib.pyplot as plt
from matplotlib.dates import DateFormatter
import matplotlib.dates as mdates



# Create your views here.

def startfunc(request):
        return render(request, "start.html", {})

def signupfunc(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        try:
            user = User.objects.create_user(username, "", password)
            return render(request, "signup.html", {})
        except IntegrityError:
            return render(request, "signup.html", {"error":"このユーザーはすでに登録されています。"})
    return render(request, "signup.html", {})

def loginfunc(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("list")
        else:
            return render(request, "login.html", {})
    return render(request, "login.html", {})

def logoutfunc(request):
    logout(request)
    return redirect("login")

@login_required
def listfunc(request):
    object_list = SongModel.objects.all()
    return render(request, "list.html", {"object_list":object_list})

def song_detail(request, pk):
    song = SongModel.objects.get(pk=pk)
    points = song.pointmodel_set.all()
    return render(request, 'detail.html', {'points': points,"song":song})

class SongCreate(CreateView):
    template_name = "create.html"
    model = SongModel
    fields = ("title",)
    success_url = reverse_lazy("list")

def createfunc(request):
    if request.method == "POST":
        form = PointModelForm(request.POST or None)
        if form.is_valid():
            form.save()
            return redirect("list")
    else:
        form = PointModelForm()
    return render(request, "create2.html", {"form":form})

class SongDelete(DeleteView):
    template_name = "delete.html"
    model = SongModel
    success_url = reverse_lazy("list")

class PointDelete(DeleteView):
    template_name = "delete2.html"
    model = PointModel
    
    def get_success_url(self):
        target_pk = self.object.title_id.pk 
        return reverse_lazy("detail", kwargs={"pk": target_pk})





def graphfunc(request, pk):
    # データベースからデータを取得し加工
    song = SongModel.objects.get(pk=pk)
    points = song.pointmodel_set.all()
    x = [point.duedate for point in points]
    y = [point.point for point in points]

    # グラフを作成
    plt.plot(x, y)
    # x軸の日付の表示形式を設定
    date_format = DateFormatter("%m/%d")  # 表示形式を適宜調整
    plt.gca().xaxis.set_major_formatter(date_format)
    plt.xlabel('duedate')
    plt.ylabel('point')
    plt.title('graph')

    # グラフを画像としてエンコード
    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    image_base64 = base64.b64encode(buffer.read()).decode('utf-8')

    return render(request, 'graph.html', {'image_base64': image_base64})


