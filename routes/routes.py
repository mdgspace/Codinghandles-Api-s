from controllers import home, auth

def setup_routes(router):
    router.add_get('/', home.get_home)
    router.add_get('/auth/login', auth.login)
    router.add_get('/auth/callback', auth.callback)
