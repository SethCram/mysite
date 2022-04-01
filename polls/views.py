from django.shortcuts import render
from django.shortcuts import get_object_or_404

from django.http import HttpResponse
from django.http import Http404
from django.http import HttpResponseRedirect
from django.template import loader

from django.urls import reverse

from .models import Question, Choice

# Create your views here.

"""First rendition: (placeholder)
def index(request):
    return HttpResponse("Hello world. You're at the polls index.")
"""

"""Second rendition: (hardcoded)
#display latest 5 poll ?'s in syst:
def index(request):
    #order according to pub date
    latest_question_list = Question.objects.order_by('-pub_date')[:5] #why minus sign before?, uses only last 5 chars
    #seperate by , 
    output = ', '.join([q.question_text for q in latest_question_list])
    
    return HttpResponse(output)
"""

"""Third rendition: (template usage)
#display latest 5 poll ?'s in syst:
def index(request):
    latest_question_list = Question.objects.order_by('-pub_date')[:5]
    template = loader.get_template('polls/index.html')
    context = { 
        'latest_question_list': latest_question_list,
        }
    return HttpResponse( template.render(context, request))
"""

#Fourth rendition: (template shortcut)
#display latest 5 poll ?'s in syst:
def index(request):
    latest_question_list = Question.objects.order_by('-pub_date')[:5]
    context = { 
        'latest_question_list': latest_question_list,
        }
    return render(request, 'polls/index.html', context)

"""First rendition: (placeholder)
def detail(request, question_id):
    return HttpResponse("You're looking at question %s." % question_id)
"""

"""Second rendition: (error 404)
def detail(request, question_id):
    try: 
        #get question w/ given id:
        question = Question.objects.get(pk=question_id) 
    except Question.DoesNotExist:
        raise Http404("Question does not exist")
    context = {'question':question}
    return render(request, 'polls/detail.html', context)
"""

#Third rendition: (error 404 shortcut)
def detail(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    context = {'question':question}
    return render(request, 'polls/detail.html', context)

def results(request, question_id):
    #response = "You're looking at the results of question %s.
    #return HttpResponse(response % question_id)
    
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/results.html', { 
        'question': question})

"""First rendition: (placeholder)
def vote(request, question_id):
    return HttpResponse("You're voting on question %s." % question_id)
"""

def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])  #rets id of sel'd choice using POST
    except (KeyError, Choice.DoesNotExist):
        #redisplay question voting form
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        #incr vote amt and save in DB
        selected_choice.votes += 1
        selected_choice.save()
        
        #Always ret an HtttpResponseRedirect after successful POST data
        # Prevents data from being posted twice if user hits Back btn
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))