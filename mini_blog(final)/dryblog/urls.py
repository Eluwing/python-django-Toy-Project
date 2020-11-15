from django.urls import path
from dryblog import views


urlpatterns = [

    path('', views.index, name='index'),
    path('blogs/', views.PostListView.as_view(), name='post'),
    path('blogs/<int:pk>', views.PostDetailView.as_view(), name='post-detail'),

    #Blogs create, update(renew), delete Urls
    path('blogs/create/', views.post_create, name='post_create'),
    #path('blogs/create/', views.PostCreate.as_view(), name='post_create'),
    path('blogs/<int:pk>/renew/', views.renew_post, name='renew-post'),
    path('blogs/<int:pk>/delete/', views.PostDelete.as_view(), name='post_delete'),


    #Comment create, update(renew), delete Urls(function)
    path('blogs/<int:post_id>/comments/create/', views.comment_create, name="comment_create"),
    path('blogs/<int:post_id>/comments/<int:comment_id>/update/', views.comment_update, name="comment_update"),
    path('blogs/<int:post_id>/comments/<int:comment_id>/delete/', views.comment_delete, name="comment_delete"),

    #User Detail
    path('blogs/blogger/<str:user_name>', views.user_detail, name = "user_detail"),

    path('blogs/blogger/', views.user_list, name = "user_list"),


    #Comment create, update(renew), delete Urls(Generic)
    #path('blogs/comment_create/', views.CommentCreate.as_view(), name='comment_create'),
    # path('blogs/<int:pk>', views.CommentUpdate.as_view(), name='comment_update'),
    # path('blogs/<int:pk>/', views.CommentDelete.as_view(), name='comment_delete'),



    #django_comments API
    #url(r'^comments/', include('django_comments.urls')),

]
