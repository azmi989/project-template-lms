from django.urls import path

from .views import (
	user_view,
	edit_user_view,
)

app_name = 'account'

urlpatterns = [
	path('<username>/', user_view, name="view"),
	path('<username>/edit/', edit_user_view, name="edit"),
]
