from django.db import models

class SortedModels(models.Manager):
    def get_sorted(self, hotel=None, floor=None):
        if hotel:
            return super().get_queryset().filter(hotel=hotel).order_by('sort_id')
        elif floor:
            return super().get_queryset().filter(floor=floor).order_by('sort_id')
        else:
            return super().get_queryset().order_by('sort_id')