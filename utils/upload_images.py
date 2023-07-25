import os
from cloudinary import utils, uploader
from django.conf import settings


def upload_cloud_image(image) -> str:
    temp_path = os.path.join(settings.MEDIA_ROOT, "temp", image.name)

    with open(temp_path, "wb") as temp_file:
        for chunk in image.chunks():
            temp_file.write(chunk)

    cloudinary_response = uploader.upload(temp_path)
    image_url = cloudinary_response["secure_url"]
    os.remove(temp_path)
    return image_url


def destroy_cloud_image(image_url: str) -> bool:
    filename = os.path.basename(image_url)
    filename_without_extension = os.path.splitext(filename)[0]

    if filename_without_extension != 'no-photo':
        response = uploader.destroy(filename_without_extension)
        
        if response["result"] == "ok":
            return True   
        else:
            return False
    else:
        return True
