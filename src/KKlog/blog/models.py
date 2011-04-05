from django.db import models
from datetime import datetime
 
class Category(models.Model):
    name = models.CharField(max_length=60)
    
    def __unicode__(self):
        return self.name
 
class Post(models.Model):
    title = models.CharField(max_length=120)
    slug = models.SlugField(max_length=120, unique=True)
    body = models.TextField()
    published = models.DateTimeField(default=datetime.now)
    categories = models.ManyToManyField(Category)
    
    def __unicode__(self):
        return self.title
    
    
class Comment(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    author = models.CharField(max_length=60)
    body = models.TextField()
    post = models.ForeignKey(Post)

    def __unicode__(self):
        return unicode("%s: %s" % (self.post, self.body[:60]))
