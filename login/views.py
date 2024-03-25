from django.shortcuts import render, redirect
from django.contrib.auth import logout
from django.contrib.auth.signals import user_logged_in
from django.dispatch import receiver
from login.models import Report
#from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.decorators import login_required
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy

from .models import Evidence
from .forms import ReportForm

# Create your views here.
class DocumentCreateView(CreateView):
    model = Evidence
    fields = ['upload', ]
    success_url = '/home'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        documents = Evidence.objects.all()
        context['documents'] = documents
        return context

@receiver(user_logged_in)
def redirect_after_google_login(sender, request, user, **kwargs):
    print(f"Signal received from {sender}")
    
    #return redirect('adminlanding/')
    if user.groups.filter(name='site admin').exists():
        print(f"I am an admin")
        return redirect('adminlanding/')
    else:
        print(f"I am a user")
        return redirect('userlanding/')


def home(request):
    return render(request, "login/home.html") #issue here

def logout_view(request):
    logout(request)
    return redirect("/")

def admin_view_reports(request):
    return render(request, "admin_view_reports.html")

def user_reports(request):
    return render(request, "user_reports.html")


def user_landing_view(request):
    ## retrieve user's name through database lookup
    print(f"requested user landing view")
    name = "name"
    return render(
        request, 
        "user_landing_page.html", 
    )


def admin_landing_view(request):
    print(f"requested admin landing view")
    return render(
        request, 
        "admin_landing_page.html",
    )

def report(request):
    if request.method == 'POST':
        evidence = Evidence(upload=request.FILES['filename'])
        evidence.save()
        userID = request.POST['userID']
        className = request.POST['className']
        professorName = request.POST['professorName']
        studentName = request.POST['studentName']
        rating = request.POST.get('rating')
        workType = request.POST.getlist('workType')
        fileLink = evidence.upload.url
        print(fileLink)
       
        if userID == "":
            userID = "Anonymous"
            
        Report.objects.create(userID = userID, className = className, professorName = professorName, studentName = studentName, rating = rating, workType = workType, fileLink = fileLink)
        # TODO: upload file and error checking (make sure all inputs are valid)
    return render(
        request,
        "report_page.html"
        )

def user_view_reports(request):
    reports = Report.objects.all()
    return render(request, 'user_landing.html', {'reports': reports})

    
def admin_report_view(request):
    reports = Report.objects.all()
    return render(
        request,
        "admin_report_view.html",
        {'reports' : reports},
        )
