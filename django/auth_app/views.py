from django.shortcuts import render,redirect
from django.contrib.auth.models import user
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixins
from .views import view 
from .form import RegisterForm




# Create your views here.

def register_view(request):
    if request.method  == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            username=form.cleaned_data.get('username')
            password=form.cleaned_data.get('password')
            user=user.objects.create_user(username='username',password='password')
            login(request,user)
            return redirect('home')

        else:
            form = RegisterForm()
            return render(request,'register.html', {'form':form})

   
def login_view(request):
    if request.method =='POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user=authenticate(username='username',password='pasword')

        if user is not None:
            login(request,user)
            next_url = request.POST.get('next') or request.GET.get('next') or 'home'
            return redirect(next_url)
        else:
            error_message = 'invalid credentials!'

    return render(request,'login.html', {'error':error_message})    


def logout_view(request):
    if request.method == 'POST':
        logout(request)
        return redirect('login')
    else:
        return redirect('home')


@login_required
def home_view(request):
    return(request,'home.html')        

        
class ProtectedView(LoginRequiredMixins,view):
    login_url = '/login/'
    redirect_field_name = 'redirect_to'

    def get(self,request):
        return render('protected.html')