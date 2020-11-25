from django.urls import path
from .import views

app_name = 'blog'

urlpatterns = [
    path('', views.post_list, name='post_list'),
    path('<int:year>/<int:month>/<int:day>/<slug:post>/',
        views.post_detail, name='post_detail'),
    path('tag/<slug:tag_slug>/', views.post_list, name='post_list_by_tag'),
    path('main_page', views.main_page, name = 'main_page'),
    path('about-us', views.about, name='about-us'),
    path('contact', views.contact, name='contact'),

]