from django.contrib import messages
from django.db import transaction, models
from django.http import JsonResponse
from skill.forms import UserSkillForm, SkillForm, SkillCategoryForm
from users.models import SystemLog,User, Country, City, District, Language, Address, Skill, SkillCategory, user, UserSkill
from django.shortcuts import render, get_object_or_404
from .models import User, Country, Language, District
from .forms import RegisterForm
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import login
from django.shortcuts import render, redirect

from django.shortcuts import render
from django.db.models import Count, Avg
from users.models import User, Skill, Exchange, ExchangeRequest, Rating
import json
from users.models.ContactMessage import ContactMessage




def login_redirect(request):
    if not request.user.is_authenticated:
        return redirect('login')
    if request.user.is_superuser:
        return redirect('/adminPanel/dashboard/')
    elif request.user.is_staff:
        return redirect('/users/dashboard/')
    else:
        return redirect('/')  # کاربر عادی


@login_required(login_url='/login/')
def dashboard(request):
    user = request.user

    my_requests_status = list(ExchangeRequest.objects.filter(requester=user)
                              .values('status')
                              .annotate(count=Count('id')))

    my_offered_skills = list(ExchangeRequest.objects.filter(requester=user)
                             .values('offered_skill__skill_id__name')
                             .annotate(count=Count('id')))

    my_exchanges = list(Exchange.objects.filter(models.Q(user_x=user) | models.Q(user_y=user))
                        .values('status')
                        .annotate(count=Count('id')))


    my_received_ratings = list(Rating.objects.filter(target_user=user)
                               .values('score')
                               .annotate(count=Count('id'))
                               .order_by('score'))


    my_time_preferences = list(ExchangeRequest.objects.filter(requester=user)
                               .values('preferred_time_range')
                               .annotate(count=Count('id')))

    context = {
        'my_requests_data': json.dumps(my_requests_status),
        'my_offered_skills_data': json.dumps(my_offered_skills),
        'my_exchanges_data': json.dumps(my_exchanges),
        'my_ratings_data': json.dumps(my_received_ratings),
        'my_time_data': json.dumps(my_time_preferences),
    }
    return render(request, 'users/dashboard.html',context)



def register_view(request):
    # ۱. گرفتن داده‌ها از URL (چه در GET و چه در POST)
    skill = request.GET.get('skill')
    postal = request.GET.get('postalcode')

    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = True
            user.is_staff = True
            user.save()

            login(request, user)

            # ۲. بررسی هوشمند: اگر داده جستجو داشتیم، برو به نتایج
            if skill and postal:
                return redirect(f'/searching_skills/?skill={skill}&postalcode={postal}')

            return redirect('user_dashboard')
    else:
        form = RegisterForm()

    return render(request, 'users/auth/register.html', {'form': form})
def users_list(request):
    users = User.objects.all().values('id', 'username', 'first_name', 'last_name', 'email', 'is_active', 'is_superuser')
    return render(request, 'users/index.html', {'users': users})
def user_form(request):
    user = request.user
    countries = Country.objects.all()
    languages = Language.objects.all()
    context = {'user': user, 'countries': countries, 'languages': languages}
    return render(request, 'users/create.html', context)
def load_cities(request):
    country_id = request.GET.get('country_id')
    cities = City.objects.filter(country_id=country_id)
    data = [{'id': c.id, 'name': c.city_name} for c in cities] if cities.exists() else []
    return JsonResponse(data, safe=False)
def load_districts(request):
    city_id = request.GET.get('city_id')
    districts = District.objects.filter(city_id=city_id)
    data = [{'id': d.id, 'name': d.district_name} for d in districts] if districts.exists() else []
    return JsonResponse(data, safe=False)
