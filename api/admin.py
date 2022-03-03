from django.contrib import admin

import api.models as models


admin.site.register(models.Exercise)
admin.site.register(models.Finding)
admin.site.register(models.Service)
admin.site.register(models.Template)
admin.site.register(models.TestCase)
admin.site.register(models.Requirement)
