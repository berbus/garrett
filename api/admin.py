from django.contrib import admin

import api.models as models


admin.site.register(models.Review)
admin.site.register(models.Finding)
admin.site.register(models.Service)
admin.site.register(models.Template)
admin.site.register(models.TestCase)
admin.site.register(models.Requirement)
admin.site.register(models.SecurityTest)
admin.site.register(models.ThreatModel)
admin.site.register(models.JiraIssue)
admin.site.register(models.JiraTransition)
