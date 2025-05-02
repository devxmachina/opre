from flask import current_app
from sqlalchemy import text

def get_user(user_id):
  with current_app.database.connect() as conn:
    user = conn.execute(text(
      """
        SELECT
          id,
          name,
          email,
          profile
        FROM users
        WHERE id = :user_id
      """
    ), {
      'user_id': user_id
    }).mappings().fetchall()

    return {
      'id'      : user['id'],
      'name'    : user['name'],
      'email'   : user['email'],
      'profile' : user['profile']
    } if user else None


def get_user_id_and_password(email):
    with current_app.database.connect() as conn:
        row = conn.execute(text(
            """
            SELECT id, password
            FROM users
            WHERE email = :email
            """
        ), {'email': email}).mappings().fetchone()
        return {'id': row['id'], 'hashed_password': row['password']} if row else None


def print_all_users():
  with current_app.database.connect() as conn:
    rows = conn.execute(text(
      """
        SELECT *
        FROM users
      """
    )).mappings().fetchall()
    print('### rows ->', rows)

    all_users = []

    for row in rows:
      user_info = {
        'id'      : row['id'],
        'name'    : row['name'],
        'email'   : row['email'],
        'profile' : row['profile']
      }
      all_users.append(user_info)
    
    return all_users if rows else None


def insert_user(user):
  return current_app.database.execute(text(
    """
      INSERT INTO users (
        name,
        email,
        profile,
        hashed_password
      ) VALUES (
        :name,
        :email,
        :profile,
        :password
      )
    """
  ), user).lastrowid

def insert_recipe(user_recipe):
  return current_app.database.execute(text(
    """
      INSERT INTO recipes (
        user_id,
        title
        description
      ) VALUES (
        :id,
        :title
        :description
      )
    """
  ), user_recipe).rowcount

def insert_follow(user_follow):
  return current_app.database.execute(text(
    """
      INSERT INTO tweets (
        user_id,
        follow_user_id
      ) VALUES (
        :id,
        :follow
      )
    """
  ), user_follow).rowcount

  
def insert_unfollow(user_unfollow):
  return current_app.database.execute(text(
    """
      DELETE FROM users_follow_list
      WHERE user_id = :id
      AND follow_user_id = :unfollow
    """
  ), user_unfollow).rowcount


def get_timeline(user_id):
  timeline = current_app.database.execute(text(
    """
      SELECT
        t.user_id,
        t.tweet
      FROM tweets t
      LEFT JOIN user_follow_list ufl ON ufl.user_id = :user_id
      WHERE t.user_id = :user_id
      OR t.user_id = ufl.follow_user_id
    """
  ), {'user_id': user_id}).fetchall()

  return [{
    'user_id' : tweet['user_id'],
    'tweet'   : tweet['tweet']
  } for tweet in timeline]

def get_user_id_and_password(email):
  with current_app.database.connect() as conn:
    row = conn.execute(text(
      """
        SELECT
          id,
          password
        FROM users
        WHERE email = :email
      """
    ), {'email': email}).mappings().fetchone()

    return {
      'id': row['id'],
      'hashed_password': row['password']
    } if row else None