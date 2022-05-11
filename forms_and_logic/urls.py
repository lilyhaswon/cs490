from django.urls import path

from forms_and_logic.views import (
	account_view,
)

app_name = 'forms_and_logic'

urlpatterns = [
	path('<user_id>/', account_view, name="view"),
]