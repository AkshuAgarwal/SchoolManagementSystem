"""Routing to React to do this"""

# from ipware import get_client_ip

# from .models import UserModel


# class RegisterLastLoginIP:
#     def __init__(self, get_response):
#         self.get_response = get_response

#     def __call__(self, request):
#         return self.get_response(request)

#     def process_request(self, request):
#         if request.user.is_authenticated():
#             ip, is_routable = get_client_ip(request)

#             if ip is not None:
#                 UserModel.objects.filter(user=request.user).update(ip_address=ip)
