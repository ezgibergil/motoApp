from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth import authenticate, login,logout
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponseForbidden
from django.http import JsonResponse
from .models import Category
from datetime import datetime
from django.db.models import Sum, Count
from motoVitrin.models import Sale
from .models import Siparis
from django.http import HttpResponse
from motoVitrin.models import Role, UserRole
from django.views.decorators.csrf import csrf_protect







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


def category_list(request):
    if request.method == 'POST':
        category_name = request.POST.get('category_name')
        if category_name:
            Category.objects.create(name=category_name)
            messages.success(request, "Kategori başarıyla eklendi.")
        else:
            messages.error(request, "Kategori adı boş olamaz.")
        return redirect('category_list')

    categories = Category.objects.all()
    return render(request, 'category_list.html', {'categories': categories})

def delete_category(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    category.delete()
    messages.success(request, "Kategori başarıyla silindi.")
    return redirect('category_list')



def sales_report(request):
    # Formdan gelen seçili ay ve yıl verileri
    selected_month = request.GET.get("month")
    selected_year = request.GET.get("year")

    # Eğer ay veya yıl seçilmemişse, hata mesajı göster
    if not selected_month or not selected_year:
        messages.error(request, "Lütfen hem ayı hem de yılı seçin.")
        selected_month = str(datetime.now().month)  # Varsayılan olarak geçerli ay
        selected_year = str(datetime.now().year)    # Varsayılan olarak geçerli yıl

    # Satışları filtrele
    sales = Sale.objects.filter(sale_date__month=selected_month, sale_date__year=selected_year)


    # Toplam Satış ve KDV
    total_sales = sales.aggregate(total=Sum("amount"))["total"] or 0
    vat_amount = total_sales * 0.20

    # Kategoriye Göre Satış
    category_sales = sales.values("category__name").annotate(
        total_sales=Sum("amount"),
        sales_count=Count("id")
    ).order_by("-total_sales")

    # Ay ve Yıl Seçenekleri
    months = [
        {"value": "1", "label": "Ocak"},
        {"value": "2", "label": "Şubat"},
        {"value": "3", "label": "Mart"},
        {"value": "4", "label": "Nisan"},
        {"value": "5", "label": "Mayıs"},
        {"value": "6", "label": "Haziran"},
        {"value": "7", "label": "Temmuz"},
        {"value": "8", "label": "Ağustos"},
        {"value": "9", "label": "Eylül"},
        {"value": "10", "label": "Ekim"},
        {"value": "11", "label": "Kasım"},
        {"value": "12", "label": "Aralık"},
    ]

    years = list(range(2020, datetime.now().year + 1))

    context = {
        "total_sales": total_sales,
        "vat_amount": vat_amount,
        "category_sales": category_sales,
        "months": months,
        "years": years,
        "selected_month": selected_month,
        "selected_year": selected_year,
    }

    return render(request, "sales.html", context)





def siparis_ekle(request):
    if request.method == 'POST':
        kullanici_id = request.POST.get('kullanici')
        urun_adi = request.POST.get('urun_adi')
        miktar = int(request.POST.get('miktar', 0))  # Sayıya çeviriyoruz
        fiyat = float(request.POST.get('fiyat', 0.0))  # Sayıya çeviriyoruz
        durum = request.POST.get('durum')

        try:
            kullanici = User.objects.get(id=kullanici_id)
        except User.DoesNotExist:
            return render(request, 'siparis_ekle.html', {
                'kullanicilar': User.objects.all(),
                'hata_mesaji': 'Kullanıcı bulunamadı.'
            })

        # Siparişi oluştur ve kaydet
        siparis = Siparis.objects.create(
            kullanici=kullanici,
            urun_adi=urun_adi,
            miktar=miktar,
            fiyat=fiyat,
            durum=durum,
        )

        return redirect('siparis_listesi')  # Yönlendirme için doğru URL adını kullan

    kullanicilar = User.objects.all()
    return render(request, 'siparis_ekle.html', {'kullanicilar': kullanicilar})

def admin_dashboard(request):
    return render(request, 'userLoginPages/admin_dashboard.html')

def user_dashboard(request):
    return render(request, 'userLoginPages/user_dashboard.html')

def marketer_dashboard(request):
    return render(request, 'userLoginPages/marketer_dashboard.html')


def custom_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            
            # Kullanıcının rollerini al
            user_roles = UserRole.objects.filter(user=user)
            roles = [user_role.role.name.lower() for user_role in user_roles]  # Küçük harfe çevir

            # Rol bazlı yönlendirme
            if 'admin' in roles:
                return redirect('admin_dashboard')  # URL name kullanılmalı
            elif 'marketer' in roles:
                return redirect('marketer_dashboard')
            else:
                return redirect('user_dashboard')

        else:
            messages.error(request, 'Geçersiz giriş')
            return render(request, 'login.html')

    return render(request, 'login.html')


