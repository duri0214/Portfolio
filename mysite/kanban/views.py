"""views.py"""
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect, resolve_url, get_object_or_404
from django.views.generic import DetailView, UpdateView, CreateView, ListView, DeleteView
from django.urls import reverse_lazy
from .forms import UserForm, ListForm, CardForm, CardCreateFromHomeForm
from .mixins import OnlyYouMixin
from . models import List, Card

def index(request):
    """index"""
    return render(request, "kanban/index.html")

def signup(request):
    """signup"""
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user_instance = form.save()
            login(request, user_instance)
            return redirect("kanban:home")
    else:
        form = UserCreationForm()

    context = {
        "form": form
    }
    return render(request, 'kanban/signup.html', context)

class HomeView(LoginRequiredMixin, ListView):
    """HomeView"""
    model = List
    template_name = "kanban/home.html"

class UserDetailView(LoginRequiredMixin, DetailView):
    """login時しかユーザーページは見れません"""
    model = get_user_model()
    template_name = "kanban/users/detail.html"

class UserUpdateView(OnlyYouMixin, UpdateView):
    """OnlyYouMixinは自作です（リクエストuseridとログインuseridが一致するか）"""
    model = get_user_model()
    template_name = "kanban/users/update.html"
    form_class = UserForm
    def get_success_url(self):
        return resolve_url('kanban:users_detail', pk=self.kwargs['pk'])

class ListCreateView(LoginRequiredMixin, CreateView):
    """ListCreateView"""
    model = List
    template_name = "kanban/lists/create.html"
    form_class = ListForm
    success_url = reverse_lazy("kanban:lists_list")

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

class ListListView(LoginRequiredMixin, ListView):
    """ListListView"""
    model = List
    template_name = "kanban/lists/list.html"

class ListDetailView(LoginRequiredMixin, DetailView):
    """ListDetailView"""
    model = List
    template_name = "kanban/lists/detail.html"

class ListUpdateView(LoginRequiredMixin, UpdateView):
    """ListUpdateView"""
    model = List
    template_name = "kanban/lists/update.html"
    form_class = ListForm
    success_url = reverse_lazy("kanban:home")

class ListDeleteView(LoginRequiredMixin, DeleteView):
    """ListDeleteView"""
    model = List
    template_name = "kanban/lists/delete.html"
    form_class = ListForm
    success_url = reverse_lazy("kanban:home")

class CardCreateView(LoginRequiredMixin, CreateView):
    """CardCreateView"""
    model = Card
    template_name = "kanban/cards/create.html"
    form_class = CardForm
    success_url = reverse_lazy("kanban:home")

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

class CardListView(LoginRequiredMixin, ListView):
    """CardListView"""
    model = Card
    template_name = "kanban/cards/list.html"

class CardDetailView(LoginRequiredMixin, DetailView):
    """CardDetailView"""
    model = Card
    template_name = "kanban/cards/detail.html"

class CardUpdateView(LoginRequiredMixin, UpdateView):
    """CardUpdateView"""
    model = Card
    template_name = "kanban/cards/update.html"
    success_url = reverse_lazy("kanban:home")

class CardDeleteView(LoginRequiredMixin, DeleteView):
    """CardDeleteView"""
    model = Card
    template_name = "kanban/cards/delete.html"
    form_class = CardForm
    success_url = reverse_lazy("kanban:home")

class CardCreateFromHomeView(LoginRequiredMixin, CreateView):
    """CardCreateFromHomeView"""
    model = Card
    template_name = "kanban/cards/create.html"
    form_class = CardCreateFromHomeForm
    success_url = reverse_lazy("kanban:home")

    def form_valid(self, form):
        form.instance.list = get_object_or_404(List, pk=self.kwargs['list_pk'])
        form.instance.user = self.request.user
        return super().form_valid(form)
