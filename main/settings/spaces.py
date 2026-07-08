# Media on DigitalOcean Spaces (see txrx-do-spaces.md).
# Uploads live at s3://skade/txrx/uploads/... and are public-read.
# Requires DIGITAL_OCEAN_SPACES_KEY/SECRET from local.py; falls back to
# local filesystem storage when they aren't defined (fresh dev machines).
DIGITAL_OCEAN_SPACES_KEY = os.environ.get("DIGITAL_OCEAN_SPACES_KEY")
DIGITAL_OCEAN_SPACES_SECRET = os.environ.get("DIGITAL_OCEAN_SPACES_SECRET")

if DIGITAL_OCEAN_SPACES_KEY:
  STORAGES = {
    "default": {
      "BACKEND": "storages.backends.s3.S3Storage",
      "OPTIONS": {
        "access_key": DIGITAL_OCEAN_SPACES_KEY,
        "secret_key": DIGITAL_OCEAN_SPACES_SECRET,
        "bucket_name": "skade",
        "region_name": "nyc3",
        "endpoint_url": "https://nyc3.digitaloceanspaces.com",
        "location": "txrx",           # key becomes txrx/<upload_to>/<filename>
        "default_acl": "public-read",
        "file_overwrite": False,
        "querystring_auth": False,    # public objects, no signed URLs
        "custom_domain": "skade.nyc3.cdn.digitaloceanspaces.com",
      },
    },
    "staticfiles": {
      "BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage",
    },
  }
  MEDIA_URL = "https://skade.nyc3.cdn.digitaloceanspaces.com/txrx/"
  # sorl-thumbnail caches generated thumbs through the same default storage
  THUMBNAIL_FORCE_OVERWRITE = True
