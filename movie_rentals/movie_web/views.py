from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.views.generic import DetailView, ListView
from .models import Movie, Profile
from django.conf import settings
from django.http import HttpResponseRedirect, Http404
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse, reverse_lazy
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

import logging

logger = logging.getLogger(__name__)


# Login Logic


@login_required()
def after_login_view(request):
    profile = Profile.objects.filter(user=request.user).first()

    if profile:
        return HttpResponseRedirect(reverse("profile_details"))

    new_profile = Profile(user=request.user)
    new_profile.update_activity_tracker()
    new_profile.save()
    return HttpResponseRedirect(reverse("profile_update"))


@login_required()
def logout(request):
    auth_logout(request)
    return redirect(settings.ACCOUNT_LOGOUT_REDIRECT_URL)


# Profile Views
class ProfileDetailView(LoginRequiredMixin, DetailView):
    model = Profile
    template_name = "movie_web/profile_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        current_owner = get_object_or_404(Profile, user=self.request.user)
        context["movies"] = Movie.objects.all().filter(owner=current_owner)
        return context

    def get_object(self, queryset=None):
        profile = get_object_or_404(Profile, user=self.request.user)
        profile.update_activity_tracker()
        return profile


class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = Profile
    fields = Profile.get_form_fields()
    template_name = "movie_web/profile_update.html"

    def get_object(self):
        return get_object_or_404(Profile, user=self.request.user)

    def get_success_url(self):
        logger.info(f"User {self.request.user.email} updated his/her account info!")
        return reverse("profile_details")


# Moviews Views
class MovieCreateView(LoginRequiredMixin, CreateView):
    model = Movie
    fields = Movie.get_form_fields()
    template_name = "movie_web/movie_create.html"

    def form_valid(self, form):
        movie = form.save(commit=False)
        movie.owner = get_object_or_404(Profile, user=self.request.user)

        return super(MovieCreateView, self).form_valid(form)

    def get_success_url(self):
        logger.info(f"User {self.request.user.email} created a post!")
        return reverse("profile_details")


class MovieUpdateView(LoginRequiredMixin, UpdateView):
    model = Movie
    fields = Movie.get_form_fields()
    template_name = "movie_web/movie_update.html"

    def get_object(self, queryset=None):
        """
        Check the logged in user is the owner of the object or 404
        """
        movie = super(MovieUpdateView, self).get_object(queryset)
        owner = get_object_or_404(Profile, user=self.request.user)

        if movie.owner != owner:
            raise Http404("You don't own this movie")

        return movie

    def form_valid(self, form):
        movie = form.save(commit=False)
        movie.owner = get_object_or_404(Profile, user=self.request.user)

        return super(MovieUpdateView, self).form_valid(form)

    def get_success_url(self):
        logger.info(f"User {self.request.user.email} created a post!")
        return reverse("profile_details")


class MovieDeleteView(LoginRequiredMixin, DeleteView):
    model = Movie
    template_name = "movie_web/movie_delete.html"
    success_url = reverse_lazy("profile_details")

    def get_object(self, queryset=None):
        """
        Check the logged in user is the owner of the object or 404
        """
        movie = super(MovieDeleteView, self).get_object(queryset)
        owner = get_object_or_404(Profile, user=self.request.user)

        if movie.owner != owner:
            raise Http404("You don't own this movie")

        return movie


class MovieDetailView(LoginRequiredMixin, DetailView):
    model = Movie
    template_name = "movie_web/movie_detail.html"


# General Viewing
class SearchView(ListView):
    model = Movie
    template_name = "movie_web/index.html"
    context_object_name = "search_results"

    def get_queryset(self):
        result = super(SearchView, self).get_queryset()
        query = self.request.GET.get("search")
        logger.info(f"Got query: {query}")

        if query:
            logger.info("Got Query")
            postresult = Movie.objects.filter(name__icontains=query)
            result = postresult

        else:
            logger.info("Query is Null")
            result = Movie.objects.all().order_by("created_at")[:10]
        return result


class PublicMovieDetailView(DetailView):
    model = Movie
    template_name = "movie_web/movie_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        return context
