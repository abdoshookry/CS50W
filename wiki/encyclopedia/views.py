from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponseRedirect
from markdown2 import Markdown
import random

from . import util


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def Entry_Page(request,title):
    entry = util.get_entry(title)
    html = Markdown_to_HTML_Conversion(entry)
    return render(request, "encyclopedia/entry page.html", {
    "entry": html,
    "title": title
    })


def search(request):
    query = request.GET['q']
    if util.get_entry(query):
        return HttpResponseRedirect(reverse("entry", args=(query,)))
    else:
      return render(request, "encyclopedia/index.html", {
        "entries": [entry for entry in util.list_entries() if query.lower() in entry.lower()]
      }) 
      
def new_page(request):
    return render(request, "encyclopedia/new page.html")


def save(request):
    title = request.POST['title']
    content = request.POST['content']
    entries = util.list_entries()
    for x in range(len(util.list_entries())):
        if title.lower() in entries[x].lower():
            return render(request, "encyclopedia/saving error.html", {
            "title": title
            })

    util.save_entry (title,content)
    return HttpResponseRedirect(reverse("entry", args=(title,)))
    
def edit(request,title):
    content = util.get_entry(title)
    return render(request, "encyclopedia/edit page.html", {
        "title":title,
        "content": content
    })

def save_edit(request):
    title = request.POST['title']
    content = request.POST['content']
    util.save_entry (title,content)
    return HttpResponseRedirect(reverse("entry", args=(title,)))

def random_page(request):
    entry_title = random.choice(util.list_entries())
    return HttpResponseRedirect(reverse("entry", args=(entry_title,)))

def Markdown_to_HTML_Conversion(file):
    if file :
        markdowner = Markdown()
        return markdowner.convert(file)
    else :
        return file
        


