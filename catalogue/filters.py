import django_filters
from .models import *
from django_filters import CharFilter, ModelMultipleChoiceFilter, MultipleChoiceFilter, ModelChoiceFilter
from django.forms.widgets import Input

class ItemFilter(django_filters.FilterSet):
    contents = CharFilter(field_name='contents',
                          lookup_expr='icontains'),
                          # widget=Input(attrs={'placeholder': 'placeholder', 'class': 'form-control'}))
    # django_filters.CharFilter(label='name_starts', method=filter_name_starts,
    #                           widget=Input(attrs={'placeholder': 'filter by first letter...', 'class': 'form-control'}))
    # category = ChoiceFilter(choices=CHOICES)
    # box = CharFilter(field_name='box__name', lookup_expr='icontains')
    # category = ModelChoiceFilter(queryset=Category.objects.all(),
    #                              widget=Input(attrs={'class': 'form-control'}))
    class Meta:
        model = Item
        fields = ('contents', 'category')
