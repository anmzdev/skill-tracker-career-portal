from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render, redirect

from career.forms import JobPostForm, EditRecruiterProfileForm
from career.models import JobPost, RecruiterProfile, JobApplication


def recruiter_dash(request):
    return render(request,'recruiter/recruiter_dash.html')

def post_job(request):
    if request.method == 'POST':
        form = JobPostForm(request.POST)
        if form.is_valid():
            job = form.save(commit=False)
            job.recruiter = request.user
            job.save()
            messages.success(request, "Job posted successfully!")
            return redirect('view_jobs')
    else:
        form = JobPostForm()
    return render(request, 'recruiter/post_job.html', {'form': form})


@login_required
def view_jobs(request):
    jobs = JobPost.objects.filter(recruiter=request.user)
    return render(request, 'recruiter/view_jobs.html', {'jobs': jobs})


def edit_job(request, post_id):
    try:
        recruiter = request.user.recruiterprofile
    except ObjectDoesNotExist:
        messages.error(request, "You are not authorized to edit job postings.")
        return redirect('login')

    job = JobPost.objects.get(id=post_id, recruiter=request.user)

    if request.method == 'POST':
        form = JobPostForm(request.POST, instance=job)
        if form.is_valid():
            form.save()
            messages.success(request, "Job updated successfully.")
            return redirect('view_jobs')
    else:
        form = JobPostForm(instance=job)

    return render(request, 'recruiter/edit_job.html', {'form': form})

def delete_job(request, post_id):
    job = JobPost.objects.get(id=post_id)
    if request.method == 'POST':
        job.delete()
        return redirect('view_jobs')
    return render(request, 'recruiter/delete_job.html', {'job': job})

@login_required
def view_profile(request):
    recruiter = RecruiterProfile.objects.get(user=request.user)
    return render(request, 'recruiter/view_profile.html', {'recruiter': recruiter})


@login_required
def edit_profile(request):
    recruiter = RecruiterProfile.objects.get(user=request.user)

    if request.method == 'POST':
        form = EditRecruiterProfileForm(request.POST, instance=recruiter)
        if form.is_valid():
            form.save()
            messages.success(request, 'Company profile updated successfully!')
            return redirect('view_profile')  # or wherever you want to redirect
    else:
        form = EditRecruiterProfileForm(instance=recruiter)

    return render(request, 'recruiter/edit_profile.html', {'form': form})


def view_applicants(request):
    jobs = JobPost.objects.filter(recruiter=request.user)
    applications = JobApplication.objects.filter(job__in=jobs).select_related('user', 'job')


    return render(request, 'recruiter/view_applicants.html', {
        'applications': applications
    })


def recruiter_card(request):
    return render(request,'recruiter/recruiter_card.html')

