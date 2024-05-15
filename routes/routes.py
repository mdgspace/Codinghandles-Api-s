from controllers import home, auth , codeforces, codeshef, leetcode, interviewbit

def setup_routes(router):
    router.add_get('/', home.get_home)
    router.add_get('/auth/login', auth.login)
    router.add_get('/auth/callback', auth.callback)
    router.add_get('/api/codeforces/user/{user}', codeforces.getUser)
    router.add_get('/api/codeforces/contests', codeforces.getContests)
    router.add_get('/api/codeforces/submissions/{user}', codeforces.getSubmissions)
    router.add_get('/api/codeshef/user/{user}', codeshef.getUser)
    router.add_get('/api/codeshef/contests', codeshef.getContests)
    router.add_get('/api/codeshef/submissions/{user}', codeshef.getSubmissions)
    router.add_get('/api/leetcode/user/{user}', leetcode.getUser)
    router.add_get('/api/leetcode/submissions/{user}', leetcode.getSubmissions)
    router.add_get('/api/leetcode/contests', leetcode.getContests)
    router.add_get('/api/interviewbit/user/{user}', interviewbit.getUser)
    router.add_get('/api/interviewbit/submissions/{user}', interviewbit.getSubmissions)
    router.add_get('/api/interviewbit/contests', interviewbit.getContests)
