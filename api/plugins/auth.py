from rest_framework.authentication import BasicAuthentication

class GlobalAuth(BasicAuthentication):
    def authenticate(self, request):
        user_cookie = request.COOKIES.get('token')
        if user_cookie:
            session_match = request.session.get(user_cookie)

            if session_match:
                return (session_match,user_cookie)
        return None