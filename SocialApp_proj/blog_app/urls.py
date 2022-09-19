from django.contrib import admin
from django.urls import path,include
from blog_app import views

urlpatterns = [
    path("accounts/signup",views.SignUpView.as_view(),name="sign-up"),
    path("accounts/signin",views.LoginView.as_view(),name="sign-in"),
    path("home",views.IndexView.as_view(),name="home"),
    path("users/profile/add",views.CreateUserProfileView.as_view(),name="add-profile"),
    # testing code
    path("users/profiles",views.ViewProfileView.as_view(),name="view-my-profile"),
    path("users/password/change",views.PasswordResetView.as_view(),name="password-reset"),
    path("users/profile/change/<int:user_id>",views.ProfileUpdateView.as_view(),name="profile-update"),
    path('users/prof_pic/change/<int:user_id>',views.ProfilepicUpdateView.as_view(),name="pic-change"),
    path('post/comment/<int:post_id>',views.add_comment,name="add-comment"),
    path('post/like/add/<int:post_id>',views.add_likes,name="add-like"),
    path('users/follow/<int:user_id>',views.follow_friend,name="follow-friend"),
    path("accounts/signout", views.sign_out, name="sign-out"),
    # path('remove/comment',views.remove_comment,name="cmd-remove"),
]