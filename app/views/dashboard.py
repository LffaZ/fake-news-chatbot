from django.views.generic import TemplateView

from app.services.analytics_service import get_dashboard_context

class DashboardView(TemplateView):
    template_name = "dashboard.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context.update(
            get_dashboard_context()
        )

        return context