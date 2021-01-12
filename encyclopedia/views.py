from django.shortcuts import render
from django import forms
from django.http import HttpResponse, HttpResponseRedirect

from . import util

from random import randint

# Initializes object known as Markdown, which allows you to to convert text to HTML and back to string via Markdown.

class searchBarForm(forms.Form):
    query = forms.CharField(label="Search:")

class createPageForm(forms.Form):
    title = forms.CharField(label="Enter the Title:")
    content = forms.CharField(widget = 
    forms.Textarea(attrs={"placeholder": 'Enter Content in Markdown here...'}))


def index(request):
    form = searchBarForm()
    return render(request, "encyclopedia/index.html", {
        "form": form,
        "entries": util.list_entries()
    })

def entry(request, title):
    content = util.get_entry(title)
    if content is None:
        form = searchBarForm()
        message = "File entered is not available."
        return render(request, 'encyclopedia/error.html', {
            "form": form,
            "message": message,
        })
    else:
        form = searchBarForm()
        content = util.get_entry(title)
        return render(request, 'encyclopedia/entry.html', {
            "form": form,
            "title": title,
            "content": content,
        })

def search(request):
    if request.method == "POST":
        form = searchBarForm(request.POST)
        if form.is_valid():
            q = form.cleaned_data["query"]
            # States the status of found
            present = False

            for i in util.list_entries():
                # iterates through, stating found or not
                if q.lower() == i.lower():
                    content = util.get_entry(i)
                    present = True 
                    break
            
            if present:
                return render(request, "encyclopedia/entry.html", {
                    "title": q,
                    "form": form,
                    "content": content,
                })

            else:
                files = []
                for i in util.list_entries():
                    if q.lower() in i.lower():
                        files.append(i)
                
                if len(files) == 0:
                    message = "File not found, please search for another entry"
                    return render(request, "encyclopedia/error.html", {
                        "form": form,
                        "message": message,
                    })
                else:
                    return render(request, "encyclopedia/index.html", {
                        "form": form,
                        "entries": files,
                    })

    else: 
        form = searchBarForm()
        message = "Please look for something in order to find a page"
        return render(request, "encyclopedia/error.html", {
            "form": form,
            "message": message,
        })

def create(request):
    if request.method == "POST":
        form = searchBarForm()
        createForm = createPageForm(request.POST)
        if createForm.is_valid():
            title = createForm.cleaned_data["title"]
            content = createForm.cleaned_data["content"]
            present = False

            for entry in util.list_entries():
                if title.lower() == entry.lower():
                    present = True
                    break
            
            if present:
                message = "This entry already exists, please go and edit the netry instead of creating a new one."
                return render(request, "encyclopedia/error.html", {
                    "form": form,
                    "message": message,
                })
            
            else:
                util.save_entry(title, content)
                newcontent = util.get_entry(title)
                return render(request, "encyclopedia/entry.html", {
                    "title": title,
                    "form": form,
                    "content": newcontent,
                })

    else:
        form = searchBarForm()
        createForm = createPageForm()
        return render(request, "encyclopedia/create.html", {
            "form": form,
            "createForm": createForm,
        })

def edit(request, title):
    if request.method == "POST":
        form = searchBarForm
        contentForm = createPageForm(request.POST)
        if contentForm.is_valid():
            newtitle = contentForm.cleaned_data["title"]
            newcontent = contentForm.cleaned_data["content"]

            if newtitle.lower() == title.lower():
                util.save_entry(newtitle, newcontent)
                newcontent = util.get_entry(newtitle)
                return render(request, "encyclopedia/entry.html", {
                    "title": title,
                    "form": form,
                    "content": newcontent,
                })
            
            else:
                util.save_entry(newtitle, newcontent)
                util.delete_entry(title)
                loadedcontent = util.get_entry(newtitle)
                return render(request, "encyclopedia/entry.html", {
                    "title": newtitle,
                    "form": form,
                    "content": loadedcontent,
                })

    else:
        loadedcontent = util.get_entry(title)
        form = searchBarForm()
        editForm = createPageForm({"title": title, "content": loadedcontent})

        return render(request, "encyclopedia/edit.html", {
            "title": title,
            "form": form,
            "editForm": editForm,
        })

def randompage(request):
    form = searchBarForm()
    entries = util.list_entries()
    index = randint(0, len(entries)-1)

    title = entries[index]
    content = util.get_entry(title)

    return render(request, "encyclopedia/entry.html", {
        "title": title,
        "form": form,
        "content": content,
    })
