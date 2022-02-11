from django.shortcuts import redirect, render

# Create your views here.
def base(request):
    if not request.user.is_authenticated:
        return redirect('/accounts/login')
    else :
        return render(request, 'dashboard/dashboard.html')

def marche(request):
    if not request.user.is_authenticated:
        return redirect('/accounts/login')
    else :
        return render(request, 'dashboard/marche.html')

def transactions(request):
    if not request.user.is_authenticated:
        return redirect('/accounts/login')
    else :
        return render(request, 'dashboard/transactions.html')

def trades(request):
    if not request.user.is_authenticated:
        return redirect('/accounts/login')
    else :
        return render(request, 'dashboard/trades.html')