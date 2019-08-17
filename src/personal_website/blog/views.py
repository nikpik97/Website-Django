import urllib
import json
from django.conf import settings
from django.contrib import messages

from django.shortcuts import render
from blog.forms import CommentForm
from blog.models import Post, Comment
# Create your views here.


def blog_index(request):
    posts = Post.objects.all().order_by('-created_on')
    context = {"posts": posts}
    return render(request, "blog_index.html", context)


def blog_category(request, category):
    posts = Post.objects.filter(categories__name__contains=category).order_by('-created_on')
    context = {"category": category, "posts": posts}
    return render(request, "blog_category.html", context)


def blog_detail(request, pk):
    post = Post.objects.get(pk=pk)
    form = CommentForm()
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            ''' Begin reCAPTCHA validation '''
            recaptcha_response = request.POST.get('g-recaptcha-response')
            url = 'https://www.google.com/recaptcha/api/siteverify'
            values = {
                'secret': settings.GOOGLE_RECAPTCHA_SECRET_KEY,
                'response': recaptcha_response
            }
            data = urllib.parse.urlencode(values).encode()
            req =  urllib.request.Request(url, data=data)
            response = urllib.request.urlopen(req)
            result = json.loads(response.read().decode())
            ''' End reCAPTCHA validation '''
            print(result)
            if result['success']:
                comment = Comment(author=form.cleaned_data["author"], body=form.cleaned_data["body"], post=post)
                comment.save()
                messages.success(request, 'New comment added with success!')
                print("error")
            else:
                print("error")
                messages.error(request, 'Invalid reCAPTCHA. Please try again.')

    comments = Comment.objects.filter(post=post)
    context = {"post": post,"comments": comments,"form": form}
    return render(request, "blog_detail.html", context)  