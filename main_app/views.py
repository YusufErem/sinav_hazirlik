from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from main_app.models import Question, Category

def registerPage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        
        if password1 == password2:
            if User.objects.filter(username=username).exists():
                messages.error(request, 'Username already exists')
            elif User.objects.filter(email=email).exists():
                messages.error(request, 'Email already exists')
            else:
                user = User.objects.create_user(username=username, email=email, password=password1)
                user.save()
                return redirect('login')
        else:
            messages.error(request, 'Passwords do not match')
    return render(request, 'register.html')

def loginPage(request):
    if request.user.is_authenticated:
        return redirect('home')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Username or Password is incorrect')
            return redirect('login')
    return render(request, 'login.html')

@login_required
def home(request):
    categories = Category.objects.all()
    show_completed = request.GET.get('show_completed', 'false') == 'true'
    if show_completed:
        questions = Question.objects.filter(user=request.user)
    else:
        questions = Question.objects.filter(user=request.user, completed=False)
    context = {
        'categories': categories,
        'questions': questions,
        'username': request.user.username,
        'show_completed': show_completed
    }
    return render(request, 'home.html', context)

@login_required
def logoutUser(request):
    logout(request)
    return redirect('login')

@login_required
def addQuestion(request):
    categories = Category.objects.all()
    if request.method == 'POST':
        category_id = request.POST.get('category')
        category = Category.objects.get(id=category_id)
        question_image = request.FILES.get('question_image')
        answer_image = request.FILES.get('answer_image')
        notes = request.POST.get('notes')
        mistake_reason = request.POST.get('mistake_reason')
        
        question = Question.objects.create(
            user=request.user,
            category=category,
            question_image=question_image,
            answer_image=answer_image,
            notes=notes,
            mistake_reason=mistake_reason
        )
        question.save()
        return redirect('home')
    return render(request, 'question.html', {'categories': categories})

@login_required
def categoryQuestions(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    show_completed = request.GET.get('show_completed', 'false') == 'true'
    if show_completed:
        questions = Question.objects.filter(user=request.user, category=category)
    else:
        questions = Question.objects.filter(user=request.user, category=category, completed=False)
    categories = Category.objects.all()
    context = {
        'category': category,
        'questions': questions,
        'categories': categories,
        'username': request.user.username,
        'show_completed': show_completed
    }
    return render(request, 'category_questions.html', context)

@login_required
def questionDetail(request, question_id):
    question = get_object_or_404(Question, id=question_id)
    context = {
        'question': question,
        'username': request.user.username
    }
    return render(request, 'question_detail.html', context)

@login_required
def editQuestion(request, question_id):
    question = get_object_or_404(Question, id=question_id)
    categories = Category.objects.all()
    if request.method == 'POST':
        category_id = request.POST.get('category')
        category = Category.objects.get(id=category_id)
        question.question_image = request.FILES.get('question_image', question.question_image)
        question.answer_image = request.FILES.get('answer_image', question.answer_image)
        question.notes = request.POST.get('notes')
        question.mistake_reason = request.POST.get('mistake_reason')
        question.category = category
        question.completed = 'completed' in request.POST
        question.save()
        return redirect('question_detail', question_id=question.id)
    context = {
        'question': question,
        'categories': categories,
        'username': request.user.username
    }
    return render(request, 'edit_question.html', context)

@login_required
def deleteQuestion(request, question_id):
    question = get_object_or_404(Question, id=question_id)
    if request.method == 'POST':
        question.delete()
        return redirect('home')
    context = {
        'question': question,
        'username': request.user.username
    }
    return render(request, 'delete_question.html', context)

@login_required
def toggleCompleteQuestion(request, question_id):
    question = get_object_or_404(Question, id=question_id)
    if request.method == 'POST':
        question.completed = not question.completed
        question.save()
    return redirect('question_detail', question_id=question.id)