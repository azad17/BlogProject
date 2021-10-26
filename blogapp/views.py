from django.shortcuts import render,redirect
from django.urls.resolvers import URLPattern
from django.views.generic import ListView,UpdateView,DeleteView,CreateView
from .forms import UserForm
from django.contrib.auth.models import User
from django.urls import reverse_lazy
from django.contrib import auth
from django.contrib import messages
# Create your views here.

def register(request):
    form = UserForm()
    if request.method=='POST':
        username = request.POST['username']
        password = request.POST['password']
        user = User.objects.create_user(username=username,password=password)
        user.save();
        return redirect('blogapp:login')
    return render(request,'blogapp/register.html',{'form':form})

def login(request):
    if request.method=='POST':
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(username=username,password=password)
        if user is not None:
            auth.login(request,user)
            return redirect('/')
        else:
            messages.info(request,'Username/Password is Incorrect')
            redirect('userapp:login')
    return render(request,'userapp/login.html')    

class  UserList(ListView):
    model = User
    template_name = 'blogapp/userlist.html'
    context_object_name = 'user'

class UserUpdate(UpdateView):
    model = UserForm
    template_name = 'blogapp/userupdate.html'    
    def get_success_url(self):
        return reverse_lazy('blogapp:userlist',kwargs = {'pk':self.object.id})