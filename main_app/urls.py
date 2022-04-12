from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('about/', views.about, name="about"),
    path('digimon/', views.digimon_index, name="index"),
    path('digimon/<int:digimon_id>/', views.digimon_detail, name='detail'),
    path('digimon/create/', views.DigimonCreate.as_view(), name='digimon_create'),
    path('digimon/<int:pk>/update/', views.DigimonUpdate.as_view(), name='digimon_update'),
    path('digimon/<int:pk>/delete/', views.DigimonDelete.as_view(), name='digimon_delete'),
    path('digimon/<int:digimon_id>/add_feeding/', views.add_feeding, name='add_feeding'),

    path('toys/', views.ToyList.as_view(), name="toys_index"),
    path('toys/<int:pk>/', views.ToyDetail.as_view(), name="toys_detail"),
    path('toys/create/', views.ToyCreate.as_view(), name='toys_create'),
    path('toys/<int:pk>/update', views.ToyUpdate.as_view(), name='toys_update'),
    path('toys/<int:pk>/delete', views.ToyDelete.as_view(), name='toys_delete'),

    # Associate a toy wiht Digimon (M:M)
    path('digimon/<int:digimon_id>/assoc_toy/<int:toy_id>/', views.assoc_toy, name= 'assoc_toy'),
    # unassociate a toy wiht Digimon (M:M)
    path('digimon/<int:digimon_id>/unassoc_toy/<int:toy_id>/', views.unassoc_toy, name='unassoc_toy'),

    #URL for signup
    path('accounts/signup/', views.signup, name='signup')

]