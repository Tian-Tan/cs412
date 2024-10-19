# Define the data object for our application
from django.db import models
from django.urls import reverse

# Create your models here.

class Article(models.Model):
    ''' Encapsulate the idea of one Article by some author
    '''

    # data attributes of an Article
    title = models.TextField(blank=False)
    author = models.TextField(blank=False)
    text = models.TextField(blank=False)
    published = models.DateTimeField(auto_now=True)
    # image_url = models.URLField(blank=True)
    image_file = models.ImageField(blank=True)

    def __str__(self):
        ''' Returns a string representation of this object
        '''
        return f'{self.title} by {self.author}'
    
    def get_comments(self):
        '''Returns a QuerySet of all Comments on this Article
        '''
        # Use the ORM to retrieve Comments for which the FK is this Article
        comments = Comment.objects.filter(article=self)
        return comments
    
    def get_absolute_url(self):
        ''' Return the URL that will display an instance of this object
        '''
        # self.pk is the primary key to this article instance
        return reverse('article', kwargs={'pk': self.pk})
    
class Comment(models.Model):
    ''' Encapsulate the idea of a Comment on an Article
    '''
    # Model the 1 to many relationship with Article (foreign key)
    article = models.ForeignKey("Article", on_delete=models.CASCADE)

    author = models.TextField(blank=False)
    text = models.TextField(blank=False)
    published = models.DateTimeField(auto_now=True)

    def __str__(self):
        ''' Returns the string representation of this comment
        '''
        return f'{self.text}'