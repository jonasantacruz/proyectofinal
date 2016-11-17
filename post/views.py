from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect

from .forms import PostForm
from .models import Post

def post_create(request):
    form = PostForm(request.POST or None)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.save()
        #messages success
        messages.success(request, "Guardado")
        return HttpResponseRedirect(instance.get_absolute_url())
    else:
        messages.error(request, "No Guardado")
    #if request.method == "POST":
    #    print ("title" + request.POST.get("content"))
    #    print (request.POST.get("title"))
    #    #Post.objects.create(title=title)
    context = {
        "form": form,
    }
    return render(request, "post_form.html", context)

def post_detail(request, id=None): #retrive
    instance = get_object_or_404(Post, id=id)
    context = {
        "title":instance.title,
        "instance": instance
    }
    return render(request, "post_detail.html", context)

def post_list(request):
    queryset = Post.objects.all()
    context = {
        "objects_list": queryset,
        "title":"List"
        }

    return render(request, "post_list.html", context)

def post_update(request, id=None):
    instance = get_object_or_404(Post, id=id)
    form = PostForm(request.POST or None, instance=instance)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.save()
        messages.success(request, "Se Edito correctamente")
        #messages success
        return HttpResponseRedirect(instance.get_absolute_url())

    context = {
        "title":instance.title,
        "instance": instance,
        "form": form,
    }
    return render(request, "post_form.html", context)


def post_delete(request, id=None):
    instance = get_object_or_404(Post, id=id)
    instance.delete()
    messages.success(request, "Se Elimino correctamente")
    return redirect("post:list")
