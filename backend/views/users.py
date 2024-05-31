from flask import Flask, jsonify, make_response, request, Blueprint
from ..database import supabase

users = Blueprint('users', __name__, url_prefix='/users')

# ---------- GET ----------

# Gets all users
@users.route("/api/flask", methods=["GET"])
def get_users():
    try:
        users = supabase.from_("users")\
        .select("id, username, firstname, lastname")\
        .order(column="id", desc=False)\
        .execute().data

        return jsonify(users), 200

    except Exception as e:
        return make_response(jsonify({"message": "Unable to GET user","error": str(e)}), 500)

# Gets user via id
@users.route("/api/flask/<id>", methods=["GET"])
def get_user(id):
    try:
        user = supabase.from_("users")\
        .select("*")\
        .eq(column="id", value=id)\
        .limit(size=1)\
        .execute().data[0]

        if user:
            return make_response(jsonify(user), 200)

        return make_response(jsonify({"message": "User not found"}), 400)

    except Exception as e:
        return make_response(jsonify({"message": "Unable to GET user","error": str(e)}), 500)
    
# Gets user via username and password
@users.route("/api/flask/credentials", methods=["GET"])
def get_user_credentials():
    try:
        data = request.get_json()
        user = supabase.from_("users")\
        .select("id")\
        .eq(column="username", value=data['username'].lower())\
        .eq(column="password", value=data['password'])\
        .limit(size=1)\
        .execute().data[0]
        
        if user:
            return make_response(jsonify(user), 200)

        return make_response(jsonify({"message": "User not found"}), 400)

    except Exception as e:
        return make_response(jsonify({"message": "Unable to GET user","error": str(e)}), 500)    

# ---------- POST ----------
@users.route("/api/flask", methods=["POST"])
def create_user():
    try:
        data = request.get_json()
        supabase.from_("users")\
        .insert({
            "username": data['username'].lower(),
            "password": data['password'],
            "firstname": data['firstname'],
            "lastname": data['lastname'],
        })\
        .execute()

        user_id = supabase.from_("users")\
            .select("id")\
            .limit(size=1)\
            .order(column="id", desc=True)\
            .execute().data[0]
        
        return jsonify({
            'id': user_id['id'],
            'username': data['username'],
            'firstname': data['firstname'],
            'lastname': data['lastname'],
        }, 201)
    
    except Exception as e:
        return make_response(jsonify({'message': 'Unable to POST user', 'error': str(e)}), 500)

# ---------- PUT ----------
@users.route("/api/flask/<id>", methods=["PUT"])
def update_user(id):
    try:
        user = supabase.from_("users")\
        .select("*")\
        .eq(column="id", value=id)\
        .limit(size=1)\
        .execute().data

        if user:
            data = request.get_json()
            supabase.from_("users")\
            .update({
                "username": data['username'].lower(),
                'password': data['password'],
                'firstname': data['firstname'],
                'lastname': data['lastname']
            })\
            .eq(column='id', value=id)\
            .execute()

            return make_response(jsonify({"message": "User UPDATED"}), 200)

        else:
            return make_response(jsonify({"message": f"Unable to Find User wiht id: {id}"}), 404)

    except Exception as e:
        return make_response(jsonify({"message": "Unable to UPDATE user","error": str(e)}), 500)
    
# ---------- DELETE ----------
@users.route("/api/flask/<id>", methods=["DELETE"])
def delete_user(id):
    try:
        user = supabase.from_("users")\
        .select("*")\
        .eq(column="id", value=id)\
        .limit(size=1)\
        .execute().data

        if user:
            supabase.from_("users")\
            .delete()\
            .eq(column='id', value=id)\
            .execute()

            return make_response(jsonify({"message": "User DELETED"}), 200)

        else:
            return make_response(jsonify({"message": f"Unable to Find User with id: {id}"}), 404)

    except Exception as e:
        return make_response(jsonify({"message": "Unable to DELETED user","error": str(e)}), 500)