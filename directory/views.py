from django.shortcuts import render

context = {}
context['user'] = "Test user"
context['firstname'] = 'tiozão'
# or
context = {
    'user'       : 'Test user',
    'firstname'  : 'tiozão',
}

# Create your views here.
def home(request):
    return render(request, 'home.html', context)

def about(request):
    return render(request, 'about.html', context)
