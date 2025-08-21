from django.db import models


class BlogModel(models.Model):
    title = models.CharField(max_length=255)
    image = models.ImageField(upload_to='blogs/')
    content = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'blog'
        verbose_name_plural = 'blogs'
