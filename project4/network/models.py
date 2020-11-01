from django.contrib.auth.models import AbstractUser
from django.db import models




class User(AbstractUser):
    pass


class follow(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="follow_info")
    following = models.ForeignKey(User, on_delete=models.CASCADE, related_name="following", null=True, blank=True)
    
    def serialize(self):
        return{
            "user":self.user.username,
            "following": self.following.username,
        }


    def __str__(self):
        return f"\n id : {self.id},\n user_id : {self.user.id},\n user : {self.user},\n following : {self.following}"



class posts(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="usernames")
    content = models.TextField(blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    no_likes = models.IntegerField()

    def serialize(self):
        return {
            "id": self.id,
            "user": self.user.email,
            "content": self.content,
            "no_likes": self.no_likes,
            "timestamp": self.timestamp.strftime("%b %d %Y, %I:%M %p")
    }

    def __str__(self):
        return f"\n id : {self.id},\n user_id : {self.user.id}, user : {self.user},\n content : {self.content},\n timestamp : {self.timestamp},\n likes: {self.no_likes}"



class likes(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="likes")
    post = models.ForeignKey(posts, on_delete=models.CASCADE, related_name="post", null=True, blank=True)

    def serialize(self):
        return{
            "id":self.id,
            "user":self.user.email,
            "post":self.post.serialize()
        }

    def __str__(self):
        return f"\n user : {self.user}"
