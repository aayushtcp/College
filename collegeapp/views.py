from django.shortcuts import render,get_object_or_404,redirect
from .models import Blog,Gallery,Course, ApplyOnline, Notice, Ourteam, FAQ, Contact,CountdownTimer,UploadedFile
import re
#! Imports class to Inherit by Aayush
from django.views.generic.base import TemplateView
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
import requests
from django.conf import settings
from django.utils.timezone import now
# Create your views here.

def home(request):
    messages = []
    name = ""

    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        email = request.POST.get('email', '').strip()
        phone = request.POST.get('phone', '').strip()

        if not name or len(name) < 3:
            messages.append("Name must be at least 3 characters long.")
        if not email or not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            messages.append("Enter a valid email address.")
        if not phone or not re.match(r"^98\d{8}$", phone):
            mobile_regex = r"^(97|98)\d{7,8}$"
            landline_regex = r"^(01|04|05|06|07)\d{6,7}$"
            if not phone or not (re.match(mobile_regex, phone) or re.match(landline_regex, phone)):
                messages.append("Enter a valid phone number.")

        if not messages:
            messages.append("Message Received Successfully!")
            context = {
                "messages": messages,
                "name": name 
            }
            return render(request, 'collegeapp/index2.html', context)
    members = Ourteam.objects.all().order_by('-id')[:4][::-1]
    notices = Notice.objects.all().order_by('-id')[:5][::-1]
    timer = CountdownTimer.objects.first() 
    context = {"members": members, "notices": notices, "messages": messages, "name": name,'timer':timer,'current_time': now()}
    return render(request, 'collegeapp/index2.html', context)



def about(request):
    return render(request,'collegeapp/about.html')

# !: This function/class updated from aayush's end
class BlogListView(ListView):
    allow_empty = True
    template_name = 'collegeapp/blog.html'
    context_object_name = 'blogs'

    def get_queryset(self):
        return Blog.objects.all().order_by('-created_at')[:10]
    
# !: This function/class updated from aayush's end
class BlogDetailView(DetailView):
    model = Blog
    template_name = 'collegeapp/BlogDepth.html'
    context_object_name = 'blog'
    
# !: This function/class updated from aayush's end
class NoticeListView(ListView):
    allow_empty= True
    template_name ='collegeapp/notice.html'
    context_object_name = 'notices'
    
    def get_queryset(self):
        return Notice.objects.all().order_by('-created_at')[:10]
    
# !: This function/class updated from aayush's end
class NoticeDetailView(DetailView):
    model = Notice
    template_name = 'collegeapp/noticeDetail.html'
    context_object_name = 'notice'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['latest_notices'] = Notice.objects.order_by('-created_at')[:10]
        return context


# !: This function/class updated from aayush's end
class OurTeamListView(ListView):
    allow_empty= True
    template_name = 'collegeapp/OurTeam.html'
    context_object_name = 'members'
    def get_queryset(self):
        return Ourteam.objects.all()

# !: This function/class updated from aayush's end
# class FAQView(ListView):
#     template_name = 'collegeapp/FAQ.html'
#     context_object_name = 'datas'
#     allow_empty= True
#     queryset = FAQ.objects.all()[::-1]
    
def faq(request):
    datas = FAQ.objects.all()[::-1]
    context = {"datas": datas}
    return render(request, 'collegeapp/FAQ.html', context)
    
class ProgramView(TemplateView):
    def get_template_names(self):
        return [self.template_name]
    

def cources(request):
    all_cources=Course.objects.all()
    context={'cources':all_cources}
    return render(request,'collegeapp/cources.html',context)


#! Recaptcha Verification if needed
def verify_recaptcha(recaptcha_response):
    secret_key = settings.RECAPTCHA_PRIVATE_KEY
    payload = {
        'secret': secret_key,
        'response': recaptcha_response
    }
    response = requests.post('https://www.google.com/recaptcha/api/siteverify', data=payload)
    result = response.json()
    return result.get('success', False)



def contact(request):
    messages = [] 
    name = ""

    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        email = request.POST.get('email', '').strip()
        subject = request.POST.get('subject', '').strip()
        message = request.POST.get('message', '').strip()
        phone = request.POST.get('phone', '').strip()

        if not name or len(name) < 3: 
            messages.append("Name must be at least 3 characters long.") 
        if not email or not re.match(r"[^@]+@[^@]+\.[^@]+", email): 
            messages.append("Enter a valid email address.") 
        if not subject or len(subject) < 5: 
            messages.append("Subject must be at least 5 characters long.") 
        if not message or len(message) < 10: 
            messages.append("Message must be at least 10 characters long.") 
        if not phone or not re.match(r"^98\d{8}$", phone):
            mobile_regex = r"^(97|98)\d{7,8}$"
            landline_regex = r"^(01|04|05|06|07)\d{6,7}$"
            if not phone or not(re.match(mobile_regex, phone) or re.match(landline_regex, phone)):
                messages.append("Enter a valid phone number.")

        secret_key = '6Lf31c4qAAAAAJypKwByiJEZPuBsGdTgaaO741q3'
        recaptcha_response = request.POST.get('g-recaptcha-response')
        recaptcha_url = 'https://www.google.com/recaptcha/api/siteverify'
        recaptcha_data = {'secret': secret_key, 'response': recaptcha_response}
        recaptcha_result = requests.post(recaptcha_url, data=recaptcha_data).json()

        if not recaptcha_result.get('success'):
            messages.append("Invalid reCAPTCHA. Please try again.")

        if not messages:  
            from collegeapp.models import Contact  
            tosave = Contact(name=name, email=email, subject=subject, message=message, phone=phone)
            tosave.save()
            messages.append("Message Received Successfully!")

    context = {'messages': messages, 'name': name}  
    return render(request, 'collegeapp/contact.html', context)