def create_user(request):
    if request.method == 'POST':
        try:
            with transaction.atomic():

                # user address
                street_name = request.POST.get('street_name')
                street_number = request.POST.get('street_number')
                postal_code = request.POST.get('postal_code')
                district_id = request.POST.get('district_id')
                gender = request.POST.get('gender')

                # فیلدهای مخفی (Hidden Fields)

                latitude = request.POST.get('latitude')
                longitude = request.POST.get('longitude')
                timezone = request.POST.get('timezone')

                # if we have data , then save it
                user_address = None
                if street_name and district_id:
                    user_address = Address.objects.create(
                        street_name=street_name,
                        street_number=street_number,
                        postal_code=postal_code,
                        district_id=district_id,
                        longitude=float(longitude) if longitude else None,
                        latitude=float(latitude) if latitude else None,
                        timezone=timezone,
                    )

                username = request.POST.get('username')
                first_name = request.POST.get('first_name')
                last_name = request.POST.get('last_name')
                email = request.POST.get('email')

                phone = request.POST.get('phone')
                if not phone or phone.strip() == "":
                    phone = None

                dob = request.POST.get('date_of_birth')
                lang_id = request.POST.get('language_id')
                notifications_via = request.POST.get('notifications_via')
                bio = request.POST.get('bio')

                is_active = request.POST.get('is_active') in ['on', '1']
                is_staff = request.POST.get('is_staff') in ['on', '1']
                is_superuser = request.POST.get('is_superuser') in ['on', '1']

                if email and username:
                    user_data = User(
                        username=username,
                        email=email,
                        first_name=first_name,
                        last_name=last_name,
                        phone=phone,
                        date_of_birth=dob if dob else None,
                        bio=bio,
                        address_id=user_address,
                        is_active=is_active,
                        is_staff=is_staff,
                        is_superuser=is_superuser,
                        notifications_via=notifications_via,
                        gender=gender
                    )

                    if lang_id and lang_id.isdigit():
                        user_data.preferred_language_id = int(lang_id)

                    if request.FILES.get('profile_image_url'):
                        user_data.profile_image_url = request.FILES.get('profile_image_url')

                    user_data.set_password("Nothack@123")
                    user_data.save()

                    messages.success(request, "Benutzer erfolgreich erstellt!")
                    return redirect('users_list')
                else:
                    messages.error(request, "Username und Email sind erforderlich.")

        except Exception as e:
            messages.error(request, f"Fehler beim Speichern: {str(e)}")
    return render(request, 'users/create.html')
def destroy_user(request, userId):
    user = get_object_or_404(User, id=userId)
    user.delete()
    address = user.address_id
    if address:
        address.delete()

    messages.success(request, "Benutzer ist gelöscht")
    return redirect('users_list')
def edit_form(request, userId):
    user = get_object_or_404(User, id=userId)
    address = user.address_id
    current_district_id = None
    current_city_id = None
    current_country_id = None

    if user.address_id and user.address_id.district_id:
        try:
            district = District.objects.select_related('city__country').get(id=user.address_id.district_id)
            current_district_id = district.id
            current_city_id = district.city.id
            current_country_id = district.city.country.id
        except District.DoesNotExist:
            pass

    context = {
        'user': user,
        'countries': Country.objects.all(),
        'languages': Language.objects.all(),
        'current_country_id': current_country_id,
        'current_city_id': current_city_id,
        'current_district_id': current_district_id,
        'address': address,
    }
    return render(request, 'users/edit.html', context)
def update_user(request, userId):
    if request.method == 'POST':
        user = get_object_or_404(User, id=userId)

        # ۱. آپدیت اطلاعات پایه کاربر
        user.username = request.POST.get('username')
        user.first_name = request.POST.get('first_name')
        user.last_name = request.POST.get('last_name')
        user.gender = request.POST.get('gender')
        user.email = request.POST.get('email')
        dob = request.POST.get('date_of_birth')
        user.date_of_birth = dob if dob else None
        user.phone = request.POST.get('phone')
        user.bio = request.POST.get('bio')
        user.preferred_language_id = request.POST.get('language_id') or None
        user.notifications_via = request.POST.get('notifications_via')

        # آپدیت وضعیت‌های بولین (Checkboxes)
        user.is_active = 'is_active' in request.POST
        user.is_staff = 'is_staff' in request.POST
        user.is_superuser = 'is_superuser' in request.POST

        # ۲. مدیریت تصویر پروفایل
        if 'profile_image_url' in request.FILES:
            user.profile_image_url = request.FILES['profile_image_url']

        # ۳. مدیریت پسورد (فقط اگر پر شده باشد)
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        if password:
            if password == confirm_password:
                user.set_password(password)
            else:
                messages.error(request, "Passwörter stimmen nicht überein!")
                return redirect('edit_form', userId=user.id)

        # ۴. آپدیت یا ایجاد جدول آدرس (Address Table)
        # فرض می‌کنیم یوزر یک رابطه ForeignKey یا OneToOne به آدرس دارد
        addr = user.address_id
        if not addr:
            addr = Address.objects.create()
            user.address_id = addr

        addr.street_name = request.POST.get('street_name')
        addr.street_number = request.POST.get('street_number')
        addr.postal_code = request.POST.get('postal_code')
        addr.district_id = request.POST.get('district_id')  # ذخیره ID منطقه

        # فیلدهای مخفی (Hidden Fields)

        latitude = request.POST.get('latitude')
        longitude = request.POST.get('longitude')

        addr.latitude = float(latitude) if latitude else None
        addr.longitude = float(longitude) if longitude else None

        addr.timezone = request.POST.get('timezone')

        addr.save()
        user.save()

        messages.success(request, f"Benutzer {user.username} wurde erfolgreich aktualisiert.")
        return redirect('users_list')
    return redirect('edit_form', userId=userId)
