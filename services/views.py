from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView
from .models import Service


class ServiceListView(ListView):
    model = Service
    template_name = 'services/service-list.html'
    context_object_name = 'services'
    queryset = Service.objects.filter(is_active=True)


class ServiceDetailView(DetailView):
    model = Service
    template_name = 'services/service-detail.html'
    context_object_name = 'service'
    slug_field = 'slug'
    queryset = Service.objects.filter(is_active=True)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['related_services'] = Service.objects.filter(
            is_active=True
        ).exclude(id=self.object.id)[:3]
        return context
