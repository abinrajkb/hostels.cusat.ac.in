from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from Application.models import Applications
from login.forms import UserForm
from login.models import VerifiedUser


def test(user):
    if user.Department_portal == "office":
        return True
    return False


# Create your views here.
@login_required(redirect_field_name='/auth/')
@user_passes_test(test, redirect_field_name='/')
def index(request):
    departments = [
        "Choose department",
        "DDU Kaushal Kendras (DDUKK)",
        "Department of Applied Chemistry",
        "Department of Applied Economics",
        "Department of Atmospheric Sciences",
        "Department of Biotechnology",
        "Department of Chemical Oceanography",
        "Department of Computer Applications",
        "Department of Computer Science",
        "Department of Electronics",
        "Department of Hindi",
        "Department of Instrumentation",
        "Department of Marine Biology, Microbiology and Biochemistry",
        "Department of Marine Geology and Geophysics",
        "Department of Mathematics",
        "Department of Physical Oceanography",
        "Department of Physics",
        "Department of Polymer Science and Rubber Technology",
        "Department of Ship Technology",
        "Department of Statistics",
        "Inter University Centre for IPR Studies (IUCIPRS)",
        "International School of Photonics",
        "National Centre for Aquatic Animal Health (NCAAH)",
        "School of Engineering",
        "School of Environmental Studies",
        "School of Industrial Fisheries",
        "School of Legal Studies",
        "School of Management Studies"]
    context = {
        "departments": departments,
        "models": Applications.objects.all()
    }
    return render(request, 'Hostel_office/index.html', context)


@login_required(redirect_field_name='/auth/')
@user_passes_test(test, redirect_field_name='/')
def get_data(request):
    # print(request.POST)
    models = Applications.objects.all().filter(Department=request.POST['dept'], Course_of_study=request.POST['course'],
                                               Gender=request.POST['gender'], verified_department='1',year_back='0')
    sortedmodels = sorted(models, key=lambda x: x.create_priority_value(), reverse=True)
    return render(request, 'Hostel_office/get_data.html', {'models': sortedmodels})


@login_required(redirect_field_name='/auth/')
@user_passes_test(test, redirect_field_name='/')
def save_data(request):
    select = request.POST['select']
    reg = request.POST['reg']
    ischeck = request.POST['ischeck']
    room = request.POST['room']
    print(ischeck)
    models = Applications.objects.get(Registration_No=reg)
    if ischeck == 'true':
        if select != "":
            models.admitted = 1
            models.Hostel_admitted = select
            models.Room_No = room
    else:
        models.admitted = 0
        models.Hostel_admitted = None
        models.Room_No = 0
    models.save()
    return HttpResponse("hello")


@login_required(redirect_field_name='/auth/')
@user_passes_test(test, redirect_field_name='/')
def add_dept(request):
    departments = [
        "Choose department",
        "DDU Kaushal Kendras (DDUKK)",
        "Department of Applied Chemistry",
        "Department of Applied Economics",
        "Department of Atmospheric Sciences",
        "Department of Biotechnology",
        "Department of Chemical Oceanography",
        "Department of Computer Applications",
        "Department of Computer Science",
        "Department of Electronics",
        "Department of Hindi",
        "Department of Instrumentation",
        "Department of Marine Biology, Microbiology and Biochemistry",
        "Department of Marine Geology and Geophysics",
        "Department of Mathematics",
        "Department of Physical Oceanography",
        "Department of Physics",
        "Department of Polymer Science and Rubber Technology",
        "Department of Ship Technology",
        "Department of Statistics",
        "Inter University Centre for IPR Studies (IUCIPRS)",
        "International School of Photonics",
        "National Centre for Aquatic Animal Health (NCAAH)",
        "School of Engineering",
        "School of Environmental Studies",
        "School of Industrial Fisheries",
        "School of Legal Studies",
        "School of Management Studies"]
    context = {
        "departments": departments,
        "models": Applications.objects.all()
    }
    return render(request, 'Hostel_office/add_data.html', context)


@login_required(redirect_field_name='/auth/')
@user_passes_test(test, redirect_field_name='/')
def create(request):
    departments = [
        "Choose department",
        "DDU Kaushal Kendras (DDUKK)",
        "Department of Applied Chemistry",
        "Department of Applied Economics",
        "Department of Atmospheric Sciences",
        "Department of Biotechnology",
        "Department of Chemical Oceanography",
        "Department of Computer Applications",
        "Department of Computer Science",
        "Department of Electronics",
        "Department of Hindi",
        "Department of Instrumentation",
        "Department of Marine Biology, Microbiology and Biochemistry",
        "Department of Marine Geology and Geophysics",
        "Department of Mathematics",
        "Department of Physical Oceanography",
        "Department of Physics",
        "Department of Polymer Science and Rubber Technology",
        "Department of Ship Technology",
        "Department of Statistics",
        "Inter University Centre for IPR Studies (IUCIPRS)",
        "International School of Photonics",
        "National Centre for Aquatic Animal Health (NCAAH)",
        "School of Engineering",
        "School of Environmental Studies",
        "School of Industrial Fisheries",
        "School of Legal Studies",
        "School of Management Studies"]
    context = {
        "departments": departments,
        "models": Applications.objects.all(),
    }
    if request.method == 'POST':
        dupli_user = VerifiedUser.objects.filter(username=request.POST['username'])
        print(dupli_user)
        if (not dupli_user):
            Dept_user = VerifiedUser.objects.create_user(username=request.POST['username'],
                                                         password=request.POST['password1'])
            Dept_user.is_active = True
            Dept_user.Department_portal = request.POST['dept']
            Dept_user.Accessible = request.POST['course']
            Dept_user.save()
            return HttpResponseRedirect('/office/add_dept/')
        else:
            return HttpResponse('Duplicate User Found,Try other Name')
    else:
        return HttpResponseRedirect('/office/add_dept/')
