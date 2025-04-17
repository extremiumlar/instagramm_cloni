from django.urls import path

from postlar.views import PostListAPIView, PostCreateView, PostRetrieveUpdateDestroyAPIView, PostCommentListView, \
    PostCommentCreateView, PostCommentListCreateView, PostLikeListView, CommentRetrieveAPIView, CommentLikeAPIView, \
    CommentLikeListAPIView, CommentLikeCreateAPIView, CommentLikeDeleteAPIView

urlpatterns = [
    path('list/', PostListAPIView.as_view()),
    path('create/', PostCreateView.as_view()),
    path('<uuid:pk>/', PostRetrieveUpdateDestroyAPIView.as_view()),
    path('<uuid:pk>/likes/', PostLikeListView.as_view()),
    path('<uuid:pk>/comments/', PostCommentListView.as_view()),
    path('<uuid:pk>/comments/create/', PostCommentCreateView.as_view()),
    path('comments/', PostCommentListCreateView.as_view()),
    path('comments/<uuid:pk>/', CommentRetrieveAPIView.as_view()),
    path('comments/<uuid:pk>/likes/', CommentLikeAPIView.as_view()),
    path('comments/likes/', CommentLikeListAPIView.as_view()),
    path('comments/<uuid:pk>/like-create/', CommentLikeCreateAPIView.as_view()),
    path('comments/<uuid:pk>/like-delete/', CommentLikeDeleteAPIView.as_view()),

]