from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from .models import Test, UserAnswer, TestResult, Question
from .forms import UserRegistrationForm, TestForm, QuestionForm
from django.conf import settings
import json

# REGISTRATION
def register(request):
    if request.method == "POST":
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data["password"])
            user.is_headhunter = form.cleaned_data["user_type"] == "headhunter"
            user.save()
            login(request, user)
            return redirect("dashboard")
    else:
        form = UserRegistrationForm()
    return render(request, "test_platform/register.html", {"form": form})

# LOGIN
def login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect("dashboard")
    else:
        form = AuthenticationForm()
    return render(request, "test_platform/login.html", {"form": form})

# DASHBOARD
@login_required
def dashboard(request):
    tests = request.user.created_tests.all() if request.user.is_headhunter else Test.objects.all()
    message = "Welcome, Headhunter!" if request.user.is_headhunter else "Welcome, User!"
    return render(request, "test_platform/dashboard.html", {"tests": tests, "message": message})

# TEST CREATION
@login_required
def create_test(request):
    if not request.user.is_headhunter:
        return redirect("dashboard")

    if request.method == "POST":
        form = TestForm(request.POST)
        if form.is_valid():
            test = form.save(commit=False)
            test.created_by = request.user
            test.save()
            return redirect("add_questions", test_id=test.id)
    else:
        form = TestForm()
    return render(request, "test_platform/create_test.html", {"form": form})


@login_required
def add_questions(request, test_id):
    test = get_object_or_404(Test, id=test_id, created_by=request.user)
    if request.method == "POST":
        form = QuestionForm(request.POST)
        if form.is_valid():
            question = form.save(commit=False)
            question.test = test
            question.save()
            return redirect("add_questions", test_id=test.id)
    else:
        form = QuestionForm()
    return render(request, "test_platform/add_questions.html", {"form": form, "test": test})

# TEST TAKING AND SUBMISSION
@login_required
def take_test(request, test_id):
    test = get_object_or_404(Test, id=test_id)
    if request.method == "POST":
        score = 0
        for question in test.questions.all():
            user_answer = request.POST.get(f"question_{question.id}")
            is_correct = user_answer == question.correct_answer
            UserAnswer.objects.create(
                user=request.user, question=question, selected_answer=user_answer, is_correct=is_correct
            )
            score += 1 if is_correct else 0
        TestResult.objects.create(user=request.user, test=test, score=score)
        return redirect("dashboard")
    return render(request, "test_platform/take_test.html", {"test": test})

# AVAILABLE TESTS
def available_tests(request):
    json_path = settings.BASE_DIR / "static" / "Hard_skills_python.json"
    with open(json_path) as f:
        json_tests = json.load(f)
    db_tests = Test.objects.filter(is_from_json=False)
    return render(request, "test_platform/tests_avalible.html", {"db_tests": db_tests, "json_tests": json_tests})


# RESOLVE JSON TEST
def resolve_json_test(request):
    if request.method == "POST":
        test_data = json.loads(request.POST["test_data"])
        questions = test_data["questions"]
        if "answers" in request.POST:
            answers = request.POST.getlist("answers")
            score = sum(1 for i, q in enumerate(questions) if q["correct_answer"] == answers[i])
            return render(request, "test_platform/test_result.html", {"score": score, "total": len(questions)})
        return render(request, "test_platform/test_resolve.html", {"test": test_data, "questions": questions})
    return redirect("available_tests")

def home(request):
    # Si el usuario está autenticado, redirigir al dashboard
    if request.user.is_authenticated:
        return redirect('dashboard')
    else:
        return redirect('login')  # Si no está autenticado, lo redirige a la página de login