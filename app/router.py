from app import views


def setup_routes(app):
    app.router.add_route('POST', '/create', views.UrlView, name='url-create')
    app.router.add_route('GET', '/{url}', views.UrlRedirectView, name='url-redirect')
