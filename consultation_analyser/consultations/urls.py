from django.urls import path

from .views import consultations, pages, questions, schema

urlpatterns = [
    path("", pages.home),
    path("consultations", consultations.show_questions),
    path("schema", schema.show),
    path("schema/<str:schema_name>.json", schema.raw_schema),
    path(
        "consultations/<str:consultation_slug>/sections/<str:section_slug>/questions/<str:question_slug>",
        questions.show,
        name="show_question",
    ),
    path(
        "consultations/<str:consultation_slug>/sections/<str:section_slug>/responses/<str:question_slug>",
        questions.show_responses,
    ),
    path("batch-example", pages.batch_example, name="batch_example"),
]
