# -*-coding:utf-8-*-

def get_current_user(request):
    current_user = request.COOKIES.get('user_name', '')
    return current_user