from django.shortcuts import render,redirect
from django.urls import reverse_lazy
from django.contrib.auth.models import User
from blog_app.forms import UserRegistrationForm,LoginForm,UserProfileForm,PasswordResetForm,BlogForm,CommentForm,ProfilepicUpdateForm
from django.views.generic import View,CreateView,FormView,TemplateView,UpdateView
from django.contrib.auth import authenticate,login,logout
from blog_app.models import UserProfile,Blogs,Comments
from django.contrib import messages
from django.core.mail import send_mail
from django.utils.decorators import method_decorator

# Create your views here.

# methode decorator
def signin_required(func):
    def wrapper(request,*args,**kwargs):
        if request.user.is_authenticated:
            return func(request,*args,**kwargs)
        else:
            messages.error(request,"you must login")
            return redirect("sign-in")
    return wrapper


class SignUpView(CreateView):
    form_class=UserRegistrationForm
    template_name="registration.html"
    model=User
    success_url = reverse_lazy("sign-in")

    # send email when registering
    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get("email")
            form.save()
            send_mail(
                'account activation',
                'your account hasbeen created',
                'pkanushad57@gmail.com',
                [email, ],
                fail_silently=False,
            )
            return redirect("sign-in")
        else:
            return render(request, self.template_name, {"form": form})

    # def get(self,request,*args,**kwargs):
    #     form=self.form_class()
    #     return render(request,self.template_name,{"form":form})
    # def post(self,request,*args,**kwargs):
    #     form=self.form_class(request.POST)
    #     if form.is_valid():
    #         form.save()
    #         return redirect("")
    #     else:
    #         return render(request,self.template_name,{"form":form})

# class LoginView(FormView):
#     model=User
#     template_name="login.html"
#     form_class=LoginForm
#
#     # def get(self,request,*args,**kwargs):
#     #     form=self.form_class()
#     #     return render(request,self.template_name,{"form":form})
#     def post(self,request,*args,**kwargs):
#         form=self.form_class(request.POST)
#         if form.is_valid():
#             username=form.cleaned_data.get("username")
#             password=form.cleaned_data.get("password")
#             user=authenticate(request,username=username,password=password)
#             if user:
#                 login(request,user)
#                 print("success")
#                 return redirect("home")
#             else:
#                 return render(request,self.template_name,{"form":form})

@method_decorator(signin_required,name="dispatch")
class IndexView(CreateView):
    template_name = "index.html"
    model = Blogs
    success_url = reverse_lazy("home")
    form_class = BlogForm

    def form_valid(self, form):
        form.instance.author=self.request.user
        self.object=form.save()
        messages.success(self.request,"post has been saved")
        return super().form_valid(form)
    def get_context_data(self, **kwargs):
        context=super().get_context_data(**kwargs)
        blogs=Blogs.objects.all().order_by("-posted_date")
        context["blogs"]=blogs
        comment_form=CommentForm()
        context["comment_form"]=comment_form
        return context

@method_decorator(signin_required,name="dispatch")
class CreateUserProfileView(CreateView):
    model = UserProfile
    template_name = "add-profile.html"
    form_class = UserProfileForm
    success_url = reverse_lazy("home")

    def form_valid(self, form):
        form.instance.user= self.request.user
        messages.success(self.request,"profile hasbeen added")
        self.object = form.save()
        return super().form_valid(form)

    # def post(self,request,*args,**kwargs):
    #     form= self.form_class(request.POST,files=request.FILES)
    #     if form.is_valid():
    #         form.instance.user=request.user
    #         form.save()
    #         messages.success(self.request,"profile hasbeen created")
    #         return redirect("home")
    #     else:
    #         return render(request,self.template_name,{"form":form})


@method_decorator(signin_required,name="dispatch")
class ViewProfileView(TemplateView):
    template_name = "view-profile.html"

@method_decorator(signin_required,name="dispatch")
class PasswordResetView(FormView):
    template_name = "password-reset.html"
    form_class = PasswordResetForm

    def post(self, request, *args, **kwargs):
        form=self.form_class(request.POST)
        if form.is_valid():
            oldpassword=form.cleaned_data.get("old_password")
            password1=form.cleaned_data.get("new_password")
            password2 = form.cleaned_data.get("confirm_password")
            user= authenticate(request,username=request.user.username,password=oldpassword)
            if user:
                user.set_password(password2)
                user.save()
                messages.success(request,"password changed successfully")
                return redirect("sign-in")
            else:
                messages.error(request,"invalid-credentials")
                return render(request,self.template_name,{"form":form})

@method_decorator(signin_required,name="dispatch")
class ProfileUpdateView(UpdateView):
    model = UserProfile
    form_class = UserProfileForm
    template_name = "profile-update.html"
    success_url = reverse_lazy("home")
    pk_url_kwarg = "user_id"

    def form_valid(self, form):
        messages.success(self.request,"your profile hasbeen updated successfully")
        self.object=form.save()
        return super().form_valid(form)

@method_decorator(signin_required,name="dispatch")
class ProfilepicUpdateView(UpdateView):
    form_class = ProfilepicUpdateForm
    template_name = "propic-update.html"
    model = UserProfile
    success_url = reverse_lazy("home")
    pk_url_kwarg = "user_id"

    def form_valid(self, form):
        messages.success(self.request,"profile pic hasbeen updated")
        self.object = form.save()
        return super().form_valid(form)


def add_comment(request,*args,**kwargs):
    if request.method=='POST':

        blog_id= kwargs.get("post_id")
        blog=Blogs.objects.get(id=blog_id)
        user=request.user
        comment= request.POST.get("comment")
        Comments.objects.create(blog=blog,comment=comment,user=user)
        messages.success(request,"comment has been posted")
        return redirect('home')

def add_likes(request,*args,**kwargs):
    blog_id=kwargs.get('post_id')
    blog=Blogs.objects.get(id=blog_id)
    blog.liked_by.add(request.user)
    blog.save()
    return redirect("home")

def follow_friend(request,*args,**kwargs):
    # follower_id=kwargs.get("user_id")
    # user_profile=UserProfile.objects.get(user=request.user)
    # follower = User.objects.get(id=follower_id)
    # user_profile.following.add(follower)
    # messages.success(request, "you are started following")
    friend_id = kwargs.get("user_id")
    friend_profile=User.objects.get(id=friend_id)
    request.user.users.following.add(friend_profile)
    friend_profile.save()
    messages.success(request,"you are started following," +friend_profile.username)
    return redirect("home")

# def remove_comment(request,*args,**kwargs):
#     comnt_id=kwargs.get('post_id')
#     blog = Blogs.objects.get(id=comnt_id)
#     user = request.user
#     comment = request.POST.get("comment")
#     Comments.objects.delete(blog=blog, comment=comment, user=user)
#     messages.success(request, "comment has been posted")
#     return redirect("home")


def sign_out(request,*args,**kwargs):
    logout(request)
    return redirect("sign-in")

# custom login
class LoginView(FormView):
    model=User
    template_name="login2.html"
    form_class=LoginForm

    def post(self,request,*args,**kwargs):
        form=self.form_class(request.POST)
        if form.is_valid():
            username=form.cleaned_data.get("username")
            password=form.cleaned_data.get("password")
            user=authenticate(request,username=username,password=password)
            if user:
                login(request,user)
                print("success")
                return redirect("home")
            else:
                return render(request,self.template_name,{"form":form})
