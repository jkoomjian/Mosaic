from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from auth.forms import LoginForm
from django.template import RequestContext
from django.forms.util import ErrorList
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout

def login_view(request):
    if request.method == 'POST':
        
        form = LoginForm(request.POST)
        if form.is_valid():

            ##is this a login or sign up
            if form.cleaned_data['submitType'] == "Login":

                #Login
                print 'Login: ' + form.cleaned_data['username']
                user = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password'])
                if user is not None:
                    login(request, user)
                    ##Logged in!
                    print 'logged in user: ' + str(request.user)
                    print 'is authed: ' + str(request.user.is_authenticated())
                    return HttpResponseRedirect('/m/home/')
                else:
                    #Login Failed
                    errors = form._errors.setdefault("username", ErrorList())
                    errors.append(u"Your login info is useless!")
                    return render_to_response('login.html', {'form': form}, context_instance=RequestContext(request))
                
            else:

                #Signup
                if form.cleaned_data['password'] != form.cleaned_data['password2']:
                    errors = form._errors.setdefault("password2", ErrorList())
                    errors.append(u"Passwords do not match!")
                    return render_to_response('login.html', {'form': form}, context_instance=RequestContext(request))
                
                #Create the new user!
                print "username: " + form.cleaned_data['username'] + \
                        " pass1: " + form.cleaned_data['password'] + \
                        " pass2: " + form.cleaned_data['password2']
                user = User.objects.create_user(form.cleaned_data['username'], password=form.cleaned_data['password'])
                #Log in user
                user2 = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password'])
                login(request, user2)
            
                return HttpResponseRedirect('/m/home/')
        else:
            return render_to_response('login.html', {'form': form}, context_instance=RequestContext(request))

    return render_to_response('login.html', {'form': LoginForm()}, context_instance=RequestContext(request))

def logout_view(request):
    logout(request)
    return HttpResponseRedirect('/')