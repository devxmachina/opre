# from functools import wraps
# from flask import Flask, jsonify, request, current_app, Response, g
# # from flask.json import JSONEncoder
# from sqlalchemy import create_engine, text
# from sqlalchemy.exc import IntegrityError
# from config import DB_URL
# import bcrypt
# from flask_cors import CORS

# import jwt
# from jwt.exceptions import InvalidTokenError, ExpiredSignatureError
# from datetime import datetime, timedelta, timezone


# def get_user(user_id):
#   with current_app.database.connect() as conn:
#     user = conn.execute(text(
#       """
#         SELECT
#           id,
#           name,
#           email,
#           profile
#         FROM users
#         WHERE id = :user_id
#       """
#     ), {
#       'user_id': user_id
#     }).mappings().fetchall()

#     return {
#       'id'      : user['id'],
#       'name'    : user['name'],
#       'email'   : user['email'],
#       'profile' : user['profile']
#     } if user else None


# def print_all_users():
#   with current_app.database.connect() as conn:
#     rows = conn.execute(text(
#       """
#         SELECT *
#         FROM users
#       """
#     )).mappings().fetchall()
#     print('### rows ->', rows)

#     all_users = []

#     for row in rows:
#       user_info = {
#         'id'      : row['id'],
#         'name'    : row['name'],
#         'email'   : row['email'],
#         'profile' : row['profile']
#       }
#       all_users.append(user_info)
    
#     return all_users if rows else None


# def insert_user(user):
#   return current_app.database.execute(text(
#     """
#       INSERT INTO users (
#         name,
#         email,
#         profile,
#         hashed_password
#       ) VALUES (
#         :name,
#         :email,
#         :profile,
#         :password
#       )
#     """
#   ), user).lastrowid

# def insert_recipe(user_recipe):
#   return current_app.database.execute(text(
#     """
#       INSERT INTO recipes (
#         user_id,
#         title
#         description
#       ) VALUES (
#         :id,
#         :title
#         :description
#       )
#     """
#   ), user_recipe).rowcount

# def insert_follow(user_follow):
#   return current_app.database.execute(text(
#     """
#       INSERT INTO tweets (
#         user_id,
#         follow_user_id
#       ) VALUES (
#         :id,
#         :follow
#       )
#     """
#   ), user_follow).rowcount

  
# def insert_unfollow(user_unfollow):
#   return current_app.database.execute(text(
#     """
#       DELETE FROM users_follow_list
#       WHERE user_id = :id
#       AND follow_user_id = :unfollow
#     """
#   ), user_unfollow).rowcount


# def get_timeline(user_id):
#   timeline = current_app.database.execute(text(
#     """
#       SELECT
#         t.user_id,
#         t.tweet
#       FROM tweets t
#       LEFT JOIN user_follow_list ufl ON ufl.user_id = :user_id
#       WHERE t.user_id = :user_id
#       OR t.user_id = ufl.follow_user_id
#     """
#   ), {'user_id': user_id}).fetchall()

#   return [{
#     'user_id' : tweet['user_id'],
#     'tweet'   : tweet['tweet']
#   } for tweet in timeline]

# # def get_user_id_and_password(email):
# #   with current_app.database.connect() as conn:
# #     row = conn.execute(text(
# #       """
# #         SELECT
# #           id,
# #           password
# #         FROM users
# #         WHERE email = :email
# #       """
# #     ), {'email': email}).mappings().fetchone()

# #     return {
# #       'id': row['id'],
# #       'hashed_password': row['password']
# #     } if row else None

#############################
# DECORATORS
#############################

# def login_required(f):
#   @wraps(f)
#   def decorated_function(*args, **kwargs):
#     access_token = request.headers.get('Authorization')
#     if access_token is not None:
#       try:
#         payload = jwt.decode(
#             access_token,
#             current_app.config['JWT_SECRET_KEY'],
#             algorithms=["HS256"]
#         )
#       except InvalidTokenError:
#         payload = None

#       if payload is None:
#         return Response(status=401)

#       user_id = payload['user_id']
#       g.user_id = user_id
#       g.user = get_user(user_id) if user_id else None
#     else:
#       return Response(status=401)

#     return f(*args, **kwargs)
#   return decorated_function

############################################################################
############################################################################
############################################################################
############################################################################
############################################################################

# def create_app(test_config=None):
#   app = Flask(__name__)
#   CORS(app, supports_credentials=True, resources={r"/*": {"origins": "http://localhost:5173"}})
#   # CORS(app, resources={r"/*": {"origins": "*"}})
#   # app.json_encoder = CustomJSONEncoder
#   if test_config is None:
#     app.config.from_pyfile("config.py")
#   else:
#     app.config.update(test_config)

#   database = create_engine(app.config['DB_URL'], max_overflow=0, echo=True)
#   app.database = database

