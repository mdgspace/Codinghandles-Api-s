from controllers import home, auth , codeforces

def setup_routes(router):
    router.add_get('/', home.get_home)
    router.add_get('/auth/login', auth.login)
    router.add_get('/auth/callback', auth.callback)
    router.add_get('/api/codeforces/getUser', codeforces.getUser)
