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
from django.core.mail import EmailMessage
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
        
        # get all data fields
        userID = request.POST['userID']
        className = request.POST['className']
        professorName = request.POST['professorName']
        studentName = request.POST['studentName']
        rating = request.POST.get('rating')
        workType = request.POST.get('workType')
        professor_email = request.POST['professor_email']
        email_prof = request.POST.get('email_prof')
        report = request.POST['report']
        privacy = request.POST.get('privacy')
        if privacy == "public":
            privacy_boolean = False
        else:
            privacy_boolean = True
        
        if(email_prof == "email_prof"):
            email_prof_boolean = True
        else:
            email_prof_boolean = False
        status = "New"
        feedback = ""
        report=request.POST['report']
        professor_email=request.POST['professor_email']
        if userID == "":
            userID = "Anonymous"
            
        # check if any data fields are missing
        if email_prof == None or (professor_email == "" and email_prof_boolean == True) or report == "" or className == "" or professorName == "" or studentName == "" or rating == None or workType == None or status == "":
            return render(
                request,
                "report_page.html",
                {
                    "error_message": "You are missing one or more fields.",
                },
                )
            
        # check if file is uploaded
        try:
            evidence = Evidence(upload=request.FILES['filename'])
            fileLink = evidence.upload.url
            evidence.save()
        except Exception as e:
            fileLink = ""
    
        Report.objects.create(userID = userID, report = report, className = className, professorName = professorName, studentName = studentName, rating = rating, workType = workType, fileLink = fileLink, status=status, feedback=feedback, email_prof = email_prof_boolean, professor_email = professor_email, private = privacy_boolean)
        return render(
            request,
            "report_page.html", 
            {
                "success_message": "Report submitted.",
            },
            )
    return render(
        request,
        "report_page.html", 
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
    if request.method == 'POST':
        if request.POST.get('Resolve',False): #if resolve button is clicked
            feedback = request.POST.get('feedback')
            print(f"Feedback received: [{feedback}]")
            if feedback == "":
                return render(
                    request, 
                    'admin_specific_report_view.html', 
                    {
                        'report': report,
                        # to include in html page
                        'error_message': "You must submit feedback.",
                    },
                )
            report.feedback = feedback
            report.status = "Resolved"
            report.save()
        elif request.POST.get('Email',False): #if email button is clicked
            print(f"emailing")
            report.email_status=True
            report.save()
            msg='A student,' + report.studentName +', in your class,'+report.className+', has been reported for the following reasons:\n'+ report.report
            if report.fileLink!="":
                msg+= "\nclick here to view additional evidence:\n" + report.fileLink +"\n"
            if report.userID=="Anonymous":
                msg+="\n This was reported anonymously"
            else:
                msg+="\n Please reach back out to the reporter at "+ report.userID + " if you have any other questions or concerns."
            email = EmailMessage('Reporting '+report.studentName+' for '+report.className,
                                msg,
                                to=[report.professor_email])
            email.send()
            return render(request, 'email_sent.html')
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
    

def email(request):
    return render(request, "email_sent.html")