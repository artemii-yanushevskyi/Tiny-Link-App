#!/Users/aware/Desktop/Tiny Link App/env/bin/python

import hashlib

def make_users():
    from django.contrib.auth.models import User

    names = ['Maya', 'Jessica', 'Kelvin', 'Jessica', 'Eric', 'Artemii']

    for name in names:
        username = name.lower()
        email = username + '@reasongrace.com'
        try:
            user = User.objects.get(username=username)
            user.set_password('UserPassword2019')
            user.save()
            print("Set a password for a user %s." % user.first_name)
        except User.DoesNotExist:
            user = User.objects.create(username=name.lower(), email=email, first_name=name)
            print("Made a user %s." % user.username)
            user.set_password('UserPassword2019')
            user.save()
            print("Set a password for a user %s." % user.first_name)

def hashing():
    # initializing string 
    string = "http://somelink.com/?example=543545"
    
    # encoding link using encode() 
    # then sending to md5() 
    result = hashlib.md5(string.encode()) 
    
    # printing the equivalent hexadecimal value. 
    print("The hexadecimal equivalent of hash is : ", end ="") 
    print(result.hexdigest()[:4]) 

hashing()