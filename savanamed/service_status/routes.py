from flask import Blueprint


def create_blueprint() -> Blueprint:
    bp = Blueprint('service_status', __name__)

    @bp.route('/')
    def status() -> str:
        return ''

    return bp
