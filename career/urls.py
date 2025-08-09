from django.urls import path
from . import views, userviews, adminviews, recruiterviews

urlpatterns = [
    path('', views.index, name='index'),
    path('register/', views.user_register, name='register'),
    path('recruiter_register/', views.recruiter_register, name='recruiter_register'),
    path('login/', views.login_view, name='login'),
    path('profile/', userviews.user_profile, name='user_profile'),
    path('profile_edit/', userviews.profile_edit, name='profile_edit'),

    path('user_dash', userviews.user_dash, name='user_dash'),
    path('admin_dash', adminviews.admin_dash, name='admin_dash'),
    path('user_card', userviews.user_card, name='user_card'),
    path('recruiter_card', recruiterviews.recruiter_card, name='recruiter_card'),
    path('admin_card', adminviews.admin_card, name='admin_card'),

    path('logout/', views.logout_view, name='logout'),
    path('quiz/', views.quiz_view, name='quiz'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('skill/<int:skill_id>/', views.update_skill, name='update_skill'),
    path('feedback/', views.submit_feedback, name='submit_feedback'),
    path('view_reply/', userviews.view_reply, name='view_reply'),

    path('add_question/', adminviews.add_question, name='add_question'),
    path('view_quiz/', adminviews.view_quiz, name='view_quiz'),
    path('edit-question/<int:question_id>/', adminviews.edit_question, name='edit_question'),
    path('delete-question/<int:question_id>/', adminviews.delete_question, name='delete_question'),

    path('add_career/', adminviews.add_career, name='add_career'),
    path('view_career/', adminviews.view_career, name='view_career'),
    path('edit_career/<int:career_id>/', adminviews.edit_career, name='edit_career'),
    path('delete_career/<int:career_id>/', adminviews.delete_career, name='delete_career'),

    path('add_option/', adminviews.add_option, name='add_option'),
    path('view_option/', adminviews.view_option, name='view_option'),
    path('edit-option/<int:option_id>/', adminviews.edit_option, name='edit_option'),
    path('delete-option/<int:option_id>/', adminviews.delete_option, name='delete_option'),


    path('add_skill/', adminviews.add_skill, name='add_skill'),
    path('view_skill/', adminviews.view_skill, name='view_skill'),
    path('skills/edit/<int:skill_id>/', adminviews.edit_skill, name='edit_skill'),
    path('skills/delete/<int:skill_id>/', adminviews.delete_skill, name='delete_skill'),

    path('users_list/', adminviews.user_list, name='user_list'),
    path('view_feedback/', adminviews.view_feedback, name='view_feedback'),
    path('feedback_reply/<int:feedback_id>/', adminviews.feedback_reply, name='feedback_reply'),



    path('recruiter_dash/', recruiterviews.recruiter_dash, name='recruiter_dash'),
    path('post_job/', recruiterviews.post_job, name='post_job'),
    path('view_jobs/', recruiterviews.view_jobs, name='view_jobs'),
    path('edit_job/<int:post_id>/', recruiterviews.edit_job, name='edit_job'),
    path('delete_job/<int:post_id>/', recruiterviews.delete_job, name='delete_job'),
    path('view_profile/', recruiterviews.view_profile, name='view_profile'),
    path('edit_profile/', recruiterviews.edit_profile, name='edit_profile'),
    path('view_all_jobs/', userviews.view_all_jobs, name='view_all_jobs'),
    path('apply_job/<int:job_id>/', userviews.apply_job, name='apply_job'),
    path('my_applications/', userviews.my_applications, name='my_applications'),
    path('view_applicants/', recruiterviews.view_applicants, name='view_applicants'),
    path('admin_view_jobs/', adminviews.admin_view_jobs, name='admin_view_jobs'),



]
