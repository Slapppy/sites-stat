from django.views.generic import ListView

from web.models import Counter

# TODO optimization for counter queryset


class CountersListView(ListView):
    template_name = "web/profile.html"
    model = Counter

    def get_queryset(self):
        queryset = Counter.objects.all().order_by("-created_at")
        return self.filter_queryset(queryset)

    def filter_queryset(self, counters):
        self.search = self.request.GET.get("search", None)

        if self.search:
            counters = counters.filter(name__icontains=self.search)

        return counters

    def get_context_data(self, *, object_list=None, **kwargs):
        return {
            **super(CountersListView, self).get_context_data(**kwargs),
            "search": self.search,
        }
