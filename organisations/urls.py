from django.urls import path
from .views import CreateOrganisationView

urlpatterns = [
    path(
        "organisation/",
        CreateOrganisationView.as_view(),
        name="create_organisation",
    ),
]
