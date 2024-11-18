from django.urls import path
from . import views
"""URLS"""
urlpatterns = [
    path('', views.home, name='home'),
    path("register/", views.register, name="register"),
    path("login/", views.login_view, name="login"),
    path("dashboard/", views.dashboard, name="dashboard"),    path("create_test/", views.create_test, name="create_test"),
    path("add_questions/<int:test_id>/", views.add_questions, name="add_questions"),
    path("take_test/<int:test_id>/", views.take_test, name="take_test"),
    path("avalable_tests/", views.available_tests, name="avalable_tests"),    
    path("resolve_json_test/", views.resolve_json_test, name="resolve_json_test"),
]
