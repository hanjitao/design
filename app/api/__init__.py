from flask import Blueprint

api = Blueprint('api', __name__)

from .import my_poetry, generate_poetry, poetry_rank, image, my_draft
