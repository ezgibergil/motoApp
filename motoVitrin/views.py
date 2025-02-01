from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login,logout
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponseForbidden
from django.http import JsonResponse



def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)

        if user is not None:
            
            login(request, user)
            messages.success(request, "Başarılı giriş")
            return redirect('home')
        else:
            messages.error(request, 'Hatalı giriş.')
            return render(request, 'login.html')
        

    return render(request, 'login.html')

@login_required  #dashboard sayfasına geçebilmek için giriş yapma zorunluluğu kılar.
def home(request):
    return render(request, 'home.html')

def register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        password2 = request.POST.get('password2')

        if not username or not password or not password2:
            return JsonResponse({
                'error': 'Lütfen bütün alanları doldurunuz.'
            })
        if password!=password2:
            return JsonResponse({
                'error': 'Şifreler eşleşmiyor.'
            })
        if User.objects.filter(username=username).exists():
            return JsonResponse({
                'error': 'Bu kullanıcı adı zaten kullanılıyor.'
            })
        user = User.objects.create_user(username=username, password=password)
        user.save()
        login(request,user)

        return JsonResponse({
           'success': 'Kayıt başarılı.',
            'redirect_url': '/login'
        })
    else:
        return render(request,'register.html')
    
def logout_user(request):
    logout(request)
    return redirect('login')

def user_list(request):
    users = User.objects.all()  # Tüm kullanıcıları al
    return render(request, 'user_list.html', {'users': users})