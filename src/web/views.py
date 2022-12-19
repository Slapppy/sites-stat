from django.shortcuts import render


from web.models import Counter


def profile_view(request):
    search = request.GET.get("search", None)
    counters = Counter.objects.all()

    if search:
        counters = counters.filter(name__icontains=search)

    return render(request, "web/profile.html", {"counters": counters, "search": search})
