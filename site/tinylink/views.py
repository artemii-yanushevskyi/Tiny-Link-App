from django.shortcuts import render
from .forms import LoginForm
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from .models import Link
from django.utils import timezone
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from random import randint
import hashlib 


# Create your views here.
def index(request):
    if not request.user.is_authenticated:
        # return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))
        return HttpResponseRedirect('login')

    name = str(request.user.first_name)
    user = User.objects.get(username=request.user.username)
    try:
        links = Link.objects.filter(user=request.user).order_by('-created')
    except Link.DoesNotExist:
        links = None

    return render(request, 'tinylink/index.html', {
        'links': links,
        'name': name,
        'time': timezone.now(),
    })

def login_user(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = LoginForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            username = request.POST['username'].lower()
            password = request.POST['password']
            print(username, password)
            user = authenticate(request, username=username, password=password)
            print(user)
            if user is not None:
                login(request, user)
                return HttpResponseRedirect('/tiny/')
            else:
                return HttpResponse("Can not log in.")
    else:
        form = LoginForm()

    return render(request, 'login.html', {'form': form})


def make_link(request):
    '''make and register link
    '''
    def azAZhash(length, string):
        h = hashlib.sha1(string.encode())
        d = h.digest()
        s = ""
        for i in range(tinylink_length):
            x = d[i] % 52
            if x >= 26:
                s += chr(ord('A') + x - 26)
            else:
                s += chr(ord('a') + x)
        return s

    username = request.user.username
    link = request.POST['originallink']

    if len(link.split('//')) == 2:
        # in case we have 'http(s)://' at the beginning
        link = link.split('//')[1]

    u = User.objects.get(username=username)

    tinylink_length = 2
    origlink = link
    tinylink = azAZhash(tinylink_length, origlink)

    while Link.objects.filter(tiny=tinylink): 
        print("Tinylink exists, looking for a new '%s'..." % tinylink)
        origlink += 'extra' 
        tinylink = azAZhash(tinylink_length, origlink)
    else:
        print("Creating a new link. The hexadecimal equivalent of hash is: '%s'." % tinylink)

    l = Link.objects.create(user=u, original=link, tiny=tinylink)

    data = {
        'exists': False,
        'name': User.objects.get(username=username).first_name,
        'tinylink': l.tiny,
        'originallink': link,
    }
    
    return JsonResponse(data)

def logout_view(request):
    logout(request)
    return HttpResponseRedirect('/tiny/')

def tinylink_dispacher(request, hash):
    print('Received hash %s. Redirecting...' % hash)
    try:
        redirect_url = Link.objects.get(tiny=hash)
        redirect_url.count += 1
        redirect_url.save()

    except Link.DoesNotExist:
        return HttpResponse('<h1>The hash has not been mached</h1>')

    return HttpResponseRedirect('https://' + redirect_url.original)