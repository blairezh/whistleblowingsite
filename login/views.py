from django.shortcuts import render, redirect
from django.contrib.auth import logout
from django.contrib.auth.signals import user_logged_in
from django.dispatch import receiver
from login.models import Report, Evidence
#from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.decorators import login_required
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404

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
    return render(request, "login/home.html") 

def logout_view(request):
    logout(request)
    return redirect("/")

def admin_view_reports(request):
    return render(request, "admin_view_reports.html")

def public_reports(request):
    return render(request, "public_reports.html")

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
        fileLink = evidence.upload.url
        evidence.save()
        userID = request.POST['userID']
        className = request.POST['className']
        professorName = request.POST['professorName']
        studentName = request.POST['studentName']
        rating = request.POST.get('rating')
        workType = request.POST.getlist('workType')
        status = "New"
        feedback = ""
        print(fileLink)
       
        if userID == "":
            userID = "Anonymous"
            
        Report.objects.create(userID = userID, className = className, professorName = professorName, studentName = studentName, rating = rating, workType = workType, fileLink = fileLink, status=status, feedback=feedback)
        # TODO: upload file and error checking (make sure all inputs are valid)
    return render(
        request,
        "report_page.html"
        )

@login_required
def user_reports(request):
    print(f"requested user view reports")
    name = "name"
    reports = Report.objects.filter(userID=request.user.email)
    return render(request, 'user_reports.html', {'reports': reports})

    
def review_reports(request):
    reports = Report.objects.all()
    return render(
        request,
        "review_reports.html",


        {'reports' : reports},
        )
    
def admin_specific_report_view(request, pk):
    report = get_object_or_404(Report, pk=pk)
    if(report.status == "New"):
        report.status = "Seen"
        report.save()
    # add error checking
    if request.method == 'POST':
        report.feedback = request.POST.get('feedback')
        report.status = "Resolved"
        report.save()
    return render(
        request, 
        'admin_specific_report_view.html', 
        {'report': report},
        )

def report_delete(request, pk):
    report = get_object_or_404(Report, pk=pk)  

    if request.method == 'POST':         
        report.delete()                    
    return redirect('/userlanding/')            
    