# # Gallery Views
def gallery(request):
    gallery_images = Gallery.objects.all()
    context={'images':gallery_images}
    return render(request, 'collegeapp/gallery.html',context)



# !Aayush Code starts----------------------------------------------------------------
# !----------------------------------------------------------------------------------

def applyonline(request):
    messages = []
    fullname = ""

    if request.method == "POST":
        fullname = request.POST.get('fullname', '').strip()
        program = request.POST.get('program', '').strip()
        phone = request.POST.get('phone', '').strip()
        email = request.POST.get('email', '').strip()
        previous_college = request.POST.get('previouscollege', '').strip()
        message = request.POST.get('message', '').strip()

        if not fullname or len(fullname) < 3:
            messages.append("Name must be at least 3 characters long.")
        if not email or not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            messages.append("Enter a valid email address.")
        if not message or len(message) < 10:
            messages.append("Message must be at least 10 characters long.")
        if not phone or not re.match(r"^98\d{8}$", phone):
            mobile_regex = r"^(97|98)\d{7,8}$"
            landline_regex = r"^(01|04|05|06|07)\d{6,7}$"
            if not phone or not (re.match(mobile_regex, phone) or re.match(landline_regex, phone)):
                messages.append("Enter a valid phone number.")

        recaptcha_response = request.POST.get('g-recaptcha-response')
        if not verify_recaptcha(recaptcha_response):
            messages.append("reCAPTCHA verification failed. Please try again.")

        if not messages:
            from collegeapp.models import ApplyOnline
            tosave = ApplyOnline(fullname=fullname, program=program, phone=phone, email=email, previous_College=previous_college, message=message)
            tosave.save()
            messages.append("Message Received Successfully!")

    context = {'messages': messages, 'fullname': fullname}
    return render(request, 'collegeapp/applyOnline.html', context)
class AboutLeadershipView(TemplateView):
    template_name = 'collegeapp/leadership.html'

def helloworld(request):
    return render(request,'collegeapp/helloworld.html')
def Downloads(request):
    files=UploadedFile.objects.all()[::-1]
    context={'files':files}
    return render(request,'collegeapp/downloads.html',context)

class PrivacyPolicyView(TemplateView):
    template_name = 'collegeapp/privacypolicy.html'

# from django.shortcuts import render, get_object_or_404, redirect
# from django.http import HttpResponse
# from .models import Blog, Course, Semester, Subject, Contact, Appointment, Gallery

# # Blog Views
# def blog_list(request):
#     blogs = Blog.objects.all()
#     return render(request, 'courses/blog_list.html', {'blogs': blogs})

# def blog_detail(request, blog_id):
#     blog = get_object_or_404(Blog, id=blog_id)
#     return render(request, 'courses/blog_detail.html', {'blog': blog})

# # Course Views
# def course_list(request):
#     courses = Course.objects.all()
#     return render(request, 'courses/course_list.html', {'courses': courses})

# def course_detail(request, course_id):
#     course = get_object_or_404(Course, id=course_id)
#     semesters = course.semesters.all()  # Related name from Semester model
#     return render(request, 'courses/course_detail.html', {
#         'course': course,
#         'semesters': semesters
#     })

# def semester_detail(request, semester_id):
#     semester = get_object_or_404(Semester, id=semester_id)
#     subjects = semester.subjects.all()  # Related name from Subject model
#     return render(request, 'courses/semester_detail.html', {
#         'semester': semester,
#         'subjects': subjects
#     })

# # Contact Views
# def contact(request):
#     if request.method == 'POST':
#         name = request.POST.get('name')
#         email = request.POST.get('email')
#         subject = request.POST.get('subject')
#         message = request.POST.get('message')
#         phone = request.POST.get('phone')

#         # Save the contact form data
#         Contact.objects.create(
#             name=name,
#             email=email,
#             subject=subject,
#             message=message,
#             phone=phone
#         )
#         return HttpResponse('Thank you for your message!')

#     return render(request, 'courses/contact.html')

# # Appointment Views
# def book_appointment(request):
#     if request.method == 'POST':
#         name = request.POST.get('name')
#         email = request.POST.get('email')
#         phone = request.POST.get('phone')

#         # Save the appointment form data
#         Appointment.objects.create(
#             name=name,
#             email=email,
#             phone=phone
#         )
#         return HttpResponse('Appointment booked successfully!')

#     return render(request, 'courses/book_appointment.html')

