def ga_key(request):
    from django_project import local_settings
    return {'GA_KEY': local_settings.GOOGLE_ANALYTICS_PROPERTY_ID}