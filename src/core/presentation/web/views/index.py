from __future__ import annotations

from typing import TYPE_CHECKING

from django.shortcuts import render
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin


if TYPE_CHECKING:
    from django.http import HttpRequest, HttpResponse


class IndexView(LoginRequiredMixin, View):
    login_url = "accounts:login"
    """This is the main view of the application."""
    def get(self, request: HttpRequest) -> HttpResponse:
        """This is the get method of the view."""

        return render(request, 'index.html')
