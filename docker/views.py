from django.shortcuts import render
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required
def application(request):
    context={}
    context['uri']='application'
    context['with_group']=False
    context['with_new']=True
    return render(request,'list.html',context)