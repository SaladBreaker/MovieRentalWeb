from django.urls import path
from . import views
from django.views.generic import TemplateView

urlpatterns = [
    # login urls
    path("profile/after_login", views.after_login_view, name="after_login"),
    path("profile/logout", views.logout, name="logout"),
    # profile urls
    path("profile/", views.ProfileDetailView.as_view(), name="profile_details"),
    path("profile/update", views.ProfileUpdateView.as_view(), name="profile_update"),
    # movies urls
    path(
        "profile/movie/create",
        views.MovieCreateView.as_view(),
        name="movie_create",
    ),
    path(
        "profile/movie/<pk>/update",
        views.MovieUpdateView.as_view(),
        name="movie_update",
    ),
    path(
        "profile/movie/<pk>/delete",
        views.MovieDeleteView.as_view(),
        name="movie_delete",
    ),
    path(
        "profile/movie/<pk>",
        views.MovieDetailView.as_view(),
        name="movie_details",
    ),
    # general views
    path("", views.SearchView.as_view(), name="home"),
    path("movie/<pk>", views.PublicMovieDetailView.as_view(), name="public_profile"),
]
