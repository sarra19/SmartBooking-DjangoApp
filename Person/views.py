from django.urls import reverse_lazy
from django.shortcuts import render,redirect
from django.views.generic import CreateView, UpdateView, DeleteView, ListView
from django.contrib.auth import login , authenticate , get_user_model , update_session_auth_hash
from .models import Person
from .forms import UserRegisterForm
from django.contrib import messages
from .forms import PersonForm
from .forms import UpdatePersonForm , PersonUpdateProfileForm , CustomPasswordChangeForm ,  FaceLoginForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.views.generic.edit import FormView
from django.urls import reverse_lazy
from .forms import PasswordResetRequestForm , CustomUserCreationForm
from django.contrib.auth.forms import SetPasswordForm
from django.utils.http import urlsafe_base64_decode
# from django.utils.encoding import force_text
from django.utils.encoding import force_str
from django.views.generic import View
from django.urls import reverse
from django.conf import settings
import http.client
from django.conf import settings
from django.http import JsonResponse
import requests
from django.conf import settings
from django.shortcuts import render, redirect
from django.contrib.auth import login

import google.generativeai as genai
from django.http import HttpResponse, JsonResponse
import json


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
def settingsProfile(request, *args, **kwargs):
    return render(request , 'frontOffice/person/settingsProfile.html')


@login_required
def settingsProfile(request):
    user = request.user  

    if request.method == 'POST':
        if 'update_profile' in request.POST:  
            form = PersonUpdateProfileForm(request.POST, request.FILES, instance=user)
            if form.is_valid():
                form.save()  
                messages.success(request, 'Your profile was successfully updated!')
                return redirect('front:settingsProfile')
        elif 'change_password' in request.POST: 
            password_form = CustomPasswordChangeForm(user=user, data=request.POST)  
            if password_form.is_valid():
                user = password_form.save()  
                update_session_auth_hash(request, user)  
                messages.success(request, 'Your password has been successfully updated !')
                return redirect('front:settingsProfile') 
            else:
                messages.error(request, 'Please correct the error below.')
        elif 'delete_account' in request.POST: 
            user.delete() 
            messages.success(request, 'Your account has been successfully deleted.')
            return redirect('front:indexF')  
    else:
        form = PersonUpdateProfileForm(instance=user)  
        password_form = CustomPasswordChangeForm(user=user)

    return render(request, 'frontOffice/person/settingsProfile.html', {
        'form': form,
        'password_form': password_form,
    })

User = get_user_model()

class PasswordResetRequestView(FormView):
    template_name = 'frontOffice/person/password_reset.html'
    form_class = PasswordResetRequestForm
    success_url = reverse_lazy('password_reset_done')  

    def form_valid(self, form):
        email = form.cleaned_data['email']
        associated_users = User.objects.filter(email=email)
        if associated_users.exists():
            for user in associated_users:
                subject = "Demande de réinitialisation de mot de passe"
                email_template_name = "frontOffice/person/password_reset_email.html"
                context = {
                    "email": user.email,  
                    'domain': get_current_site(self.request).domain,
                    'uid': urlsafe_base64_encode(force_bytes(user.pk)),  
                    'token': default_token_generator.make_token(user),  
                    'protocol': 'http',
                }
                email = render_to_string(email_template_name, context)
                send_mail(subject, email, settings.DEFAULT_FROM_EMAIL, [user.email])  
        print(f"Redirection vers: {self.success_url}")
        return super().form_valid(form)

class PasswordResetConfirmView(View):
    def get(self, request, uidb64, token):
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None

        if user is not None and default_token_generator.check_token(user, token):
            form = SetPasswordForm(user=user)
            return render(request, 'frontOffice/person/password_reset_confirm.html', {'form': form})
        else:
            return redirect('password_reset_invalid')

    def post(self, request, uidb64, token):
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None

        form = SetPasswordForm(user=user, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('password_reset_complete')
        return render(request, 'frontOffice/person/password_reset_confirm.html', {'form': form})

def password_reset_request_view(request):
    if request.method == "POST":
        form = PasswordResetRequestForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data["email"]
            try:
                user = User.objects.get(email=email)
                token = default_token_generator.make_token(user)
                uid = urlsafe_base64_encode(force_bytes(user.pk))
                
                reset_url = request.build_absolute_uri(
                    reverse("password_reset_confirm", args=[uid, token])
                )
                
                subject = "Réinitialisation de votre mot de passe"
                message = render_to_string("frontOffice/person/password_reset_email.html", {
                    "reset_url": reset_url,
                    "user": user,
                })
                
                send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [email])
                return redirect("password_reset_complete")
            except User.DoesNotExist:
                form.add_error("email", "Aucun compte associé à cet email.")
    else:
        form = PasswordResetRequestForm()
    
    return render(request, "frontOffice/person/password_reset_form.html", {"form": form})


def password_reset_done(request):
    return render(request, "frontOffice/person/password_reset_done.html")


# def compare_faces(request):
#     # URL des images pour la comparaison
#     image_url_1 = "https://upload.wikimedia.org/wikipedia/commons/thumb/c/cb/Mohanlal_Viswanathan_Nair_BNC.jpg/240px-Mohanlal_Viswanathan_Nair_BNC.jpg"
#     image_url_2 = "https://www.thenewsminute.com/sites/default/files/styles/news_detail/public/Mohanlal_DN_0.jpg?itok=rosZJnyx"

#     payload = f"""-----011000010111000001101001\r\n
#     Content-Disposition: form-data; name="img_1"\r\n\r\n{image_url_1}\r\n
#     -----011000010111000001101001\r\n
#     Content-Disposition: form-data; name="img_2"\r\n\r\n{image_url_2}\r\n
#     -----011000010111000001101001--\r\n\r\n"""

