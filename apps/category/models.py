from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=150)
    slug = models.SlugField(max_length=150,  unique=True)
    parent = models.ForeignKey('self', related_name='children', null=True, blank=True, on_delete=models.CASCADE,
                               default=None)

    def __str__(self):
        if self.parent:
            return f'{self.parent} -> {self.name}'
        return self.name

    @property
    def get_children(self):
        if self.children:
            return self.children.all()
        return False


