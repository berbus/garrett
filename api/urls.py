from django.urls import path
from django.urls import include

from rest_framework import routers

from . import views

from django.contrib import admin
admin.autodiscover()

router = routers.DefaultRouter()
router.register(r'exercise', views.ExerciseViewSet)
router.register(r'finding', views.FindingViewSet)
router.register(r'group', views.GroupViewSet)
router.register(r'jira_transition', views.JiraTransitionViewSet)
router.register(r'jira_issue', views.JiraIssueViewSet)
router.register(r'requirement', views.RequirementViewSet)
router.register(r'service', views.ServiceViewSet)
router.register(r'template', views.TemplateViewSet)
router.register(r'test_case', views.TestCaseViewSet)
router.register(r'user', views.UserViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
