from django.shortcuts import render, HttpResponse, redirect
from home.models import Contact
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from blog.models import Post

# Create your views here.
def home(request):
    return render(request, 'home/home.html')
    
def about(request):
    return render(request, 'home/about.html')

def contact(request):
    if request.method=='POST':
        name = request.POST['name']
        email = request.POST['email']
        phone = request.POST['phone']
        content = request.POST['content']

        if len(name)<2 or len(email)<3 or len(phone)<10 or len(content)<4:
            messages.error(request, "PLease fill the details correctly.")
        else:
            contact = Contact(name=name, email=email, phone=phone, content=content)
            contact.save()
            messages.success(request, "Your form has been successfully sent.")
    return render(request, 'home/contact.html')

# Handle Search Functionality
def search(request):
    query = request.GET['query']
    if len(query)>70:
        allPosts = Post.objects.none()
    else:
        allPostsTitle = Post.objects.filter(title__icontains=query)
        allPostsContent = Post.objects.filter(content__icontains=query)
        allPosts = allPostsTitle.union(allPostsContent)

    if allPosts.count() == 0:
        messages.warning(request, "No search results found. Please refine your query.")
    params = {'allPosts': allPosts, 'query': query}
    return render(request, 'home/search.html', params)

# Handle Signup Page
def handleSignup(request):
    # Get the post parameters
    if request.method == 'POST':
        username = request.POST['username']
        fname = request.POST['fname']
        lname = request.POST['lname']
        email = request.POST['email']
        pass1 = request.POST['pass1']
        pass2 = request.POST['pass2']

        #Check for errorneous inputs
        if len(username) > 10:
            messages.error(request, "Username must be under 10 characters")
            return redirect('home')
        if not username.isalnum():
            messages.error(request, "Username must contain only letters and numbers")
            return redirect('home')
        if (pass1 != pass2):
            messages.error(request, "Password do not match")
            return redirect('home')

        #Create the user
        myuser = User.objects.create_user(username, email, pass1)
        myuser.fname = fname
        myuser.lname = lname
        myuser.save()
        messages.success(request, "Your account has been created successfully.")
        return redirect('home')        #Redirect to home (home = /)

    else:
        return HttpResponse("404 - Page not found")

# Handle Login Page
def handleLogin(request):
    if request.method == 'POST':
        #Get the post parameters
        loginemail = request.POST['loginemail']
        loginpassword = request.POST['loginpassword']
        username = User.objects.get(email=loginemail.lower()).username
        user = authenticate(username=username, password=loginpassword)

        if user is not None:
            login(request, user)
            messages.success(request, "Successfully Logged In")
            return redirect('home')
        else:
            messages.error(request, "Invalid credentials")
            return redirect('home')

    return HttpResponse("404 - Page not found")

# Handle Logout Page
def handleLogout(request):
    logout(request)
    messages.success(request, "Successfully Logged Out")
    return redirect('home')

    