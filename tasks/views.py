from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render

from tasks.forms import EntryForm
from tasks.models import Entry, Keyword


def new_task(request):
    if request.method == 'POST':
        form = EntryForm(request.POST)

        if form.is_valid():
            url = form.cleaned_data['url']
            email = form.cleaned_data['email']
            keywords = form.cleaned_data['keywords'].split(',')
            end_date = form.cleaned_data['end_date']
            task_entry = Entry(url=url, email=email, end_date=end_date)
            task_entry.save()
            
            for keyword in keywords:
                key = Keyword(entry=task_entry, key=keyword)
                key.save()
                
            return HttpResponseRedirect('/tasks')
        else:
            print form.errors
            return HttpResponse('Some fields are incorrect!')
    return render(request, 'tasks/tasks.new.html')

def all_tasks(request):
    entries = Entry.objects.all()

    context = {'entries': entries}

    return render(request, 'tasks/tasks.all.html', context)
