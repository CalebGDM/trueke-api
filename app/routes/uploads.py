from flask import Blueprint, send_from_directory, abort, current_app
import os
from app import config

uploads = Blueprint('uploads', __name__)

@uploads.route('/<path:filename>', methods=['GET'])
def get_file(filename):
    # Sube un nivel desde app para llegar a la raíz del proyecto
    project_root = os.path.dirname(current_app.root_path)
    folder_path = os.path.join(project_root, config.Config.UPLOAD_FOLDER)
    file_path = os.path.join(folder_path, filename)
    print("Buscando archivo en:", file_path)
    if not os.path.exists(file_path):
        print("NO ENCONTRADO:", file_path)
        abort(404)
    return send_from_directory(folder_path, filename)