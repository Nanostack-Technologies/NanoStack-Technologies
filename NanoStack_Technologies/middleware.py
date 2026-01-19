class SubdomainRoutingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        host = request.get_host().split(':')[0]
        if host == 'nanoadmin.nanostacktechnologies.com':
            request.urlconf = 'NanoStack_Technologies.urls_admin'
        return self.get_response(request)
