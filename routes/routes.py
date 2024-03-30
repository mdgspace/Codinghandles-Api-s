from controllers import home, auth , codeforces, codeshef

def setup_routes(router):
    router.add_get('/', home.get_home)
    router.add_get('/auth/login', auth.login)
    router.add_get('/auth/callback', auth.callback)
    router.add_get('/api/codeforces/user/{user}', codeforces.getUser)
    router.add_get('/api/codeforces/contests', codeforces.getContests)
    router.add_get('/api/codeforces/submissions/{user}', codeforces.getSubmissions)
    router.add_get('/api/codeshef/user/{user}', codeshef.getUser)
    router.add_get('/api/codeshef/contests', codeshef.getContests)
