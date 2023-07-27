from django_filters import FilterSet, DateFilter, CharFilter, ModelMultipleChoiceFilter, MultipleChoiceFilter
from django_filters.widgets import forms
from .models import Post, Category
from datetime import date


class PostFilter(FilterSet):
    name = CharFilter(
        field_name='name',
        label='Name',
        lookup_expr='icontains'
    )

    category = ModelMultipleChoiceFilter(
        field_name='postcategory__category',
        queryset=Category.objects.all(),
        label='Category')

    date = DateFilter(
        field_name='date',
        widget=forms.DateInput(attrs={'type': 'date'}),
        lookup_expr='gt', label='After Date'
    )

    class Meta:
        model = Post
        fields = ['name', 'category', 'date', 'type']

