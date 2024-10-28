from django.urls import reverse_lazy
from django.shortcuts import render,redirect
from django.views.generic import CreateView, UpdateView, DeleteView, ListView
from django.contrib.auth import login , authenticate , get_user_model , update_session_auth_hash
from .models import Person
from .forms import UserRegisterForm
from django.contrib import messages
from .forms import PersonForm
from .forms import UpdatePersonForm , PersonUpdateProfileForm , CustomPasswordChangeForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required

def register(request):
    if request.user.is_authenticated:
        return redirect('front:indexF')

    if request.method =="POST":
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            
            user = form.save()
            login(request,user)
            
            return redirect("front:indexF")
        else:
            print("Registration failed")
                
    else:        
        form = UserRegisterForm()
        
    return render(request, "frontOffice/person/register.html", {"form":form})


def Login_user(request):
    if request.user.is_authenticated:
        return redirect('front:indexF')

    if request.method=="POST":
        
        username = request.POST['username']
        pwd= request.POST['password']
        
        user = authenticate(request,username=username , password=pwd)
        
        if user is not None:
            login(request,user)
            return redirect("front:indexF")
        
        else:
            messages.info(request,"Username or password incorrect")
            return redirect("login")
        
    else: 
        return render(request, "frontOffice/person/login.html")

# def signin(request):
#     if request.method == 'POST':
#         username = request.POST['username']
#         password = request.POST['password']
#         user = authenticate(request, username=username, password=password)
#         if user is not None:
#             login(request, user)
#             return redirect('back:signin') 
#         else:
#             messages.error(request, 'Please enter the correct username and password for a staff account. Note that both fields may be case-sensitive.')
#             return render(request, 'backOffice/pages/sign-in.html')
            
#     return render(request, 'backOffice/pages/sign-in.html')

class PersonCreateView(CreateView):
    model = Person
    form_class = PersonForm
    template_name = 'BackOffice/pages/person/person_form.html'
    success_url = reverse_lazy('back:list_persons')

class PersonListView(ListView):
    model = Person
    template_name = 'BackOffice/pages/person/person_list.html'
    context_object_name = 'persons'

class PersonUpdateView(UpdateView):
    model = Person
    form_class = UpdatePersonForm
    template_name = 'BackOffice/pages/person/person_form.html'
    success_url = reverse_lazy('back:list_persons')

class PersonDeleteView(DeleteView):
    model = Person
    template_name = 'BackOffice/pages/person/person_confirm_delete.html'
    success_url = reverse_lazy('back:list_persons')

# def get_queryset(self):
#         return Person.objects.all()


@login_required
def settings_view(request):
    user = request.user

    # Changer l'avatar
    if request.method == 'POST' and 'avatar' in request.FILES:
        avatar = request.FILES['avatar']
        user.image = avatar
        user.save()
        messages.success(request, 'Avatar changed successfully!')
        return redirect('back:settings_view')

    # Contexte pour le template
    context = {
        'user': user,
    }

    return render(request, 'BackOffice/pages/settings.html', context)

@login_required
def remove_avatar(request):
    user = request.user
    user.image.delete(save=True)  # Supprimer l'avatar actuel
    messages.success(request, 'Avatar removed successfully!')
    return redirect('back:settings_view')

@login_required
def settingsProfile(request, *args, **kwargs):
    return render(request , 'frontOffice/person/settingsProfile.html')


@login_required
def settingsProfile(request):
    user = request.user  # Obtenez l'utilisateur connecté

    if request.method == 'POST':
        # Vérifiez quel formulaire a été soumis
        if 'update_profile' in request.POST:  # Mise à jour du profil
            form = PersonUpdateProfileForm(request.POST, request.FILES, instance=user)
            if form.is_valid():
                form.save()  # Enregistrez les modifications
                messages.success(request, 'Your profile was successfully updated!')
                return redirect('settingsProfile')
        elif 'change_password' in request.POST:  # Changement de mot de passe
            form = CustomPasswordChangeForm(user=request.user, data=request.POST)
            if form.is_valid():
                form.save()
                update_session_auth_hash(request, form.user)  # Gardez l'utilisateur connecté
                messages.success(request, 'Your password was successfully updated!')
                return redirect('settingsProfile')
            else:
                messages.error(request, 'Please correct the error below.')
    else:
        form = PersonUpdateProfileForm(instance=user)  # Remplissez le formulaire avec les données existantes
        password_form = CustomPasswordChangeForm(user=user)

    return render(request, 'frontOffice/person/settingsProfile.html', {
        'form': form,
        'password_form': password_form,
    })

