from rest_framework.routers import Route, DynamicRoute, SimpleRouter


class AccountRouter(SimpleRouter):
    """
    A router for account view APIs, which doesn't use lookup.
    """
    routes = [
        Route(
            url=r'^{prefix}$',
            mapping={
                'post': 'create',
                'get': 'retrieve',
                'put': 'update',
                'patch': 'partial_update',
                'delete': 'destroy'
            },
            name='{basename}-list',
            detail=False,
            initkwargs={'suffix': 'List'}
        ),
        DynamicRoute(
            url=r'^{prefix}/{url_path}$',
            name='{basename}-{url_name}',
            detail=True,
            initkwargs={}
        )
    ]
