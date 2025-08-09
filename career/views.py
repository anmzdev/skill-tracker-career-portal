from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect
from .models import *
from .forms import *
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required, user_passes_test




def index(request):
    return render(request, 'index.html')



def user_register(request):
    if request.method == "POST":
        user_form    = RegisterForm(request.POST)
        profile_form = UserRegisterForm(request.POST)

        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            profile           = profile_form.save(commit=False)
            profile.user      = user
            profile.save()

            messages.success(request, "Registered! Please log in.")
            return redirect("login")        # login url‑name
    else:
        user_form    = RegisterForm()
        profile_form = UserRegisterForm()

    context = {
        "user_form":           user_form,
        "user_profile_form":   profile_form,
    }
    return render(request, "register.html", context)

def recruiter_register(request):
    if request.method == 'POST':
        user_form = RecruiterUserForm(request.POST)
        profile_form = RecruiterProfileForm(request.POST)

        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()  # UserCreationForm handles password
            recruiter = profile_form.save(commit=False)
            recruiter.user = user
            recruiter.save()

            UserProfile.objects.create(user=user, is_recruiter=True)


            login(request, user)
            return redirect('login')  # Change this to your actual dashboard URL name
    else:
        user_form = RecruiterUserForm()
        profile_form = RecruiterProfileForm()

    return render(request, 'recruiter_register.html', {
        'user_form': user_form,
        'profile_form': profile_form,
    })


def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            if user.is_staff:
                return redirect('admin_dash')
            elif hasattr(user, 'userprofile') and user.userprofile.is_recruiter:
                return redirect('recruiter_dash')
            else:
                return redirect('user_dash')
        else:
            messages.error(request, 'Invalid username or password')
    return render(request, 'login.html')




def logout_view(request):
    logout(request)
    return redirect('index')

def dash_board(request):
    return render(request, 'dash.html')

@login_required
def quiz_view(request):
    profile, created = UserProfile.objects.get_or_create(user=request.user)

    if profile.chosen_career and request.GET.get('retake') != 'true':
        return render(request, 'quiz_already_taken.html', {
            'career': profile.chosen_career
        })

    if request.GET.get('retake') == 'true':
        profile.chosen_career = None
        profile.save()

    questions = Question.objects.all()

    if request.method == 'POST':
        selected_careers = []

        for question in questions:
            selected_option_id = request.POST.get(f'q{question.id}')
            if selected_option_id:
                try:
                    selected_option = Option.objects.get(id=selected_option_id)
                    selected_careers.append(selected_option.career)
                except Option.DoesNotExist:
                    pass

        if selected_careers:
            suggested_career = max(set(selected_careers), key=selected_careers.count)
            match_count = selected_careers.count(suggested_career)
            match_percentage = int((match_count / len(questions)) * 100)

            profile.chosen_career = suggested_career
            profile.save()

            request.session['match_percentage'] = match_percentage

            messages.success(request, "Quiz submitted successfully!")
            return redirect('dashboard')

    return render(request, 'quiz.html', {'questions': questions})


@login_required
def dashboard_view(request):
    user = request.user

    profile, _created = UserProfile.objects.get_or_create(user=user)

    career = profile.chosen_career
    skills = []
    progress = []

    if career:
        skills = Skill.objects.filter(career=career)
        progress = SkillProgress.objects.filter(user=user)

    match_percentage = request.session.get('match_percentage', None)

    return render(request, 'dashboard.html', {
        'career': profile.chosen_career,
        'skills': skills,
        'progress': progress,
        'match_percentage': match_percentage,
    })


@login_required
def update_skill(request, skill_id):
    skill = Skill.objects.get(id=skill_id)
    progress_obj, created = SkillProgress.objects.get_or_create(user=request.user, skill=skill)
    if request.method == 'POST':
        form = SkillProgressForm(request.POST, instance=progress_obj)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
    else:
        form = SkillProgressForm(instance=progress_obj)
    return render(request, 'skills.html', {'form': form, 'skill': skill})

@user_passes_test(lambda u: u.is_superuser)
def admin_dashboard(request):
    users = UserProfile.objects.all()
    return render(request, 'admin_dashboard.html', {'users': users})

def submit_feedback(request):
    if request.method == 'POST':
        form = FeedbackForm(request.POST)
        if form.is_valid():
            feedback = form.save(commit=False)
            feedback.user = request.user
            feedback.save()
            messages.success(request, "Thank you! Your feedback has been submitted.")
            return redirect('submit_feedback')
    else:
        form = FeedbackForm()
    return render(request, 'user/feedback.html', {'form': form})