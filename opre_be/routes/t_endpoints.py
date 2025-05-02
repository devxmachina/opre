from flask import Blueprint, jsonify, current_app
from sqlalchemy import text
from .auth import login_required  # 데코레이터 import
from ..services import services

test_bp = Blueprint("test", __name__)

@test_bp.route("/ping", methods=['GET'])
def ping():
  return 'pooooong'


@test_bp.route("/", methods=['GET'])
@login_required
def home():

  with test_bp.database.connect() as conn:
    results = conn.execute(text("""SELECT * FROM users""")).mappings()
    # columns = result.keys()  # 열 이름을 얻음te
    # all_users = [dict(zip(columns, row)) for row in result.fetchall()]
    all_users = [dict(row) for row in results]
  
    return jsonify(all_users)
