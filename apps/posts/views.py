"""M3 (posts) views.

The post_detail route is reserved by the integration contract. M3 replaces the
temporary 404 with the real implementation without changing its name or path.
"""

from django.http import Http404, HttpRequest, HttpResponse


def post_detail(request: HttpRequest, post_id: int) -> HttpResponse:
    raise Http404("Post detail is implemented by M3.")
