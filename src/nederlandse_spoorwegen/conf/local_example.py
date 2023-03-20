#
# Any machine specific settings when using development settings.
#

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": "nederlandse_spoorwegen",
        "USER": "nederlandse_spoorwegen",
        "PASSWORD": "nederlandse_spoorwegen",
        "HOST": "",  # Empty for localhost through domain sockets or '127.0.0.1' for localhost through TCP.
        "PORT": "",  # Set to empty string for default.
    }
}

TWO_FACTOR_FORCE_OTP_ADMIN = False
TWO_FACTOR_PATCH_ADMIN = False
