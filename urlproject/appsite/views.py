import short_url
from cProfile import Profile

from django.shortcuts import render, get_object_or_404
from django.urls import include
import random, string, json
from appsite.models import Urls
from django.http import HttpResponseRedirect, HttpResponse
from django.conf import settings
from django.views.generic import View
from datetime import datetime
from .forms import NameForm, RegistrationForm, UrlForm
import csrf
import short_url


class UrlView(View):
    template_name = 'url.html'

    def get(self, request):
        form = UrlForm()
        return render (request, self.template_name, {'form':form})

    def post(self,request):
        form = UrlForm(request.POST)
        if form.is_valid():
            httpurl = form.cleaned_data.get('url')
            short_id = short_url.encode_url(httpurl)
            pub_date = datetime.today()
            urls_short = Urls.objects.create(short_id=short_id, httpurl=httpurl, pub_date=pub_date)
            return HttpResponse('Ok', content_type='text/plain')

        return HttpResponse('error', content_type='text/plain')

class RegistrationView(View):
    template_name = 'registration.html'

    def get(self, request):
        form = RegistrationForm()
        return render (request, self.template_name, {'form':form})

    def post(self,request):
        form = RegistrationForm(request.POST)
        data = request.POST
        user = data['user_name']
        email = data['email_id']
        password = data["password"]
        password_retype= data['password_retype']
        # if form.is_valid():
        #     if Profile.object.filter(username=user).exists() is False and password == password_retype:
        #         profile = Profile.object.create(username = user, email = email, is_active = False)
        #         profile.set_password(password)
        #         profile.save()
        #         return HttpResponse('Ok', content_type='text/plain')

        return HttpResponse('error', content_type='text/plain')


def index(request):
    c = {}
    c.update(csrf(request))
    return render('appsite/index.html', c)

def redirect_original(request, short_id):
    url = get_object_or_404(Urls, pk=short_id) # get object, if not        found return 404 error
    url.count += 1
    url.save()
    return HttpResponseRedirect(url.httpurl)

def shorten_url(request):
    url = request.POST.get("url", '')
    if not (url == ''):
        short_id = get_short_code()
        b = Urls(httpurl=url, short_id=short_id)
        b.save()

        response_data = {}
        response_data['url'] = settings.SITE_URL + "/" + short_id
        return HttpResponse(json.dumps(response_data),  content_type="application/json")
    return HttpResponse(json.dumps({"error": "error occurs"}), content_type="application/json")

def get_short_code():
    length = 6
    char = string.ascii_uppercase + string.digits + string.ascii_lowercase
    # if the randomly generated short_id is used then generate next
    while True:
        short_id = ''.join(random.choice(char) for x in range(length))
        try:
            temp = Urls.objects.get(pk=short_id)
        except:
            return short_id