#     headers = {
#         'x-rapidapi-key': settings.FACEX_API_KEY,
#         'x-rapidapi-host': settings.FACEX_API_HOST,
#         'Content-Type': "multipart/form-data; boundary=---011000010111000001101001",
#         'user_id': settings.FACEX_USER_ID,
#         'user_key': settings.FACEX_USER_KEY
#     }

#     # Connexion et requête
#     conn = http.client.HTTPSConnection(settings.FACEX_API_HOST)
#     conn.request("POST", settings.FACEX_COMPARE_PATH, payload, headers)

#     res = conn.getresponse()
#     data = res.read()
#     conn.close()

#     # Affichage des résultats de l'API
#     return JsonResponse({"result": data.decode("utf-8")})


# def login_with_face(request):
#     if request.method == "POST":
#         # Récupérer l'image soumise par l'utilisateur pour le login
#         face_image = request.FILES['face_image']

#         # URL de l'API et entêtes d’authentification
#         url = "https://facex-facex-v1.p.rapidapi.com/compare_faces"
#         headers = {
#             "x-rapidapi-key": settings.FACEX_API_KEY,
#             "x-rapidapi-host": "facex-facex-v1.p.rapidapi.com",
#             "Content-Type": "multipart/form-data",
#             "user_id": settings.FACEX_USER_ID ,
#             "user_key": settings.FACEX_USER_KEY,
#         }

#         # Parcourir les utilisateurs pour trouver un match avec l’image faciale
#         for person in Person.objects.filter(face_image__isnull=False):
#             files = {
#                 "img_1": face_image,
#                 "img_2": person.face_image.url,  # URL de l’image de référence enregistrée
#             }
            
#             # Envoi de la requête pour comparaison des visages
#             response = requests.post(url, headers=headers, files=files)
            
#             if response.status_code == 200:
#                 result = response.json()
#                 similarity = result.get("similarity", 0)
                
#                 # Authentifier si le pourcentage de similarité est assez élevé
#                 if similarity > 90:  # seuil de similarité ajustable
#                     login(request, person)
#                     return redirect("front:indexF")

#         # Si aucun visage n'est reconnu, afficher une erreur
#         return render(request, "frontOffice/person/login.html", {"error": "Visage non reconnu."})

#     return render(request, "frontOffice/person/login.html")


# # finale hedhy 
# def register(request):
#     if request.method == "POST":
#         form = CustomUserCreationForm(request.POST, request.FILES)  # Inclure request.FILES pour l'upload
#         if form.is_valid():
#             user = form.save()  # Sauvegarde l’utilisateur avec l’image faciale
#             login(request, user)  # Connexion automatique après l’inscription
#             return redirect("front:indexF")  # Redirigez vers la page d'accueil ou une autre page
#     else:
#         form = CustomUserCreationForm()
    
#     return render(request, "frontOffice/person/RegisterFace.html", {"form": form})

# def face_login(request):
#     if request.method == 'POST':
#         form = FaceLoginForm(request.POST, request.FILES)
#         if form.is_valid():
#             face_image = request.FILES.get('face_image')
#             user = authenticate_face(request , face_image)
#             if user:
#                 # Connectez l'utilisateur
#                 login(request, user)
#                 return redirect('front:indexFront')  # Redirigez vers la page d'accueil ou autre
#             else:
#                 error_message = "Reconnaissance faciale échouée. Essayez à nouveau."
#                 return render(request, 'frontOffice/person/face_login.html', {'form': form, 'error_message': error_message})
#     else:
#         form = FaceLoginForm()
#     return render(request, 'frontOffice/person/face_login.html', {'form': form})

# def authenticate_face(request, face_image):
#     url = "https://facex-facex-v1.p.rapidapi.com/compare_faces"
    
#     face_image_data = face_image.read()

#     stored_user_images = Person.objects.all()
#     for user in stored_user_images:
#         if not user.face_image:
#             continue

#         stored_image_url = request.build_absolute_uri(user.face_image.url)

#         querystring = {
#             "face_det": "1"
#         }

#         headers = {
#             "x-rapidapi-key": "0b3b105646mshcb64140d7bd3783p107fadjsndd3d929023bc",
#             "x-rapidapi-host": "facex-facex-v1.p.rapidapi.com",
#             "Content-Type": "multipart/form-data"
#         }

#         response = requests.post(url, data={
#             'img_1': (face_image.name, face_image_data, face_image.content_type),
#             'img_2': (stored_image_url, requests.get(stored_image_url).content, 'image/jpeg')
#         }, headers=headers, params=querystring)

#         print(response.json())  # Affiche la réponse pour déboguer

#         if response.status_code == 200:
#             result = response.json()
#             # Réduisez le seuil de similarité pour tester
#             if result.get('similarity') >= 0.5:
#                 return user

#     return None

################generation de password sécurisé###################
genai.configure(api_key="AIzaSyBU9E_Dbq8rYEjuGPlCvuqPytXMk0N71YU")

def ai_generate_password(keyword):
    model = genai.GenerativeModel("gemini-1.5-flash") #le model gemini qu'on va utiliser
    prompt = f"Generate only a  meaningful in that must contain at least 8 characters, cannot be entirely numeric , with symbols, numbers , and must include the keyword: {keyword}"
    response = model.generate_content(prompt)  
    return response.text

def generate_password(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        keyword = data.get('keyword')
        password1 = ai_generate_password(keyword)
        return JsonResponse({'password1': password1})
    return JsonResponse({'error': 'Invalid request'}, status=400)