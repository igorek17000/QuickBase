from django.shortcuts import redirect, render

# Create your views here.
def base(request):
    if not request.user.is_authenticated:
        return redirect('/accounts/login')
    else :
        return render(request, 'dashboard/dashboard.html')