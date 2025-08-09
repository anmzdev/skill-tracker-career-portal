from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib import messages

from career.forms import QuestionForm, OptionForm, CareerForm, SkillForm
from career.models import Question, CareerPath, Skill, Option, Feedback, JobPost


def admin_dash(request):
    return render(request,'admin/admin_dash.html')



def view_quiz(request):
    questions = Question.objects.all()
    return render(request, 'admin/view_quiz.html', {'questions': questions})


def add_question(request):
    if request.method == 'POST':
        form = QuestionForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Question added successfully!')
            return redirect('view_quiz')
    else:
        form = QuestionForm()
    return render(request, 'admin/add_question.html', {'form': form})


def edit_question(request, question_id):
    question = Question.objects.get(id=question_id)
    if request.method == 'POST':
        form = QuestionForm(request.POST, instance=question)
        if form.is_valid():
            form.save()
            return redirect('view_quiz')
    else:
        form = QuestionForm(instance=question)
    return render(request, 'admin/edit_question.html', {'form': form})

def delete_question(request, question_id):
    question = Question.objects.get(id=question_id)
    question.delete()
    return redirect('view_quiz')

def add_option(request):
    if request.method == 'POST':
        form = OptionForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('add_option')
    else:
        form = OptionForm()

    return render(request, 'admin/add_option.html', {'form': form})


def view_option(request):
    options = Option.objects.select_related('question').all()
    return render(request, 'admin/view_option.html', {'options': options})

def edit_option(request, option_id):
    option = Option.objects.get(id=option_id)
    if request.method == 'POST':
        form = OptionForm(request.POST, instance=option)
        if form.is_valid():
            form.save()
            return redirect('view_options')
    else:
        form = OptionForm(instance=option)
    return render(request, 'admin/edit_option.html', {'form': form})

def delete_option(request, option_id):
    option = Option.objects.get(id=option_id)
    option.delete()
    return redirect('view_option')


def add_career(request):
    if request.method == 'POST':
        form = CareerForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('add_career')
    else:
        form = CareerForm()
    return render(request, 'admin/add_career.html', {'form': form})



def view_career(request):
    query = request.GET.get('q')
    careers = CareerPath.objects.all()
    if query:
        careers = careers.filter(name__icontains=query)
    return render(request, 'admin/view_career.html', {'careers': careers, 'query': query})

def edit_career(request, career_id):
    career = CareerPath.objects.get(id=career_id)
    if request.method == 'POST':
        form = CareerForm(request.POST, instance=career)
        if form.is_valid():
            form.save()
            return redirect('view_career')
    else:
        form = CareerForm(instance=career)
    return render(request, 'admin/edit_career.html', {'form': form})

def delete_career(request, career_id):
    career = CareerPath.objects.get(id=career_id)
    career.delete()
    return redirect('view_career')



def add_skill(request):
    if request.method == 'POST':
        form = SkillForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('add_skill')
    else:
        form = SkillForm()
    return render(request, 'admin/add_skill.html', {'form': form})

def view_skill(request):
    query = request.GET.get('q')
    skills = Skill.objects.all()
    if query:
        skills = skills.filter(name__icontains=query)
    return render(request, 'admin/view_skill.html', {'skills': skills, 'query': query})

def edit_skill(request, skill_id):
    skill = Skill.objects.get(id=skill_id)
    if request.method == 'POST':
        form = SkillForm(request.POST, instance=skill)
        if form.is_valid():
            form.save()
            return redirect('view_skill')  # Make sure you have this URL name
    else:
        form = SkillForm(instance=skill)
    return render(request, 'admin/edit_skill.html', {'form': form})

def delete_skill(request, skill_id):
    skill = Skill.objects.get(id=skill_id)
    if request.method == 'POST':
        skill.delete()
        return redirect('view_skill')
    return render(request, 'admin/delete_skill.html', {'skill': skill})


def user_list(request):
    users = User.objects.filter(is_staff=False, is_superuser=False)
    return render(request, 'admin/user_list.html', {'users': users})


def view_feedback(request):
    feedbacks = Feedback.objects.all()
    return render(request, 'admin/view_feedback.html', {'feedbacks': feedbacks})

def feedback_reply(request, feedback_id):
    feedback = Feedback.objects.get(id=feedback_id)

    if request.method == "POST":
        reply_text = request.POST.get('reply')
        feedback.reply = reply_text
        feedback.save()
        messages.success(request, "Reply sent successfully!")
        return redirect('view_feedback')  # ✅ Make sure this URL name matches

    return render(request, 'admin/feedback_reply.html', {'feedback': feedback})


def admin_view_jobs(request):
    jobs = JobPost.objects.select_related('recruiter', 'career').all()
    return render(request, 'admin/admin_view_jobs.html', {'jobs': jobs})

def admin_card(request):
    return render(request,'admin/admin_card.html')
