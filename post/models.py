from django.db import models
from user.models import User
# Create your models here.
class Post(models.Model):
    class Meta:
        db_table = 'post'
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=256,null=False)
    postdate = models.DateTimeField(null=False)
    author = models.ForeignKey(User)   #创建了一个外键到user表中的

    def __repr__(self):
        return '<Post {}>'.format(self.title)
    __str__ = __repr__

class Content(models.Model):
    class Meta:
        db_table = 'content'
    post = models.OneToOneField(Post)
    content = models.TextField(null=False)
    def __repr__(self):
        return '<Content {}>'.format(self.content[:20])
    __str__ = __repr__