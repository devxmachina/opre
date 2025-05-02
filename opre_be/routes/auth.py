# from flask import Blueprint, request, jsonify, current_app, Response, g
# from sqlalchemy import text
# from sqlalchemy.exc import IntegrityError
# from datetime import datetime, timedelta, timezone

# import bcrypt
# import jwt


# def get_user_id_and_password(email):
#   with current_app.database.connect() as conn:
#     row = conn.execute(text(
#       """
#         SELECT
#           id,
#           password
#         FROM users
#         WHERE email = :email
#       """
#     ), {'email': email}).mappings().fetchone()

#     return {
#       'id': row['id'],
#       'hashed_password': row['password']
#     } if row else None



# auth_bp = Blueprint("auth", __name__)

# @auth_bp.route("/login", methods=["POST"])
# def login():
#     credential = request.json
#     email = credential['email']
#     password = credential['password']

#     user_credential = get_user_id_and_password(email)

#     # 존재하지 않거나 비밀번호 해시가 없는 경우
#     if not user_credential or not user_credential['hashed_password']:
#       return jsonify({'message': 'Invalid email or password'}), 401

#     # 비밀번호 검증 디버깅용 출력
#     print("LOGIN EMAIL:", email)
#     print("RAW INPUT PASSWORD:", password)
#     print("HASHED FROM DB:", user_credential['hashed_password'])
#     try:
#       result = bcrypt.checkpw(password.encode('UTF-8'), user_credential['hashed_password'].encode('UTF-8'))
#       print("BCRYPT RESULT:", result)
#     except Exception as e:
#       print("BCRYPT ERROR:", str(e))
#       return jsonify({'message': 'Bcrypt error: ' + str(e)}), 500

#     if result:
#       user_id = user_credential['id']
#       payload = {
#         'user_id': user_id,
#         'exp': datetime.now(timezone.utc) + timedelta(seconds=60 * 60 * 24)
#       }
#       token = jwt.encode(payload, current_app.config['JWT_SECRET_KEY'], algorithm='HS256')
#       return jsonify({
#         'user_id': user_id,
#         'access_token': token
#       })
#     else:
#       return jsonify({'message': 'Invalid email or password'}), 401

# @auth_bp.route("/register", methods=["POST"])
# def register():
#     new_user = request.json
#     new_user['password'] = bcrypt.hashpw(
#       new_user['password'].encode('UTF-8'),
#       bcrypt.gensalt()
#     ).decode('UTF-8')
#     try:
#       with app.database.connect() as conn:
#         new_user_id = conn.execute(text(
#           """
#             INSERT INTO users (
#               name,
#               email,
#               profile,
#               password
#             ) VALUES (
#               :name,
#               :email,
#               :profile,
#               :password
#             )
#           """
#         ), new_user).lastrowid

#         conn.commit()

#         row = conn.execute(text(
#           """
#             SELECT id, name, email, profile
#             FROM users
#             WHERE id = :user_id
#           """
#         ), {'user_id': new_user_id}).mappings().first()

#         return jsonify({
#             'id': row['id'],
#             'name': row['name'],
#             'email': row['email'],
#             'profile': row['profile']
#         })
#     except IntegrityError:
#       return jsonify({'message': 'This email is already registered.'}), 409
from functools import wraps
from flask import Blueprint, request, Response, jsonify, current_app, g
from sqlalchemy import text
from sqlalchemy.exc import IntegrityError
from datetime import datetime, timedelta, timezone
import bcrypt
import jwt
from ..services import services

auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/login", methods=["POST"])
def login():
    credential = request.json
    email = credential['email']
    password = credential['password']

    user_credential = services.get_user_id_and_password(email)
    if not user_credential or not user_credential['hashed_password']:
        return jsonify({'message': 'Invalid email or password'}), 401

    if bcrypt.checkpw(password.encode('utf-8'), user_credential['hashed_password'].encode('utf-8')):
        user_id = user_credential['id']
        payload = {
            'user_id': user_id,
            'exp': datetime.now(timezone.utc) + timedelta(days=1)
        }
        token = jwt.encode(payload, current_app.config['JWT_SECRET_KEY'], algorithm='HS256')
        return jsonify({'user_id': user_id, 'access_token': token})
    else:
        return jsonify({'message': 'Invalid email or password'}), 401

@auth_bp.route("/register", methods=["POST"])
def register():
    new_user = request.json
    new_user['password'] = bcrypt.hashpw(
        new_user['password'].encode('utf-8'),
        bcrypt.gensalt()
    ).decode('utf-8')

    try:
        with current_app.database.connect() as conn:
            new_user_id = conn.execute(text(
                """
                INSERT INTO users (
                    name,
                    email,
                    profile,
                    password
                ) VALUES (
                    :name,
                    :email,
                    :profile,
                    :password
                )
                """
            ), new_user).lastrowid

            conn.commit()

            row = conn.execute(text(
                """
                SELECT id, name, email, profile
                FROM users
                WHERE id = :user_id
                """
            ), {'user_id': new_user_id}).mappings().first()

            return jsonify({
                'id': row['id'],
                'name': row['name'],
                'email': row['email'],
                'profile': row['profile']
            })

    except IntegrityError:
        return jsonify({'message': 'This email is already registered.'}), 409


# 이메일 중복 확인 엔드포인트
@auth_bp.route("/check-email", methods=['GET'])
def check_email():
  email = request.args.get("email")
  if not email:
    return jsonify({"message": "Missing email parameter."}), 400

  with current_app.database.connect() as conn:
    result = conn.execute(text(
      "SELECT id FROM users WHERE email = :email"
    ), {"email": email}).fetchone()

    if result:
      return jsonify({"exists": True})
    else:
      return jsonify({"exists": False})


#############################
# DECORATORS
#############################

def login_required(f):
  @wraps(f)
  def decorated_function(*args, **kwargs):
    access_token = request.headers.get('Authorization')
    if access_token is not None:
      try:
        payload = jwt.decode(
            access_token,
            current_app.config['JWT_SECRET_KEY'],
            algorithms=["HS256"]
        )
      except jwt.InvalidTokenError:
        payload = None

      if payload is None:
        return Response(status=401)

      user_id = payload['user_id']
      g.user_id = user_id
      g.user = services.get_user(user_id) if user_id else None
    else:
      return Response(status=401)

    return f(*args, **kwargs)
  return decorated_function