import os
import sys
import django

# إعداد بيئة جانجو
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bazarna.settings')
django.setup()

from django.core.files.storage import FileSystemStorage
from cloudinary_storage.storage import MediaCloudinaryStorage
from django.conf import settings

def upload_local_media_to_cloudinary():
    if not os.getenv('CLOUDINARY_URL'):
        print("Error: CLOUDINARY_URL is not set in environment or .env file.")
        print("Please add it to your .env file first.")
        sys.exit(1)

    local_storage = FileSystemStorage(location=settings.MEDIA_ROOT)
    cloud_storage = MediaCloudinaryStorage()

    if not os.path.exists(settings.MEDIA_ROOT):
        print(f"Media folder not found at {settings.MEDIA_ROOT}")
        sys.exit(0)

    print("Starting upload of local media to Cloudinary...")
    upload_count = 0
    skip_count = 0

    for root, dirs, files in os.walk(settings.MEDIA_ROOT):
        for file in files:
            # Get the relative path exactly as it is stored in the database
            local_path = os.path.relpath(os.path.join(root, file), settings.MEDIA_ROOT)
            
            # Use forward slashes for Cloudinary paths
            cloud_path = local_path.replace('\\', '/')
            
            print(f"Processing: {cloud_path}...", end=" ")
            
            # Check if file exists in Cloudinary
            if not cloud_storage.exists(cloud_path):
                with local_storage.open(local_path, 'rb') as f:
                    cloud_storage.save(cloud_path, f)
                print("UPLOADED ✅")
                upload_count += 1
            else:
                print("SKIPPED (Already exists) ⏭️")
                skip_count += 1

    print("\nMigration Summary:")
    print(f"- Files Uploaded: {upload_count}")
    print(f"- Files Skipped: {skip_count}")
    print("- Database remains fully compatible with these files.")
    print("\nDONE!")

if __name__ == '__main__':
    upload_media_to_cloudinary()