def user_info(request, userId):
    user = get_object_or_404(User, id=userId)

    district_obj = None
    if user.address_id and user.address_id.district_id:
        district_obj = District.objects.select_related('city__country').filter(id=user.address_id.district_id).first()
    else:
        district_obj = None
        language_obj = None
    context = {
        'user': user,
        'location': district_obj
    }
    return render(request, 'users/user_info.html', context)
def profile(request, userId):
    user = get_object_or_404(User, id=userId)
    address = user.address_id
    current_district_id = None
    current_city_id = None
    current_country_id = None

    if user.address_id and user.address_id.district_id:
        try:
            district = District.objects.select_related('city__country').get(id=user.address_id.district_id)
            current_district_id = district.id
            current_city_id = district.city.id
            current_country_id = district.city.country.id
        except District.DoesNotExist:
            pass

    context = {
        'user': user,
        'countries': Country.objects.all(),
        'languages': Language.objects.all(),
        'current_country_id': current_country_id,
        'current_city_id': current_city_id,
        'current_district_id': current_district_id,
        'address': address,
    }
    return render(request, 'users/profile.html', context)
def update_user_profile(request, userId):
    if request.method == 'POST':
        user = get_object_or_404(User, id=userId)

        user.username = request.POST.get('username')
        user.first_name = request.POST.get('first_name')
        user.last_name = request.POST.get('last_name')
        user.gender = request.POST.get('gender')
        user.email = request.POST.get('email')
        user.phone = request.POST.get('phone')
        user.bio = request.POST.get('bio')
        user.preferred_language_id = request.POST.get('language_id') or None
        user.notifications_via = request.POST.get('notifications_via')

        if request.user.is_superuser:
            user.is_active = 'is_active' in request.POST
            user.is_staff = 'is_staff' in request.POST
            user.is_superuser = 'is_superuser' in request.POST
        else:
            pass

        if 'profile_image_url' in request.FILES:
            user.profile_image_url = request.FILES['profile_image_url']

        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        if password:
            if password == confirm_password:
                user.set_password(password)
            else:
                messages.error(request, "Passwörter stimmen nicht überein!")
                return redirect('edit_form', userId=user.id)

        addr = user.address_id
        if not addr:
            addr = Address.objects.create()
            user.address_id = addr

        addr.street_name = request.POST.get('street_name')
        addr.street_number = request.POST.get('street_number')
        addr.postal_code = request.POST.get('postal_code')
        addr.district_id = request.POST.get('district_id')

        latitude = request.POST.get('latitude')
        longitude = request.POST.get('longitude')

        addr.latitude = float(latitude) if latitude else None
        addr.longitude = float(longitude) if longitude else None

        addr.timezone = request.POST.get('timezone')

        addr.save()
        user.save()

        messages.success(request, f"Benutzer {user.username} wurde erfolgreich aktualisiert.")
        return redirect('profile',userId=userId)
    return redirect('profile', userId=userId)


# ------------------user skill funktion -------------------

def user_skill(request):
    user_id = request.user.id
    user_skills = UserSkill.objects.select_related('skill_id', 'user_id').filter(user_id=user_id)
    context = {
        'user_skills': user_skills,
        'form': UserSkillForm(),
        'skill_form': SkillForm(),
        'category_form': SkillCategoryForm(),
        'categories': SkillCategory.objects.all(),
        'skills': Skill.objects.all(),
        'all_skills': Skill.objects.all(),
    }
    return render(request, 'users/user_skill.html', context)
