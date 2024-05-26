from flask import Flask, jsonify, make_response, request
from .supabase import create_supabase_client
from .models import User

app = Flask(__name__)
supabase = create_supabase_client()

@app.route("/api/test", methods=["GET"])
def test():
    return jsonify({"message": "Server is Running"})

@app.route("/api/flask/users", methods=["POST"])
def create_user():
    try:
        data = request.get_json()
        supabase.from_("users")\
        .insert({
            "username": data['username'].lower(),
            "password": data['password'],
            "firstname": data['firstname'],
            "lastname": data['lastname'],
            "birthday": data['birthday']
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
            'birthday': data['birthday'],
        }, 201)
    
    except Exception as e:
        return make_response(jsonify({'message': 'Unable to POST user', 'error': str(e)}), 500)

@app.route("/api/flask/users", methods=["GET"])
def get_users():
    try:
        users = supabase.from_("users")\
        .select("id, username, firstname, lastname, birthday")\
        .order(column="id", desc=False)\
        .execute().data

        return jsonify(users), 200

    except Exception as e:
        return make_response(jsonify({"message": "Unable to GET user","error": str(e)}), 500)

@app.route("/api/flask/users/<id>", methods=["GET"])
def get_user(id):
    try:
        user = supabase.from_("users")\
        .select("*")\
        .eq(column="id", value=id)\
        .limit(size=1)\
        .execute().data[0]

        if user:
            return make_response(jsonify({"user": user.json()}), 200)

        return make_response(jsonify({"message": "User not found"}), 400)

    except Exception as e:
        return make_response(jsonify({"message": "Unable to GET user","error": str(e)}), 500)
    
@app.route("/api/flask/users/<id>", methods=["PUT"])
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
                'lastname': data['lastname'],
                'birthday': data['birthday'],
            })\
            .eq(column='id', value=id)\
            .execute()

            return make_response(jsonify({"message": "User UPDATED"}), 200)

        else:
            return make_response(jsonify({"message": f"Unable to Find User wiht id: {id}"}), 404)

    except Exception as e:
        return make_response(jsonify({"message": "Unable to UPDATE user","error": str(e)}), 500)
    
@app.route("/api/flask/users/<id>", methods=["DELETE"])
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