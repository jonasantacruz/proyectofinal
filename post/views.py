from urllib.parse import quote_plus

from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from .forms import PostForm
from .models import Post

def post_create(request):
    if not request.user.is_staff or not request.user.is_superuser:
        raise Http404
    form = PostForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.user = request.user
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
    if instance.publish > timezone.now().date() or instance.draft:
        if not request.user.is_staff or not request.user.is_superuser:
            raise Http404
    share_string = quote_plus(instance.content)
    context = {
        "title":instance.title,
        "instance": instance,
        "share_string": share_string,
        #s"categoria" : categoria
    }
    return render(request, "post_detail.html", context)

def post_list(request):
    today = timezone.now().date()
    queryset_list = Post.objects.active()#.order_by("-timestamp")
    if request.user.is_staff or request.user.is_superuser:
        queryset_list=Post.objects.all()
    query = request.GET.get("q")
    if query:
        queryset_list = queryset_list.filter(
                Q(title__icontains=query) |
                Q(content__icontains=query) |
                Q(user__first_name__icontains=query) |
                Q(user__last_name__icontains=query)
                ).distinct()
    paginator = Paginator(queryset_list, 2) # Show 25 contacts per page
    page_request_var = "page"
    page = request.GET.get(page_request_var)
    try:
        queryset = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        queryset = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        queryset = paginator.page(paginator.num_pages)


    context = {
        "objects_list": queryset,
        "title":"List",
        "page_request_var": page_request_var,
        "today": today,
    }

    return render(request, "post_list.html", context)

def post_update(request, id=None):
    if not request.user.is_staff or not request.user.is_superuser:
        raise Http404
    instance = get_object_or_404(Post, id=id)
    form = PostForm(request.POST or None, request.FILES or None, instance=instance)
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
    if not request.user.is_staff or not request.user.is_superuser:
        raise Http404
    instance = get_object_or_404(Post, id=id)
    instance.delete()
    messages.success(request, "Se Elimino correctamente")
    return redirect("post:list")
