from rest_framework import generics, status
from rest_framework.exceptions import ValidationError

from rest_framework.permissions import IsAuthenticated, AllowAny, IsAuthenticatedOrReadOnly
from rest_framework.response import Response

from .models import Posts, PostLike , PostComments, CommentLike

from .serializers import PostSerializer , PostLikeSerializer, CommentLikeSerializer, CommentSerializer

from shared.custom_pagination import CustomPagination

class PostListAPIView(generics.ListAPIView):
    serializer_class = PostSerializer
    permission_classes = [AllowAny, ]
    pagination_class = CustomPagination
    queryset = Posts.objects.all()

class PostCreateView(generics.CreateAPIView):
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated, ]
    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

class PostRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Posts.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, ]

    def put(self, request, *args, **kwargs):
        post = self.get_object()
        serializer = self.serializer_class(post, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({
            "success": True,
            "kod": status.HTTP_200_OK,
            "message": "Post successfully updated",
            "data": serializer.data,
        })
    def delete(self, request, *args, **kwargs):
        post = self.get_object()
        post.delete()
        return Response({
            "success": True,
            "kod": status.HTTP_204_NO_CONTENT,
            "message": "Post successfully deleted",
        })

class PostCommentListView(generics.ListAPIView):
    serializer_class = CommentSerializer
    permission_classes = [AllowAny, ]

    def get_queryset(self):
        post_id = self.kwargs['pk']
        # Bu boshqacha yo'li releted_name ishlatilgan yo'li
        # post = Posts.objects.get(pk=post_id)
        # queryset = post.post_comments.all()
        queryset = PostComments.objects.filter(post__id=post_id)
        return queryset

class PostCommentCreateView(generics.CreateAPIView):
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated, ]

    def perform_create(self, serializer):
        post_id = self.kwargs['pk']
        serializer.save(post_id=post_id, author=self.request.user)

class PostCommentListCreateView(generics.ListCreateAPIView):
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, ]
    queryset = PostComments.objects.all()
    pagination_class = CustomPagination

    def get_queryset(self):
        return self.queryset
    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

class PostLikeListView(generics.ListAPIView):
    serializer_class = PostLikeSerializer
    permisson_classes = [AllowAny, ]

    def get_queryset(self):
        post_id = self.kwargs['pk']
        queryset = PostLike.objects.filter(post_id = post_id)
        return queryset

class CommentRetrieveAPIView(generics.RetrieveAPIView):
    serializer_class = CommentSerializer
    permission_classes = [AllowAny, ]
    queryset = PostComments.objects.all()

class CommentLikeAPIView(generics.ListAPIView):
    serializer_class = CommentLikeSerializer
    permission_classes = [AllowAny, ]

    def get_queryset(self):
        comment_id = self.kwargs['pk']
        queryset = CommentLike.objects.filter(comment_id = comment_id)
        return queryset

class CommentLikeListAPIView(generics.ListAPIView):
    serializer_class = CommentLikeSerializer
    permission_classes = [AllowAny, ]
    queryset = CommentLike.objects.all()

class CommentLikeCreateAPIView(generics.CreateAPIView):
    serializer_class  = CommentLikeSerializer
    permission_classes = [IsAuthenticated, ]

    def perform_create(self, serializer):
        comment_id = self.kwargs['pk']
        user = self.request.user
        if CommentLike.objects.filter(author=user, comment_id = comment_id).exists():
            raise ValidationError({
                "success": False,
                'message': "Siz allaqachon bu komentga like bosgansiz. "
            })
        serializer.save(comment_id=comment_id, author=self.request.user)

class CommentLikeDeleteAPIView(generics.DestroyAPIView):
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated, ]
    queryset = CommentLike.objects.all()

    def delete(self, request, *args, **kwargs):
        comment_id = self.kwargs['pk']
        if not(CommentLike.objects.filter(comment_id = comment_id, author = request.user).exists()):
            raise ValidationError({
                "success": False,
                "message": "Siz bu komentga like bosmagansiz. "
            })
        CommentLike.objects.get(comment_id = comment_id, author = request.user).delete()
        return Response({
            "success": True,
            "message": "Comment successfully deleted",
        })




































