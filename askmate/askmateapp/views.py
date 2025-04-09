from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required
from .models import Question, Answer, Like
from .forms import QuestionForm, AnswerForm


def home(request):
    # Display all questions
    questions = Question.objects.all()

    return render(request, 'home.html', {'questions': questions})


# User registration view
def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserCreationForm()

    return render(request, 'register.html', {'form': form})

# Login view (Django built-in login view)
# Add URL for login view
from django.contrib.auth.views import LoginView


# Post a new question (requires login)
@login_required
def post_question(request):
    if request.method == 'POST':
        form = QuestionForm(request.POST)
        if form.is_valid():
            question = form.save(commit=False)
            question.created_by = request.user
            question.save()
            return redirect('home')
    else:
        form = QuestionForm()
    return render(request, 'post_question.html', {'form': form})

# View to display the details of a question
def question_detail(request, question_id):
    # Retrieve the question by ID
    question = get_object_or_404(Question, id=question_id)  
    return render(request, 'question_detail.html', {'question': question})


@login_required
def answer_question(request, question_id):
    question = get_object_or_404(Question, id=question_id)
    
    if request.method == 'POST':
        form = AnswerForm(request.POST)
        
        if form.is_valid():
            answer = form.save(commit=False)
            answer.question = question
            answer.created_by = request.user
            answer.save()
            
            return redirect('home')
        else:
            print("Form is not valid:", form.errors)
    else:
        form = AnswerForm()

    return render(request, 'answer_question.html', {'form': form, 'question': question})



# Like an answer (requires login)
@login_required
def like_answer(request, answer_id):
    answer = Answer.objects.get(id=answer_id)
    if not Like.objects.filter(answer=answer, user=request.user).exists():
        Like.objects.create(answer=answer, user=request.user)
    return redirect('home')


# User logout (requires login)
def user_logout(request):
    logout(request)
    return redirect('home')

