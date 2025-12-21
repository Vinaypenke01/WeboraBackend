from .models import SiteSetting

class SiteSettingService:
    @staticmethod
    def get_or_create_settings():
        settings, created = SiteSetting.objects.get_or_create(id=1)
        return settings

    @staticmethod
    def update_settings(settings_instance, data):
        for key, value in data.items():
            setattr(settings_instance, key, value)
        settings_instance.save()
        return settings_instance
