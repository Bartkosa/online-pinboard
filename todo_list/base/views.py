from django.shortcuts import render, redirect
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django import forms
import calendar
from calendar import HTMLCalendar
from .models import *


class CustomLoginView(LoginView):
    template_name = 'base/login.html'
    fields = '__all__'
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy('tasks')


class RegisterView(FormView):
    template_name = 'base/register.html'
    form_class = UserCreationForm
    redirect_authenticated_user = True
    success_url = reverse_lazy('tasks')

    def form_valid(self, form):
        user = form.save()
        if user is not None:
            login(self.request, user)
        return super(RegisterView, self).form_valid(form)

    def get(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('tasks')
        return super(RegisterView, self).get(*args, **kwargs)


def calendar_view(request, year, month):
    if month == 13:
        year = datetime.now().year
        month = datetime.now().strftime("%B")
    month = month.capitalize()
    month_num = list(calendar.month_name).index(month)

    def prev_month(m):
        return m - 1 if m > 1 else 12

    def next_month(m):
        return m + 1 if m < 12 else 1

    now = datetime.now()
    cal = HTMLCalendar()
    html_calendar = cal.formatmonth(year, month_num)
    events = Event.objects.filter(start_date__year=year, start_date__month=month_num, user=request.user)

    day_events = {}
    for event in events:
        if event.start_date.day not in day_events:
            day_events[event.start_date.day] = []
        day_events[event.start_date.day].append((event.title, reverse('event-update', kwargs={'pk': event.id}),
                                                 event.start_date))

    for day, day_event in day_events.items():
        print(day, day_event)
        event_str = ""
        for title, update_url, start_date in day_event:
            event_str += f'-<a style="color: #00A92FFF" href="{update_url}">'
            event_str += f'<b>{title}</b></a><br>'
            this_date = start_date
        if day == now.day:
            html_calendar = html_calendar.replace(
                f'<td class="{now.strftime("%a").lower()}">{day}</td>',
                f'<td style="background-color: #ffadbd; " class="{now.strftime("%a").lower()}">'
                f'{day}<br>{event_str}</td>')
        else:
            print(event_str, now.strftime("%a").lower())
            html_calendar = html_calendar.replace(
                f'<td class="{this_date.strftime("%a").lower()}">{day}</td>',
                f'<td class="{this_date.strftime("%a").lower()}">'
                f'{day}<br>{event_str}</td>')

    time = now.strftime('%I:%M %p')
    return render(request, 'base/calendar.html',
                  {"year": year, "month": month, "month_number": month_num, "cal": html_calendar,
                   "time": time, "prev_month": calendar.month_name[prev_month(month_num)].capitalize(),
                   "next_month": calendar.month_name[next_month(month_num)].capitalize(),
                   "events": events})


class TaskList(LoginRequiredMixin, ListView):
    model = Task
    context_object_name = 'tasks'

    def get_context_data(self, **kwargs):
        now = datetime.now()
        year = now.year
        month = now.strftime("%B")
        events = Event.objects.filter(start_date__year=year, start_date__month=now.month, user=self.request.user)
        cal = HTMLCalendar().formatmonth(year, now.month)
        for event in events:
            if event.start_date.date() == datetime.now().date():
                cal = cal.replace(
                    f'<td class="{event.start_date.strftime("%a").lower()}">{event.start_date.day}</td>',
                    f'<td style="color: #3455db; background-color: #ff76a7; " class="{event.start_date.strftime("%a").lower()}">'
                    f'<b>{event.start_date.day}</b><br></td>')
            else:
                cal = cal.replace(
                    f'<td class="{event.start_date.strftime("%a").lower()}">{event.start_date.day}</td>',
                    f'<td style="color: #3455db; " class="{event.start_date.strftime("%a").lower()}">'
                    f'<b>{event.start_date.day}</b><br></td>')

        cal = cal.replace(
            f'<td class="{now.strftime("%a").lower()}">{now.day}</td>',
            f'<td style="background-color: #ff76a7; " class="{now.strftime("%a").lower()}">'
            f'{now.day}<br></td>')

        context = super().get_context_data(**kwargs)
        context['tasks'] = context['tasks'].filter(user=self.request.user)
        context['count'] = context['tasks'].filter(complete=False).count()
        context['habits'] = Habit.objects.all()
        context['habits'] = context['habits'].filter(user=self.request.user)
        context['year'] = year
        context['month'] = month
        context['cal'] = cal
        search_input = self.request.GET.get('search-area') or ''
        if search_input:
            context['tasks'] = context['tasks'].filter(title__startswith=search_input)

        context['search_input'] = search_input
        return context


class TaskDetail(LoginRequiredMixin, DetailView):
    model = Task
    context_object_name = 'task'
    template_name = 'base/task.html'


class TaskCreate(LoginRequiredMixin, CreateView):
    model = Task
    fields = {'title', 'description'}
    success_url = reverse_lazy('tasks')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(TaskCreate, self).form_valid(form)


class TaskUpdate(LoginRequiredMixin, UpdateView):
    model = Task
    fields = {'title', 'description'}
    success_url = reverse_lazy('tasks')


class DeleteTask(LoginRequiredMixin, DeleteView):
    model = Task
    context_object_name = 'task'
    success_url = reverse_lazy('tasks')


class HabitCreate(LoginRequiredMixin, CreateView):
    model = Habit
    fields = {'title', 'complete'}
    success_url = reverse_lazy('tasks')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(HabitCreate, self).form_valid(form)


class HabitUpdate(LoginRequiredMixin, UpdateView):
    model = Habit
    fields = {'title', 'complete'}
    success_url = reverse_lazy('tasks')


class DeleteHabit(LoginRequiredMixin, DeleteView):
    model = Habit
    context_object_name = 'habit'
    success_url = reverse_lazy('tasks')


class EventCreate(LoginRequiredMixin, CreateView):
    model = Event
    fields = {'title', 'description', 'start_date', 'end_date'}
    now = datetime.now()
    year = now.year
    month = now.strftime("%B")
    success_url = reverse_lazy('calendar', kwargs={'year': year, 'month': month})

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields['start_date'].widget = forms.TextInput(attrs={'type': 'datetime-local'})
        form.fields['end_date'].widget = forms.TextInput(attrs={'type': 'datetime-local'})
        return form

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(EventCreate, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({'year': self.year, 'month': self.month})
        return context


class EventUpdate(LoginRequiredMixin, UpdateView):
    model = Event
    fields = {'title', 'description', 'start_date', 'end_date'}
    now = datetime.now()
    year = now.year
    month = now.strftime("%B")
    success_url = reverse_lazy('calendar', kwargs={'year': year, 'month': month})


class DeleteEvent(LoginRequiredMixin, DeleteView):
    model = Event
    context_object_name = 'event'
    now = datetime.now()
    year = now.year
    month = now.strftime("%B")
    success_url = reverse_lazy('calendar', kwargs={'year': year, 'month': month})
    