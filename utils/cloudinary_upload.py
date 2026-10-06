"""Optional Cloudinary image uploads. Enabled when CLOUDINARY_URL or cloud name/key/secret are set."""
import os


def cloudinary_enabled():
    return bool(
        os.environ.get('CLOUDINARY_URL')
        or (os.environ.get('CLOUDINARY_CLOUD_NAME')
            and os.environ.get('CLOUDINARY_API_KEY')
            and os.environ.get('CLOUDINARY_API_SECRET'))
    )


def upload_to_cloudinary(file_storage, folder='school'):
    """Upload Werkzeug FileStorage to Cloudinary. Returns secure URL or None."""
    if not cloudinary_enabled() or not file_storage:
        return None
    try:
        import cloudinary
        import cloudinary.uploader

        if os.environ.get('CLOUDINARY_URL'):
            cloudinary.config(cloudinary_url=os.environ['CLOUDINARY_URL'])
        else:
            cloudinary.config(
                cloud_name=os.environ['CLOUDINARY_CLOUD_NAME'],
                api_key=os.environ['CLOUDINARY_API_KEY'],
                api_secret=os.environ['CLOUDINARY_API_SECRET'],
                secure=True,
            )

        result = cloudinary.uploader.upload(
            file_storage,
            folder=f"nebula-school/{folder}",
            resource_type='auto',
        )
        return result.get('secure_url')
    except Exception as e:
        print(f'Cloudinary upload error: {e}')
        return None
