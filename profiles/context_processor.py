"""
This function allows django to access profile
data from any view template.
"""

from .models import Profile

def profile_context(request):
    """
    A function that defines custom context processor
    for profile data.
    """
    profiles = Profile.objects.all()
    return {'profiles': profiles}