############################################################################
############################################################################
############################################################################
############################################################################
############################################################################

  # @app.route("/ping", methods=['GET'])
  # def ping():
  #   return 'pooooong'

  
  # @app.route("/", methods=['GET'])
  # @login_required
  # def home():
  #   with app.database.connect() as conn:
  #     results = conn.execute(text("""SELECT * FROM users""")).mappings()
  #     # columns = result.keys()  # 열 이름을 얻음te
  #     # all_users = [dict(zip(columns, row)) for row in result.fetchall()]
  #     all_users = [dict(row) for row in results]
    
  #     return jsonify(all_users)


  # # 회원가입 엔드포인트
  # @app.route("/register", methods=['POST'])
  # def register():
  #   new_user = request.json
  #   new_user['password'] = bcrypt.hashpw(
  #     new_user['password'].encode('UTF-8'),
  #     bcrypt.gensalt()
  #   ).decode('UTF-8')
  #   try:
  #     with app.database.connect() as conn:
  #       new_user_id = conn.execute(text(
  #         """
  #           INSERT INTO users (
  #             name,
  #             email,
  #             profile,
  #             password
  #           ) VALUES (
  #             :name,
  #             :email,
  #             :profile,
  #             :password
  #           )
  #         """
  #       ), new_user).lastrowid

  #       conn.commit()

  #       row = conn.execute(text(
  #         """
  #           SELECT id, name, email, profile
  #           FROM users
  #           WHERE id = :user_id
  #         """
  #       ), {'user_id': new_user_id}).mappings().first()

  #       return jsonify({
  #           'id': row['id'],
  #           'name': row['name'],
  #           'email': row['email'],
  #           'profile': row['profile']
  #       })
  #   except IntegrityError:
  #     return jsonify({'message': 'This email is already registered.'}), 409

  # 이메일 중복 확인 엔드포인트
  # @app.route("/check-email", methods=['GET'])
  # def check_email():
  #   email = request.args.get("email")
  #   if not email:
  #     return jsonify({"message": "Missing email parameter."}), 400

  #   with app.database.connect() as conn:
  #     result = conn.execute(text(
  #       "SELECT id FROM users WHERE email = :email"
  #     ), {"email": email}).fetchone()

  #     if result:
  #       return jsonify({"exists": True})
  #     else:
  #       return jsonify({"exists": False})
    
  # @app.route('/login', methods=['POST', 'GET'])
  # def login():
  #   credential = request.json
  #   email = credential['email']
  #   password = credential['password']

  #   user_credential = get_user_id_and_password(email)

  #   # 존재하지 않거나 비밀번호 해시가 없는 경우
  #   if not user_credential or not user_credential['hashed_password']:
  #     return jsonify({'message': 'Invalid email or password'}), 401

  #   # 비밀번호 검증 디버깅용 출력
  #   print("LOGIN EMAIL:", email)
  #   print("RAW INPUT PASSWORD:", password)
  #   print("HASHED FROM DB:", user_credential['hashed_password'])
  #   try:
  #     result = bcrypt.checkpw(password.encode('UTF-8'), user_credential['hashed_password'].encode('UTF-8'))
  #     print("BCRYPT RESULT:", result)
  #   except Exception as e:
  #     print("BCRYPT ERROR:", str(e))
  #     return jsonify({'message': 'Bcrypt error: ' + str(e)}), 500

  #   if result:
  #     user_id = user_credential['id']
  #     payload = {
  #       'user_id': user_id,
  #       'exp': datetime.now(timezone.utc) + timedelta(seconds=60 * 60 * 24)
  #     }
  #     token = jwt.encode(payload, current_app.config['JWT_SECRET_KEY'], algorithm='HS256')
  #     return jsonify({
  #       'user_id': user_id,
  #       'access_token': token
  #     })
  #   else:
  #     return jsonify({'message': 'Invalid email or password'}), 401
  


#   # 레시피 등록 엔드포인트
#   @app.route("/recipes", methods=['POST'])
#   def create_recipe():
#     user_recipe = request.json
#     title = user_recipe['title']
#     description = user_recipe['description']

#     if len(description) > 800:
#       return '800 characters or less please.', 400

#     with app.database.connect() as conn:
#       conn.execute(text(
#         """
#           INSERT INTO tweets (
#             user_id,
#             tweet
#           ) VALUES (
#             :id,
#             :tweet
#           )
#         """
#       ), user_recipe)

#       conn.commit()
#       return '', 200


# #  레시피 타임라인 엔드포인트
#   @app.route("/timeline", methods=['GET'])
#   def timeline():
#     with app.database.connect() as conn:
#       rows = conn.execute(text(
#         """
#           SELECT * FROM recipes
#         """
#       )).mappings().fetchall()

#     timeline = [{
#       'user_id': row['user_id'],
#       'title': row['title']
#     } for row in rows]

#     return jsonify(timeline)


#   # 유저 타임라인
#   @app.route("/recipes/<int:user_id>", methods=['GET'])
#   def user_timeline(user_id):
#     with app.database.connect() as conn:
#       rows = conn.execute(text(
#         """
#           SELECT
#             r.user_id,
#             r.title
#           FROM recipes r
#           LEFT JOIN users_follow_list ufl ON ufl.user_id = :user_id
#           WHERE r.user_id = :user_id
#           OR r.user_id = ufl.follow_user_id
#         """
#       ), {'user_id': user_id}).mappings().fetchall()

#       timeline = [{
#         'user_id': row['user_id'],
#         'title' : row['title']
#       } for row in rows]

#       return jsonify({
#         'timeline' : timeline,
#         'user_id': user_id
#       })

from opre_be import create_app

app = create_app()

if __name__ == "__main__":
  app.run(debug=True)