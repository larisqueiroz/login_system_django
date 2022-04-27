from base64 import urlsafe_b64encode
from unicodedata import name
from django.core.mail import EmailMessage
from lib2to3.pgen2.tokenize import generate_tokens
from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from chat_system import settings
from chat_app.models import Room, Message
from django.core.mail import send_mail
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from . tokens import generate_token

def index(request):
    return render(request, 'index.html')

def signup(request):
    if request.method == "POST":
        firstname = request.POST['1stname']
        lastname = request.POST['lastname']
        email = request.POST['email']
        username = request.POST['username']
        password = request.POST['passwd']
        repeat_passwd = request.POST['repeat_passwd']

        if User.objects.filter(username = username):
            messages.error(request, "Username already exists. Please try another username.")
            return redirect('index')

        if User.objects.filter(email = email).exists():
            messages.error(request, "Email already registered.")
            return redirect('index')

        if len(username) > 10:
            messages.error(request, "Username must have less than 10 characters.")

        if password != repeat_passwd:
            messages.error(request, "Passwords did not match.")

        if not username.isalnum():
            messages.error(request, "Username must have letters and/or numbers only.")
            return redirect('index') 
        
        user = User.objects.create_user(username, email, password)
        user.first_name = firstname
        user.last_name = lastname
        user.is_active = False
        user.save()

        messages.success(request, "Your account was successfully created. A confirmation email was sent to your email account.")

        # EMAIL

        subject = "Welcome to GoChat!"
        message = "Hello " + user.first_name + "! \n" + "Welcome to GoChat! We have sent you a confirmation email, please confirm your email address to activate you account. \n\n Thank you."
        from_email = settings.EMAIL_HOST_USER
        to_list = [user.email]
        send_mail(subject, message, from_email, to_list, fail_silently=True)

        # EMAIL ADDRESS CONFIRMATION EMAIL
        current_site = get_current_site(request)
        email_subject = "Confirm your email - GoChat"
        message2 = render_to_string('email_confirmation.html',{
            
            'name': user.first_name,
            'domain': current_site.domain,
            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            'token': generate_token.make_token(user)
        })

        email = EmailMessage(
        email_subject,
        message2,
        settings.EMAIL_HOST_USER,
        [user.email],
        )
        email.fail_silently = True
        email.send()
        
        return redirect('signin')

    return render(request, 'signup.html')

def signin(request):

    if request.method == "POST":
        username = request.POST['username']
        passwd = request.POST['passwd']

        user = authenticate(username=username, password=passwd)
        user.backend = 'django.contrib.auth.backends.ModelBackend'

        if user is not None:
            login(request, user)
            firstname = user.first_name
            print(request.user.password)
            return render(request, 'index.html', {'first_name': firstname})

        else:
            messages.error(request, "Bad credentials!")
            return redirect('index')
        
    return render(request, 'signin.html')

def signout(request):
    logout(request)
    messages.success(request, "Logged out successfully.")
    return redirect('index')

def activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    
    if user is not None and generate_token.check_token(user, token):
        user.is_active = True
        user.save()
        user.backend = 'django.contrib.auth.backends.ModelBackend'
        login(request, user)
        return redirect('index')
    else:
        return render(request, "activation_failed.html")

def delete(request):
    if request.method == "POST":
        email_acc = request.POST['email']
        
        if User.objects.filter(email = email_acc).exists():
            logout(request)
            User.objects.get(email=email_acc).delete()
            messages.success(request, "Deleted successfully.")
            return redirect('index')

    return render(request, "delete_account.html")

def room(request, room):
    username = request.user.get_username()
    room_details = Room.objects.get(name=room)
    return render(request, 'room.html' , {
        'username': username,
        'room': room,
        'room_details':room_details
    })

def checkview(request):
    room = request.POST['room']
    username = request.user.get_username()

    if Room.objects.filter(name=room).exists():
        return redirect('/' + room+'/?username='+ username)
    else:
        new_room = Room.objects.create(name=room)
        new_room.save()
        return redirect('/' + room+'/?username='+ username)

def send(request):
    message = request.POST['message']
    username = request.POST['username']
    room_id = request.POST['room_id']
    print('room_id: ', room_id)

    new_message = Message.objects.create(message=message, user=username, room=room_id)
    new_message.save()
    return HttpResponse('Message sent successfully.')

def getMessages(request, room):
    room_details = Room.objects.get(name=room)

    messages = Message.objects.filter(room=room_details.id)
    print('MESSAGE!!!!!!!',list(messages.values()))
    return JsonResponse({"messages":list(messages.values())})