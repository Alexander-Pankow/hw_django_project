from django.http import HttpResponse
# Create your views here.

def hallo_name(request):
 return HttpResponse("<h1>Hello, Alex!</h1>")