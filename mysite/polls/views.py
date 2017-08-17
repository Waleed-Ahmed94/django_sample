# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from .models import Question, Choice, Answer
from django.template import loader
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.contrib import messages
from usermanager.models import PollUser

def login_required(func):
    def function_wrapper(request, **args):
        if request.session.has_key('username'):
            if args:
                return func(request, **args)
            else:
                return func(request)
        else:
            messages.add_message(request, messages.WARNING, "Login Required")
            return HttpResponseRedirect(reverse("usermanager:home"))
    return function_wrapper

@login_required
def index(request):
    latest_question_list = Question.objects.order_by("-pub_date")[:5]
    return render(request, "polls/index.html", { 'latest_question_list':latest_question_list})

@login_required
def detail(request, pk):
    question = Question.objects.get(pk=pk)
    user = PollUser.objects.get(pk=request.session['userid'])
    try:
        answer = user.answer_set.get(question_id=pk)
    except (KeyError, Answer.DoesNotExist):
        return render(request, "polls/detail.html", {'question': question})
    else:
        return render(request, "polls/detail.html", {'question': question,'answer':answer})

@login_required
def results(request, pk):
    question = Question.objects.get(pk=pk)
    return render(request, "polls/results.html", {'question':question})


@login_required
def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        selected_choice.votes += 1
        user = PollUser.objects.get(pk=request.session['userid'])
        user.answer_set.create(question_id=question_id, choice_id=selected_choice.id)
        selected_choice.save()
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))

