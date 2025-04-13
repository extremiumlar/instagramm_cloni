from django.core.validators import FileExtensionValidator, MaxLengthValidator
from django.db.models import UniqueConstraint

# from django.db.models import UniqueConstraint

from shared.models import BaseModel
from users.models import User
from django.db import models

class Posts(BaseModel):
    author = models.ForeignKey(User, on_delete = models.CASCADE, related_name = 'postlar')
    image = models.ImageField(upload_to = 'post_images', validators=[
        FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png']),
    ])
    caption = models.TextField(validators=[MaxLengthValidator(2000)])
    class Meta:
        db_table = 'posts'
        verbose_name_plural = 'posts'
        verbose_name = 'post'
    def __str__(self):
        return f'{self.author} - {self.caption}'

class PostComments(BaseModel):
    author = models.ForeignKey(User, on_delete = models.CASCADE)
    post = models.ForeignKey(Posts, on_delete = models.CASCADE, related_name = 'post_comments')
    comment = models.TextField(validators=[MaxLengthValidator(2000)])
    parent = models.ForeignKey(
        'self',
        on_delete = models.CASCADE,
        related_name = 'child',
        null = True,
        blank = True,
    )
    def __str__(self):
        return f'{self.author} - {self.comment}'

class PostLike(BaseModel):
    author = models.ForeignKey(User, on_delete = models.CASCADE)
    post = models.ForeignKey(Posts, on_delete = models.CASCADE, related_name = 'post_likes')
    class Meta:
        constraints = [
            UniqueConstraint(fields=['author', 'post'], name='unique_like_post')
        ]
    def __str__(self):
        return f'{self.author} - {self.post}'

class CommentLike(BaseModel):
    author = models.ForeignKey(User, on_delete = models.CASCADE)
    comment = models.ForeignKey(PostComments, on_delete = models.CASCADE, related_name = 'comment_likes')
    class Meta:
        constraints = [
            UniqueConstraint(fields=['author', 'comment'], name='unique_comment_like')
        ]
    def __str__(self):
        return f'{self.author} - {self.comment}'

 











