from django.contrib.auth.views import LoginView
from django.urls import reverse

from django.urls import reverse


class SmartLoginView(LoginView):
    template_name = 'users/auth/login.html'

    def get_success_url(self):
        user = self.request.user
        skill = self.request.GET.get('skill')
        postal = self.request.GET.get('postalcode')

        # اولویت اول: جستجوی خاص
        if skill and postal:
            return f"/searching_skills/?skill={skill}&postalcode={postal}"

        if user.is_superuser:
            return reverse('adminPanel:dashboard')
        return reverse('user_dashboard')


# class SmartLoginView(LoginView):
#     template_name = 'users/auth/login.html'
#
#     def get_success_url(self):
#         skill = self.request.GET.get('skill')
#         postal = self.request.GET.get('postalcode')
#
#         if skill and postal:
#             return f"/searching_skills/?skill={skill}&postalcode={postal}"
#         try:
#             return reverse('user_dashboard')
#         except:
#             return '/users/dashboard/'