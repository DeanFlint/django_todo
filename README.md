Blank template

```sudo pip3 install django```

```django-admin startproject nameOfProject .```

```python3 manage.py runserver $IP:$C9_PORT```

In settings.py, add the C9 host in 'Allowed Hosts'

Click on settings to 'Show home in favorites'

Add the following alias:
```alias run ="python3 ~workspace/manage.py runserver $IP:$C9_PORT"```

Create an app:
``` django-admin startapp todo ```

URLS

In views.py in the new app

```
from django.shortcuts import render, HttpResponse

# Create your views here.
def say_hello(request):
    return HttpResponse("Hello world")
```

In urls.py:

```
from django.contrib import admin
from django.conf.urls import url
from django.urls import path
from todo.views import say_hello

urlpatterns = [
    path('admin/', admin.site.urls),
    url(r'message$', say_hello)
]
```

r = regular expression.

^$ = Everything between these two are needed to show that view.

^ = If you remove the & symbol, any url would work.

message$ = Means that the URL needs to end with message to work.

TEMPLATES

Create templates folder in app. Add a html file.

In views.py, add:

``` 
def get_todo_list(request):
    return render(request, "todo_list.html")
```

Import the app by updating the import statements at the top of the URLs.py:

``` from todo.views import get_todo_list ```

Add the URL to the urlpatterns on URLs.py:

```
urlpatterns = [
    path('admin/', admin.site.urls),
    url(r'^$', get_todo_list)
]
```

In settings.py, add the app in the INSTALLED_APPS array:
``` 

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'todo' <---- Here
]
```

ADMIN

``` 
sqlite3 db.sqlite3
```

If we run:

``` python3 manage.py migrate ```

To create a superuser:

``` python3 manage.py createsuperuser ```

Fill in the details to create the super user.

```.table``` to view tables, ```.quit``` to exit command line.

Run the server and add /admin to the url. Login using the superuser credentials that you've created.

Click on settings to 'Show home in favorites' and create a file called .sqliterc

Add the following:

```
.headers on
.mode column
```

MODELS

In models.py, add the following:

```
# Create your models here.
class Item(models.Model):
    name = models.CharField(max_length=30, blank=False) """Allows string input"""
    done = models.BooleanField(blank=False, default=False) 
    
    def __str__(self):
        return self.name """This gives a the name of the items rather than 'object 1' etc"""
```

Run the following:

```
python3 manage.py makemigrations
```

In the admin.py file, add the import and add the following:

```
from django.contrib import admin
from .models import Item

# Register your models here.
admin.site.register(Item)
```

TABLE

Add the following on todo_list.html:

``` 
<table>
    {% for item in items %}
        <tr>
            {% if item.done %}
            <td><strike>{{item.name}}</strike></td>
            {% else %}
            <td>{{item.name}}</td>
            {% endif %}
        </tr>
        {% empty %} <!-- If empty, display the following... -->
        <p> You have nothing to do.</p>
    {% endfor %}
</table>
```

In views.py, add the following:

```
from django.shortcuts import render, HttpResponse
from .models import Item

# Create your views here.

def get_todo_list(request):
    results = Item.objects.all()
    return render(request, "todo_list.html", {'items': results})
```

CREATE A NEW ITEM

In the todo_list.html, as a link:

``` <a href="add">Add an item</a> ```

Create a new file in templates called ```item_form.html``` and add the following form and button:

```
<form method="POST">
    {% csrf_token %} <!-- To prevent CRSF (which prevents anyone from injecting JS code into input elements) -->
    <label for="id_name">Name:</label><br>
    <input type="text" id="id_name" name="name"/><br>
    <label for="id_done">Done:</label><br>
    <input type="checkbox" id="id_done" name="done"/><br>
    <br>
    <button type="submit">Save</button>
</form>
```

In views.py, import redirect at the top and add the ```create_an_item``` function

```
from django.shortcuts import render, HttpResponse, redirect
from .models import Item

def get_todo_list(request):
    results = Item.objects.all()
    return render(request, "todo_list.html", {'items': results})
    
def create_an_item(request):
    if request.method=="POST":
        new_item = Item() """Create an instance of the item class"""
        new_item.name = request.POST.get('name') """Grab the value from the name form (yet to be created)"""
        new_item.done = 'done' in request.POST """If 'done' is checked (true), otherwise default is false."""
        new_item.save() 
        return redirect(get_todo_list)
    return render(request, "item_form.html")
```

