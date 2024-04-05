import random

import factory
import faker as _faker
import yaml

from consultation_analyser.consultations import models

faker = _faker.Faker()

default_multiple_choice_options = ["Yes", "No", "Not sure"]


def generate_dummy_topic_label():
    dummy_sentence = faker.sentence()
    words = dummy_sentence.lower().strip(".")
    words_joined = words.replace(" ", "_")
    topic_number = random.randint(-1, 3)
    output = f"{topic_number}_{words_joined}"
    return output


class FakeConsultationData:
    def __init__(self):
        with open("./tests/examples/questions.yml", "r") as f:
            questions = yaml.safe_load(f)
            slugs = [q["slug"] for q in questions]
            self.questions = dict(zip(slugs, questions))

    def question(self):
        return random.choice(list(self.questions.values()))

    def get_free_text_answer(self, slug):
        q = self.questions[slug]
        return random.choice(q["answers"])

    def all_questions(self):
        return list(self.questions.values())


class ConsultationFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.Consultation
        skip_postgeneration_save = True

    name = faker.sentence()
    slug = faker.slug()

    @factory.post_generation
    def with_question(consultation, creation_strategy, value, **kwargs):
        if value is True:
            SectionFactory(
                consultation=consultation,
                with_question=True,
                with_question__with_answer=kwargs.get("with_answer"),
                with_question__with_multiple_choice=kwargs.get("with_multiple_choice"),
                with_question__with_free_text=kwargs.get("with_free_text"),
            )


class SectionFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.Section
        skip_postgeneration_save = True

    name = faker.sentence()
    slug = faker.slug()
    consultation = factory.SubFactory("tests.factories.ConsultationFactory")

    class Params:
        with_questions = factory.Trait(questions=[factory.SubFactory("tests.factories.QuestionFactory")])

    @factory.post_generation
    def with_question(section, creation_strategy, value, **kwargs):
        if value is True:
            QuestionFactory(
                section=section,
                with_answer=kwargs.get("with_answer"),
                with_multiple_choice=kwargs.get("with_multiple_choice"),
                with_free_text=kwargs.get("with_free_text"),
            )


class QuestionFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.Question
        skip_postgeneration_save = True

    text = factory.LazyAttribute(lambda o: o.question["text"])
    slug = factory.LazyAttribute(lambda o: o.question["slug"])
    multiple_choice_options = factory.LazyAttribute(lambda o: o.question["multiple_choice_options"])
    has_free_text = factory.LazyAttribute(lambda o: o.question["has_free_text"])
    section = factory.SubFactory(SectionFactory)

    class Params:
        question = FakeConsultationData().question()

    @factory.post_generation
    def with_answer(question, creation_strategy, value, **kwargs):
        if value is True:
            answer = AnswerFactory(question=question)
            answer.save()

    @factory.post_generation
    def with_multiple_choice(question, creation_strategy, value, **kwargs):
        if value is True and question.multiple_choice_options is None:
            question.multiple_choice_options = default_multiple_choice_options
            question.save()

    @factory.post_generation
    def with_free_text(question, creation_strategy, value, **kwargs):
        if value is True:
            answer = AnswerFactory(
                question=question,
                with_free_text=kwargs.get("with_free_text"),
            )
            answer.save()


class ConsultationResponseFactory(factory.django.DjangoModelFactory):
    consultation = factory.SubFactory(ConsultationFactory)

    class Meta:
        model = models.ConsultationResponse


class ThemeFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.Theme

    # TODO - may need to be changed once ML pipeline is in
    label = generate_dummy_topic_label()
    summary = f"Summary: {label}"


class AnswerFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.Answer
        skip_postgeneration_save = True

    free_text = factory.LazyAttribute(
        lambda o: FakeConsultationData().get_free_text_answer(o.question.slug) if o.question.has_free_text else None
    )

    question = factory.SubFactory(QuestionFactory)
    consultation_response = factory.SubFactory(ConsultationResponseFactory)
    theme = factory.LazyAttribute(lambda o: ThemeFactory() if o.free_text else None)

    multiple_choice_responses = factory.LazyAttribute(
        lambda o: random.choice(o.question.multiple_choice_options) if o.question.multiple_choice_options else None
    )

    @factory.post_generation
    def with_free_text(answer, creation_strategy, value, **kwargs):
        if answer.free_text is None:
            answer.free_text = "This is a sample free-text response"
            answer.save()
