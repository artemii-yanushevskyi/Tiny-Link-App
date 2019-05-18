from django.shortcuts import render
from .forms import LoginForm
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from .models import Link
from django.utils import timezone
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from random import randint
import hashlib 

from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from django.shortcuts import get_object_or_404


def index(request):
    if not request.user.is_authenticated:
        # return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))
        return HttpResponseRedirect('/login/')

    name = str(request.user.first_name)
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
                return HttpResponseRedirect('/')
            else:
                return render(request, 'login.html', {'form': form, 'invalid': True})
    else:
        form = LoginForm()

    return render(request, 'login.html', {'form': form, 'invalid': False})


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
    return HttpResponseRedirect('/')

def tinylink_dispacher(request, hash):
    print('Received hash %s. Redirecting...' % hash)
    try:
        redirect_url = Link.objects.get(tiny=hash)
        redirect_url.count += 1
        redirect_url.save()

    except Link.DoesNotExist:
        return render(request, 'tinylink/match_error.html', {
            'hash': hash,
        })

    return HttpResponseRedirect('https://' + redirect_url.original)

def stats(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect('/login/')

    name = str(request.user.first_name)
    
    user = request.user
    user_id = user.pk

    # any permission check will cache the current set of permissions
    print('does user %s has permission "tinylink.view_link"?' % name, user.has_perm('tinylink.view_link'))

    content_type = ContentType.objects.get_for_model(Link)
    permission = Permission.objects.get(
        codename='view_link',
        content_type=content_type,
    )
    user.user_permissions.add(permission)

    # Checking the cached permission set
    print('does user %s has permission "tinylink.view_link"?' % name, user.has_perm('tinylink.view_link'))
    # False

    # Request new instance of User
    # Be aware that user.refresh_from_db() won't clear the cache.
    user = get_object_or_404(User, pk=user_id)

    # Permission cache is repopulated from the database
    print('does user %s has permission "tinylink.view_link"?' % name, user.has_perm('tinylink.view_link'))  # True

    links = Link.objects.order_by('-created')

    return render(request, 'tinylink/stats.html', {
        'permission': 'have' if user.has_perm('tinylink.view_link') else "don't have",
        'links': links,
        'name': name,
        'time': timezone.now(),
    })