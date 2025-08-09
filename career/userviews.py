from django.contrib import messages
from django.shortcuts import render, redirect

from career.forms import  EditUserProfileForm
from career.models import UserProfile, Feedback, JobPost, JobApplication


def user_dash(request):
    profile = UserProfile.objects.filter(user=request.user).first()
    return render(request, 'user/user_dash.html', {
        'profile': profile
    })

def user_profile(request):
    profile, created = UserProfile.objects.get_or_create(user=request.user)
    return render(request, 'user/profile.html', {
        'user': request.user,
        'profile': profile
    })


def profile_edit(request):
    profile, created = UserProfile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        form = EditUserProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('user_profile')  # Your profile view URL name
    else:
        form = EditUserProfileForm(instance=profile)

    return render(request, 'user/profile_edit.html', {'form': form})


def view_reply(request):
    feedbacks = Feedback.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'user/view_reply.html', {'feedbacks': feedbacks})


def view_all_jobs(request):
    all_jobs = JobPost.objects.all()
    user_applications = JobApplication.objects.filter(user=request.user)
    applied_jobs = [app.job for app in user_applications]

    return render(request, 'user/view_jobs.html', {
        'jobs': all_jobs,
        'applied_jobs': applied_jobs
    })


def apply_job(request, job_id):
    job = JobPost.objects.get(id=job_id)

    # Prevent duplicate applications
    if JobApplication.objects.filter(user=request.user, job=job).exists():
        messages.info(request, "You already applied for this job.")
    else:
        JobApplication.objects.create(user=request.user, job=job)
        messages.success(request, "Application submitted successfully!")

    return redirect('view_all_jobs')

def my_applications(request):
    applications = JobApplication.objects.filter(user=request.user).select_related('job')
    return render(request, 'user/my_applications.html', {'applications': applications})


def user_card(request):
    return render(request,'user/user_card.html')

