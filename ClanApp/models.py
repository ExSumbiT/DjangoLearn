from allauth.socialaccount.signals import pre_social_login
from django.db import models
from django.dispatch import receiver


# @receiver(pre_social_login)
# def CreateProfile(sender, request, sociallogin, **kwargs):
#     """
# 	This function catches the signal for social login and print the extra information
# 	"""
#     print("LOGS: Caught the signal--> Printing extra data of the acccount: \n", sociallogin.account.data)
# from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
#
#
# class ProfileAdapter(DefaultSocialAccountAdapter):
#
#     def pre_social_login(self, request, sociallogin):
#         """
#         Check for extra user data and save the desired fields.
#         """
#         data = sociallogin.account.extra_data
#         user = sociallogin.account.user
#         print("LOGS: Caught the signal -> Printing extra data of the account: \n" + str(data))
#         if 'first_name' in data:
#             user.first_name = data['first_name']
#         elif 'given_name' in data:
#             user.first_name = data['given_name']
#         if 'last_name' in data:
#             user.last_name = data['last_name']
#         elif 'family_name' in data:
#             user.last_name = data['family_name']
#         user.save()


class Members(models.Model):
    nickname = models.TextField(blank=True, null=True)
    real_name = models.TextField(blank=True, null=True)
    birthday = models.DateTimeField(blank=True, null=True)
    country = models.TextField(blank=True, null=True)
    discord = models.TextField(blank=True, null=True)
    id = models.IntegerField(blank=True, primary_key=True)
    vacation = models.TextField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'members'

