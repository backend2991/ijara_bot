from django.shortcuts import render, redirect
from .models import Register, Comment, Book, Bookimage

from django.contrib import messages

from django.contrib.auth.hashers import make_password, check_password

def logout(request):
    request.session.flush()
    return redirect('base')

def succes(request):
    return render(request, 'succes.html')

def dashboard(request):
    # 1. Avtorizatsiyani tekshirish
    user_id = request.session.get('user_id')
    if not user_id:
        return redirect('login') # Agar session bo'lmasa, login sahifasiga yuboramiz
    
    # 2. Foydalanuvchi ma'lumotlarini olish
    try:
        user_data = Register.objects.get(id=user_id)
    except Register.DoesNotExist:
        return redirect('login') # Foydalanuvchi topilmasa ham logout qilib yuboramiz

    # 3. Kitoblarni olish (Qidiruv bo'lsa filter bilan, bo'lmasa hammasi)
    qidiruv_sozi = request.GET.get('q') # HTML dagi input name="q" bo'lgani uchun 'q' ni oldim
    if qidiruv_sozi:
        kitoblar = Book.objects.filter(name__icontains=qidiruv_sozi)
    else:
        kitoblar = Book.objects.all()

    # 4. Hammasini bitta context'da yuboramiz
    context = {
        'user': user_data,
        'kitoblar': kitoblar
    }
    
    return render(request, 'dashboard.html', context)



def base(request):
    return render(request, 'home.html')




def create_user(request):
    if request.method == 'POST':
        data = request.POST
        username_check = data.get('username')

        if Register.objects.filter(username=username_check).exists():
            messages.error(request, 'Iltimos boshqa username kiritng bu username band')
            return render(request,'register.html')

        last_name = data.get('last_name')
        first_name = data.get('first_name')
        birth_year = data.get('year')
        email = data.get('email')
        username = data.get('username')
        password = data.get('password')
        hashed_pass = make_password(password)   
        new_user = Register.objects.create(
            last_name=last_name,
            first_name=first_name,
            year=birth_year,
            email=email,
            username=username,
            password=hashed_pass
        )

        new_user.save()

        

        return redirect('succes')
    return render(request,'register.html')


def login(request):
    if request.method == "POST":
        data = request.POST
        username = data.get('username')
        password = data.get('password')


        try:
            user = Register.objects.get(username=username,)

            if check_password(password, user.password):
                request.session['user_id'] = user.id
                return redirect('dashboard')
            else:
                messages.error(request, 'Parol xato')
                return redirect('login')
        except Register.DoesNotExist:
            messages.error(request, 'Bunday foydalanuvchi mavjud emas')
            return redirect( 'login')
    return render(request, 'login.html')



    


def book_detail(request, pk):
    book = Book.objects.filter(id=pk).first()
    return render(request, 'pass.html', context={'kitob_batafsil': book})

def create_comment(request):
    if request.method == "POST":
        data = request.POST
        full_name = data.get('full_name')
        text = data.get('text')
        product_id = data.get('product_id')
        print(data)
        new_comment = Comment.objects.create(
            full_name=full_name,
            text=text,
            book_id=product_id
        )          
        new_comment.save()
        return redirect('book_detail', pk=product_id)
    
    return redirect('books_list')


            
        

        








