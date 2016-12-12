from django.contrib import admin
from .models import *
from add_items import *

admin.site.register(Nutrient)
admin.site.register(Food)
admin.site.register(Nutrient_ingredient)
admin.site.register(Search_query)
admin.site.register(Search_entry)
admin.site.register(PhysicalActivity)

