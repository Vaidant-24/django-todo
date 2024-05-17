from django.shortcuts import render,get_object_or_404
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from django.contrib.auth import authenticate,login as loginuser,logout
from django.http import HttpResponseRedirect
from django.urls import reverse
from app.forms import TodoForm
from app.models import Todo
from django.contrib.auth.decorators import login_required
# Create your views here.

@login_required(login_url='app:login')
def index(request):
    if request.user.is_authenticated:
        user = request.user
        form = TodoForm()
        todos = Todo.objects.filter(user=user).order_by('priority')
        context = {'form': form, 'todos': todos}
        return render(request,'app/index.html',context = context)

def signout(request):
    logout(request)
    return HttpResponseRedirect(reverse('app:index'))
def login(request):
    if request.method == 'GET':
        form = AuthenticationForm()
        context = {'form':form}
        return render(request, 'app/login.html',context=context)
    else:
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username = username, password = password)
            if user is not None:
                loginuser(request,user)
                return HttpResponseRedirect(reverse('app:index'))
        else:
            context = {'form': form}
            return render(request, 'app/login.html',context=context)



def success(request):
    return HttpResponseRedirect(reverse('app:success'))

def signup(request):
    if request.method == 'GET':
        form = UserCreationForm()
        context = {'form': form}
        return render(request, 'app/signup.html', context= context)
    else:
        form = UserCreationForm(request.POST)
        context = {'form': form}

        if form.is_valid():
           user = form.save()
           if user is not None:
               return HttpResponseRedirect(reverse('app:login'))
        else:
            return render(request, 'app/signup.html', context= context)
        
def add_todo(request):
    if request.user.is_authenticated:
        user = request.user
        form = TodoForm(request.POST)
        if form.is_valid():
            todo = form.save(commit=False)
            todo.user = user
            todo.save()
            return HttpResponseRedirect(reverse('app:index'))
        else:
            return render(request, 'app/index.html', context= {'form': form})
        
def delete_todo(request,id):
    record = Todo.objects.get(pk = id)
    record.delete()
    return HttpResponseRedirect(reverse('app:index'))

def change_todo(request,id,status):
    record = Todo.objects.get(pk = id)
    record.status = status
    record.save()
    return HttpResponseRedirect(reverse('app:index'))