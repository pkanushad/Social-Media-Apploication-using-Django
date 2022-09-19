from django.db import models
from django.contrib.auth.models import User
import random
# Create your models here.

class UserProfile(models.Model):
    profile_pic=models.ImageField(upload_to="profile_pics",null=True)
    bio=models.CharField(max_length=120)
    phone=models.CharField(max_length=15)
    date_of_birth=models.DateField(null=True)
    options=(
        ("male","male"),
        ("female","female"),
        ("other","other")
    )
    gender=models.CharField(max_length=12,choices=options,default="male")
    user=models.OneToOneField(User,on_delete=models.CASCADE,related_name="users")
    following=models.ManyToManyField(User,related_name="following",blank=True)
    # following
    @property
    def fetch_following(self):
        return self.following.all()

    # following count
    @property
    def fetch_following_count(self):
        return self.fetch_following.count()

    @property
    def get_invitation(self):
        #fetch all UserProfile object except current user
        all_users_profile=UserProfile.objects.all().exclude(user=self.user)
        #taking userobjects from all users
        user_list=[userprofile.user for userprofile in all_users_profile]
        following_list=[user for user in self.fetch_following]
        #exclude myfollowing from all users
        invitations= [user for user in user_list if user not in following_list]
        # return random.sample(invitations,2)
        return invitations
    def get_followers(self):
        all_userprofile=UserProfile.objects.all()
        my_followers=[]
        for profile in all_userprofile:
            if self.user in profile.fetch_following:
                my_followers.append(profile)
        return my_followers
    def my_follower_count(self):
        return len(self.get_followers())



class Blogs(models.Model):
    title= models.CharField(max_length=120)
    description=models.CharField(max_length=230)
    image=models.ImageField(upload_to="blogimages",null=True)
    author=models.ForeignKey(User,on_delete=models.CASCADE,related_name="author")
    posted_date=models.DateTimeField(auto_now=True)
    liked_by=models.ManyToManyField(User)

    @property
    def get_like_count(self):
        like_count=self.liked_by.all().count()
        return like_count

    @property
    def get_liked_users(self):
        liked_users=self.liked_by.all()
        users=[user.username for user in liked_users]
        return users

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "blog"
        verbose_name_plural = "blogs"

class Comments(models.Model):
    blog=models.ForeignKey(Blogs,on_delete=models.CASCADE)
    comment=models.CharField(max_length=160)
    user=models.ForeignKey(User,on_delete=models.CASCADE)

    def __str__(self):
        return self.comment

    class Meta:
        verbose_name = "comment"
        verbose_name_plural = "comments"

# super users =[pkanushad,django,admin]
#        pass- [pkanushad, django,admin@123]
#   newpass -[pkanushad,django@123,admin@123]


