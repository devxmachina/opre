from flask import Blueprint, request, jsonify, current_app
from sqlalchemy import text
from ..services import services
from .auth import login_required

recipe_bp = Blueprint('recipes', __name__)

# 레시피 등록 엔드포인트
@recipe_bp.route("/recipes", methods=['POST'])
def create_recipe():
  user_recipe = request.json
  title = user_recipe['title']
  description = user_recipe['description']

  if len(description) > 800:
    return '800 characters or less please.', 400

  with recipe_bp.database.connect() as conn:
    conn.execute(text(
      """
        INSERT INTO tweets (
          user_id,
          tweet
        ) VALUES (
          :id,
          :tweet
        )
      """
    ), user_recipe)

    conn.commit()
    return '', 200


#  레시피 타임라인 엔드포인트
@recipe_bp.route("/timeline", methods=['GET'])
def timeline():
  with recipe_bp.database.connect() as conn:
    rows = conn.execute(text(
      """
        SELECT * FROM recipes
      """
    )).mappings().fetchall()

  timeline = [{
    'user_id': row['user_id'],
    'title': row['title']
  } for row in rows]

  return jsonify(timeline)


# 유저 타임라인
@recipe_bp.route("/recipes/<int:user_id>", methods=['GET'])
def user_timeline(user_id):
  with recipe_bp.database.connect() as conn:
    rows = conn.execute(text(
      """
        SELECT
          r.user_id,
          r.title
        FROM recipes r
        LEFT JOIN users_follow_list ufl ON ufl.user_id = :user_id
        WHERE r.user_id = :user_id
        OR r.user_id = ufl.follow_user_id
      """
    ), {'user_id': user_id}).mappings().fetchall()

    timeline = [{
      'user_id': row['user_id'],
      'title' : row['title']
    } for row in rows]

    return jsonify({
      'timeline' : timeline,
      'user_id': user_id
    })
