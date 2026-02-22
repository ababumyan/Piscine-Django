from django.db import models

# Create your models here.
class Movies(models.Model):
    episode_nb = models.AutoField(primary_key=True)
    title = models.CharField(max_length=64, unique=True, null=False)
    opening_crawl = models.TextField()
    director = models.CharField(max_length=64, null=False)
    producer = models.CharField(max_length=128, null=False)
    release_date = models.DateField(null=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    
    def update_opening_crawl(self, new_opening_crawl):
        self.opening_crawl = new_opening_crawl
        self.save()

    def __str__(self):
        return self.title