FORMS

Create forms.py and add the following:

``` 
from django import forms
from .models import Item

class ItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ('name', 'done')
```

On item_form.html:

``` 
 <form method="POST">
    {% csrf_token %} <!-- To prevent CRSF (which prevents anyone from injecting JS code into input elements) -->
    
    {{ form.as_p }} <!-- render form as <p></p> -->
    
    <button type="submit">Save</button>
</form>
```

Update views.py:

```
from django.shortcuts import render, HttpResponse, redirect
from .models import Item
from .forms import ItemForm

# Create your views here.

def get_todo_list(request):
    results = Item.objects.all()
    return render(request, "todo_list.html", {'items': results})
    
def create_an_item(request):
    if request.method=="POST":
        form = ItemForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect(get_todo_list)
    else:
        form = ItemForm()
        
    return render(request, "item_form.html", {'form': form})
```

EDIT AN ITEM

On todo_list.html, update the table to the following:

```
<table>
    {% for item in items %}
        <tr>
            {% if item.done %}
            <td><strike>{{item.name}}</strike></td>
            {% else %}
            <td>{{item.name}}</td>
            {% endif %}
            <td>
                <form method="GET" action="edit/{{ item.id }}">
                    <input type="submit" value="Edit">
                </form>
            </td>
        </tr>
        {% empty %} <!-- If empty, display the following... -->
        <p> You have nothing to do.</p>
    {% endfor %}
</table>
```

On views.py, add the ```edit_an_item``` function:

```
def edit_an_item(request, id):
    item = get_object_or_404(Item, pk=id)
    
    if request.method == "POST":
        form = ItemForm(request.POST, instance=item)
        if form.is_valid():
            form.save()
            return redirect(get_todo_list)
    else:
        form = ItemForm(instance=item)
        
    return render(request, "item_form.html", {'form': form})
```

Import ```get_object_or_404``` at the top of the page.

On urls.py, add ```edit_an_item``` from the todo.views import.

Add the following to the ```urlpatterns```:

```
url(r'^edit/(?P<id>\d+)$', edit_an_item)
```
?P = Expression, d+ = digits

HEROKU

``` sudo pip3 install gunicorn ```

``` sudo pip3 install psycopg2 ```

``` pip3 freeze --local > requirements.txt ```

``` heroku create simple-django-todo-df --region eu ``

``` heroku addons:create heroku-postgresql:hobby-dev ```

``` sudo pip3 install dj_database_url ```

``` pip3 freeze --local > requirements.txt ```

On settings.py:

``` 
DATABASES = {
    'default': dj_database_url.parse("postgres://nthcnnczqjuody:4bfb366b7121369efc6739d308f00494a351e8d239ef7acc83bf6a0a374a632e@ec2-54-195-246-59.eu-west-1.compute.amazonaws.com:5432/d6mam7537n10ln")
    }
```

Also, add:

```
import os
import dj_database_url
```

Push to github
``` git push origin master ```

Push to heroku
``` heroku config:set DISABLE_COLLECTSTATIC=1 ```

``` git push heroku master ```

Create a profile

``` echo web: gunicorn django_todo.wsgi:application > Procfile ```

Push Procfile to Github and Heroku.

Change Deployment method to Github on Heroku.

Amend ALLOWED_HOSTS on settings.py

```
ALLOWED_HOSTS = [os.environ.get('C9_HOSTNAME'),
                os.environ.get('HOSTNAME')]
```

Now amend DATABASES:

```
DATABASES = {
    'default': dj_database_url.parse(os.environ.get('DATABASE_URL'))
    }
```

Now when you push to GitHub, this will update Heroku.

Updated this below your imports in settings.py
```
if os.environ.get('DEVELOPMENT'):
    development = True
else: 
    development = False
```

Then update:
```
DEBUG = development
```

And update the default DATABASES:
```
if development:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
        }
    }
else:
    DATABASES = {
        'default': dj_database_url.parse(os.environ.get('DATABASE_URL'))
        }
```

Show Home in Favourites and in .bashrc, add the following at the bottom:
```
export DEVELOPMENT=1
```

Generate a new secret key from https://www.miniwebtool.com/django-secret-key-generator/

Add the new secret key at the bottom of .bashrc:

```
export SECRET_KEY=" < Secret key > "
```

Generate a second secret key and on the cmd line, type the following:

```
heroku config:set SECRET_KEY="<SecretKey>"
```
