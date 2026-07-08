# txrx.org media on DO Spaces

Purpose: hand off to the modernizing Claude. The 3.3G of user uploads that used to live at `~/projects/txrx.org/.media/uploads/` on the old droplet were moved to DigitalOcean Spaces so skade doesn't have to hold them.

## Bucket

- Name: `skade`
- Region: `nyc3`
- Origin URL: `https://skade.nyc3.digitaloceanspaces.com/`
- CDN URL: `https://skade.nyc3.cdn.digitaloceanspaces.com/` (verify CDN is enabled on the bucket; if it isn't, DO console → bucket → Settings → CDN)
- Prefix for this project: `txrx/`

## What was uploaded (public-read)

| Local path (source droplet) | Spaces key prefix | Size |
| --- | --- | --- |
| `.media/uploads/` | `s3://skade/txrx/uploads/` | 3.3G |

## What was NOT uploaded

Not shipped to skade or Spaces — decide per modernization:

| Local path (source droplet) | Size | Notes |
| --- | --- | --- |
| `.media/banners/` | 32K | Trivial — copy to `s3://skade/txrx/banners/` if the app references them. |
| `.media/bulkemail/` | 60M | Historic bulk-email attachments. Skip unless someone needs the archive. |
| `.media/floorplans/` | 3.2M | Static-ish diagrams. Copy if the app links them. |
| `.media/cache/` | 216M | `sorl-thumbnail` cache. Do NOT ship. Regenerated on demand. |

To sync any of the small dirs from the old droplet, on unrest:

```bash
~/.local/bin/s3cmd sync -P /home/django/projects/txrx.org/.media/banners/ s3://skade/txrx/banners/
```

Credentials are already in `~/.s3cfg` on unrest and at the bottom of `main/settings/local.py` (see below).

## Credentials

`main/settings/local.py` on the source and destination both contain:

```
DIGITAL_OCEAN_SPACES_KEY="DO801N7WT7A9DD7DJ9R9"
DIGITAL_OCEAN_SPACES_SECRET="<43-char secret>"
```

The secret was pasted in chat while setting this up — **rotate it** at https://cloud.digitalocean.com/account/api/spaces once the modernization is done, then update `local.py` on skade with the new pair.

## Django wiring (for whatever version you land on)

Install `django-storages` and `boto3`:

```
pip install "django-storages[boto3]"
```

Add to `main/settings/local.py` (or a new `spaces.py` module imported by settings):

```python
from .local import DIGITAL_OCEAN_SPACES_KEY, DIGITAL_OCEAN_SPACES_SECRET  # or read from env

# Django >= 4.2 preferred form:
STORAGES = {
    "default": {
        "BACKEND": "storages.backends.s3.S3Storage",
        "OPTIONS": {
            "access_key": DIGITAL_OCEAN_SPACES_KEY,
            "secret_key": DIGITAL_OCEAN_SPACES_SECRET,
            "bucket_name": "skade",
            "region_name": "nyc3",
            "endpoint_url": "https://nyc3.digitaloceanspaces.com",
            "location": "txrx",           # so the key becomes txrx/<upload_to>/<filename>
            "default_acl": "public-read",
            "file_overwrite": False,
            "querystring_auth": False,    # public objects, no signed URLs
            "custom_domain": "skade.nyc3.cdn.digitaloceanspaces.com",  # CDN in URLs
        },
    },
    "staticfiles": {
        "BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage",
    },
}

MEDIA_URL = "https://skade.nyc3.cdn.digitaloceanspaces.com/txrx/"
```

If you end up on Django < 4.2, use the legacy pair instead:

```python
DEFAULT_FILE_STORAGE = "storages.backends.s3boto3.S3Boto3Storage"
AWS_ACCESS_KEY_ID = DIGITAL_OCEAN_SPACES_KEY
AWS_SECRET_ACCESS_KEY = DIGITAL_OCEAN_SPACES_SECRET
AWS_STORAGE_BUCKET_NAME = "skade"
AWS_S3_ENDPOINT_URL = "https://nyc3.digitaloceanspaces.com"
AWS_S3_REGION_NAME = "nyc3"
AWS_LOCATION = "txrx"
AWS_DEFAULT_ACL = "public-read"
AWS_QUERYSTRING_AUTH = False
AWS_S3_CUSTOM_DOMAIN = "skade.nyc3.cdn.digitaloceanspaces.com"
AWS_S3_FILE_OVERWRITE = False
MEDIA_URL = f"https://{AWS_S3_CUSTOM_DOMAIN}/{AWS_LOCATION}/"
```

## Do the DB paths line up?

The Django DB rows have `FileField`/`ImageField` values like `uploads/photos/2016/03/foo.jpg` (relative to MEDIA_ROOT). With `AWS_LOCATION = "txrx"`, Django will build URLs as:

```
{AWS_S3_CUSTOM_DOMAIN}/{AWS_LOCATION}/<field-value>
= skade.nyc3.cdn.digitaloceanspaces.com/txrx/uploads/photos/2016/03/foo.jpg
```

Since files were uploaded to `s3://skade/txrx/uploads/...`, the URLs will resolve without a data migration. Spot-check with:

```sql
SELECT photo FROM auth_user_userprofile WHERE photo IS NOT NULL LIMIT 3;
```

and paste one into `https://skade.nyc3.cdn.digitaloceanspaces.com/txrx/<value>`.

## nginx block (skade)

`/media/` on `txrx.unrest.io` doesn't need to be served by nginx anymore — the URLs point at Spaces directly. You can drop the `location /media/` alias from the nginx block. Keep `/static/` local (that's collectstatic output, not user content).

If you *want* `/media/` URLs to stay on `txrx.unrest.io` (single-origin), use a proxy_pass to the CDN:

```nginx
location /media/ {
    proxy_pass https://skade.nyc3.cdn.digitaloceanspaces.com/txrx/;
    proxy_set_header Host skade.nyc3.cdn.digitaloceanspaces.com;
    proxy_ssl_server_name on;
}
```

Then set `MEDIA_URL = "/media/"` instead of the CDN URL.

## Signatures (heads-up)

The old nginx config had `location /media/signatures/` proxied through Django for auth. That directory doesn't exist on disk in the source — signatures may be generated dynamically by the `jsignature` app and not stored as files. If they *are* files that end up in `uploads/signatures/` after modernization, those should probably be **private** (signed URLs, not public-read). Search the codebase for `jsignature` and `SIGNATURE_ROOT` before deciding.
