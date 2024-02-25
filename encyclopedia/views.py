from django.shortcuts import render
from markdown2 import Markdown
import random

from . import util


# Check for a valid markdown file 
def check_convert(title):
        
     content = util.get_entry(title)
     markdowner = Markdown()

     # Check for a valid entry
     if content == None:
          return None
     else:
          # If the entry is a valid one, convert the .md to an HTML file 
          return markdowner.convert(content)


# Main page
def index(request):
    
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })


# Render the entry pages 
def entry(request, title):

     content = check_convert(title)

     # Check if the content is valid or not 
     if content == None:
        # If the content is not valid render an error page 
        return render(request, "encyclopedia/error.html", {
             "message": "This entry does not exist"
        })
     else:
        return render(request, "encyclopedia/entry.html", {
             "title" : title,
             "content": content
        })
    

# Define the search algorithm
def search(request):
     if request.method == "POST":
          # Stores the query from the form named q
          data = request.POST['q']
          content = check_convert(data)
        
          # If the content ( entry ) exist, return the page   
          if content is not None:
               return render (request, "encyclopedia/entry.html", {
                    "title": data,
                    "content": content
               })
          
          else:
               allEntries = util.list_entries()
               recommendations = []

               for entry in allEntries:
                    if data.lower() in entry.lower():
                         recommendations.append(entry)
               return render(request, "encyclopedia/search.html", {
                    "recommendations": recommendations
               })
                        

def new_page(request):

     if request.method == "GET":
          return render(request, "encyclopedia/new.html")
     # Working with the POST method
     else:
          # Stores the title and the content from the HTML form into variables 
          title = request.POST['title']
          content = request.POST['content']

          # Check if the entry already exist 
          check = util.get_entry(title)

          if check is not None:
               return render(request, "encyclopedia/error.html", {
                    "message": "Entry page already exists"
               })
          else:
                  
               # If the entry is new, save it
               util.save_entry(title, content)

               # Redirect the user to the new page
               page = check_convert(title)
               return render(request, "encyclopedia/entry.html", {
                    "title":title,
                    "content": page
               })


def edit(request):
     if request.method == "POST":
          title = request.POST['entry_title']
          content = util.get_entry(title)
          return render(request, "encyclopedia/edit.html", {
               "title": title,
               "content": content
          })


def save(request):
     if request.method == "POST":
          title = request.POST['title']
          content = request.POST['content']
          util.save_entry(title, content)

          page = check_convert(title)

          return render(request, "encyclopedia/entry.html", {
               "title": title,
               "content": page
          })
     
def random_page(request):
     allEntries = util.list_entries()
     random_entry = random.choice(allEntries)
     content = check_convert(random_entry)

     return render(request, "encyclopedia/entry.html", {
          "title": random_entry,
          "content": content
     })