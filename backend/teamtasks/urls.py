from django.urls import path, include
from .views import JobsListView
from rest_framework.routers import DefaultRouter
from .views import StaffApplicationViewSet, UserDetailsViewSet, TaskViewSet, TaskCommentViewSet,UnassignedSymbolListView

# Create a router and register the viewsets
router = DefaultRouter()
router.register(r'staff-applications', StaffApplicationViewSet, basename='staff-application')
router.register(r'user-details', UserDetailsViewSet, basename='user-detail')
router.register(r'tasks', TaskViewSet, basename='task')
router.register(r'task-comments', TaskCommentViewSet, basename='task-comment')


#Example URLs Generated:
#StaffApplication URLs:#
#
#GET /staff-applications/: List all staff applications or create a new one.
#POST /staff-applications/{id}/approve/: Approve a specific staff application.
#POST /staff-applications/{id}/disapprove/: Disapprove a specific staff application.
#UserDetails URLs:
#
#GET /user-details/: List user details or create new user details.
#GET /user-details/{id}/: Retrieve, update, or delete a specific user's details.
#Task URLs:
#
#GET /tasks/: List all tasks or create a new task.
#POST /tasks/{id}/complete/: Mark a task as completed.
#POST /tasks/{id}/reopen/: Reopen a previously completed task.
#TaskComment URLs:
#
#GET /task-comments/: List all comments or create a new comment for a task.
# URL patterns
urlpatterns = [
    path('jobs/', JobsListView.as_view(), name='jobs-list'),
    path('unassigned-symbols/', UnassignedSymbolListView.as_view(), name='unassigned-symbols'),
    path('', include(router.urls)),  # Include all the viewset URLs generated by the router

]