def load_skills(request):
    category_id = request.GET.get('category_id')
    skills = Skill.objects.filter(skill_category_id=category_id)
    data = [{'id': s.id, 'name': s.name} for s in skills]
    return JsonResponse(data, safe=False)
def create_user_skill_category(request):
    if request.method == 'POST':
        form = SkillCategoryForm(request.POST, request.FILES)
        if form.is_valid():
            category = form.save()
            # Wir geben die ID und den Namen zurück, damit JS das Dropdown aktualisieren kann
            return JsonResponse({
                'success': True,
                'id': category.id,
                'name': category.skill_name
            })
        else:
            return JsonResponse({'success': False, 'errors': form.errors}, status=400)
    return JsonResponse({'success': False}, status=405)
def ajax_create_skill(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        category_id = request.POST.get('skill_category_id')
        description = request.POST.get('description', '')

        if name and category_id:
            skill = Skill.objects.create(
                name=name,
                skill_category_id_id=category_id,  # Nutze die ID direkt
                description=description
            )
            return JsonResponse({'success': True, 'id': skill.id, 'name': skill.name})
    return JsonResponse({'success': False}, status=400)
def user_skill_create(request):
    if request.method == 'POST':
        form = UserSkillForm(request.POST, user=request.user)

        if form.is_valid():
            user_skill = form.save(commit=False)

            # اگر ادمین نیست، یوزر را اجباراً خودش ست کن
            if not request.user.is_superuser:
                user_skill.user_id = request.user
            # اگر ادمین است، خودِ فرم مقدار user_id را دارد و ذخیره می‌شود

            user_skill.save()
            messages.success(request, "Erfolgreich gespeichert!")
            return redirect('user_skill')
        else:
            messages.error(request, f"Fehler: {form.errors}")
    return redirect('user_skill')
def user_skill_delete(request, pk):
    user_skill = get_object_or_404(UserSkill, pk=pk)
    user_skill.delete()
    messages.warning(request, "Die Kompetenz wurde erfolgreich aus Ihrem Profil entfernt.")
    return redirect('user_skill')
def skills_by_category(request):
    category_id = request.GET.get('category_id')
    if category_id:
        skills = Skill.objects.filter(skill_category_id_id=category_id).values('id', 'name')
        return JsonResponse(list(skills), safe=False)
    return JsonResponse([], safe=False)
def user_skill_update(request, pk):
    user_skill = get_object_or_404(UserSkill, pk=pk)

    if request.method == 'POST':
        category_id = request.POST.get('category_id')
        skill_id = request.POST.get('skill_id')
        proficiency_level = request.POST.get('proficiency_level')
        working_status = request.POST.get('working_status') == 'on'

        skill = get_object_or_404(Skill, pk=skill_id)

        # امنیت: skill باید متعلق به همان category باشد
        if str(skill.skill_category_id.id) != str(category_id):
            return redirect('user_skill')

        user_skill.skill_id = skill
        user_skill.proficiency_level = proficiency_level
        user_skill.working_status = working_status
        user_skill.save()

    return redirect('user_skill')


# user contact
def save_contact(request):
    if request.method == "POST":
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')
        ContactMessage.objects.create(name=name, email=email, message=message)
        return redirect('core:index')
    return render(request, 'core/index.html')


# user logs
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.paginator import Paginator
from django.contrib import messages
from .models import SystemLog


@login_required
@user_passes_test(lambda u: u.is_staff)
def system_logs_list(request):
    # دریافت تمام لاگ‌ها
    logs_list = SystemLog.objects.select_related('action_by', 'content_type').all().order_by('-created_at')

    # قابلیت جستجو
    query = request.GET.get('q')
    if query:
        logs_list = logs_list.filter(object_id__icontains=query)

    # صفحه‌بندی: فقط ۸ تا در هر صفحه
    paginator = Paginator(logs_list, 8)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'users/user_logs/index.html', {'page_obj': page_obj, 'query': query})


@login_required
@user_passes_test(lambda u: u.is_staff)
def delete_log(request, log_id):
    # متد حذف لاگ
    log = get_object_or_404(SystemLog, id=log_id)
    log.delete()
    messages.success(request, "Protokoll erfolgreich gelöscht.")
    return redirect('system_logs_list')