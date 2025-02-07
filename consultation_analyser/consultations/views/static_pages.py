from django.http import HttpRequest
from django.shortcuts import render

from .. import models


def home(request: HttpRequest):
    questions = models.Question.objects.all().order_by("id")[:10]
    context = {"questions": questions}
    return render(request, "home.html", context)
