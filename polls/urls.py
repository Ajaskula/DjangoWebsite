from django.urls import path

# importuje widoki
from . import views


# mapuje widok na stronkę
urlpatterns = [
    path("", views.home, name="home"),
    # path("<int:question_id>/", views.detail, name = "detail"),

    # widok do potencjalnego przybliżania sobie każdego z obrazków
    # path("show_images/", views.show_images, name='show_images'),

    # widok, który pozwoli na zarządzanie wszystkimi 
    # path("manage/", views.manage, name = 'manage'),
    path("manage/<int:image_id>/", views.manage_rectangle, name = 'manage_rectangle'),
    path("manage_my_pictures/<int:user_id>/", views.manage_my_pictures, name = 'manage_my_pictures'),
    path("<int:image_id>/", views.detail, name="detail"),
    # path("<int:question_id>/results/", views.results, name = "results"),
    # path("<int:question_id>/vote/", views.vote, name="vote"),
    path('add_rectangle/<int:svg_image_id>/', views.add_rectangle, name='add_rectangle'),
    # path("delete/", views.delete_rectangle, name = "delete"),
    # path("show_image_list/", views.show_image_list, name = "show_image_list"),
]