import os
from datetime import datetime
from werkzeug.utils import secure_filename
from app import config

def upload_image(request):
    if 'profile_picture' in request.files:
            file = request.files['profile_picture']
            if file.filename != '':
                # Generar el nomnbre
                timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
                filename = secure_filename(f"{timestamp}_{file.filename}")
                file.save(os.path.join(config.Config.UPLOAD_FOLDER, filename))
                
                image_url = f"{request.host_url[:-1]}{config.Config.UPLOAD_URL}{filename}"
                return image_url
            else:
                return None
    else:
        return None
    
def upload_images(request):
    images_urls = []
    if 'images_url' in request.files:
        files = request.files.getlist('images_url')
        print("Archivos recibidos:", files)
        for file in files:
            if file.filename != '':
                # Generar el nomnbre
                timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
                filename = secure_filename(f"{timestamp}_{file.filename}")
                file.save(os.path.join(config.Config.UPLOAD_FOLDER, filename))
                
                image_url = f"{request.host_url[:-1]}{config.Config.UPLOAD_URL}{filename}"
                print(image_url)
                images_urls.append(image_url)
        return images_urls
    if not images_urls and request.form.get('images_url'):
        images_urls = request.form.get('images_url').split(',')
    return images_urls
   
    