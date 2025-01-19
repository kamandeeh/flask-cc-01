from flask import jsonify, request, Blueprint
from models import User, db

user_bp = Blueprint("user_bp", __name__)

@user_bp.route("/users")
def fetch_users():
    users = User.query.all()
    user_list = []
    for user in users:
        user_list.append({
            'id': user.id,
            'email': user.email,
            'username': user.username,
            "password": user.password
        })
    return jsonify(user_list), 200

@user_bp.route("/users", methods=['POST'])
def add_users():
    data = request.get_json()
    username = data["username"]
    email = data["email"]
    password = data["password"]

    check_username = User.query.filter_by(username=username).first()
    check_email = User.query.filter_by(email=email).first()

    if check_username or check_email:
        return jsonify({"error": "Username/Email exists"}), 406
    else:
        new_user = User(username=username, email=email, password=password)
        db.session.add(new_user)
        db.session.commit()
        return jsonify({"Success": "Added successfully"}), 201


@user_bp.route("/users/<int:user_id>", methods=['PATCH'])
def update_user(user_id):
    user = User.query.get(user_id)

    if user:
        data = request.get_json()
        username = data.get("username",user.username)
        email = data.get("email",user.email)
        password = data.get("password",user.password)

        # Fix the condition for checking username and email
        check_username = User.query.filter(User.username == username, User.id != user.id).first()
        check_email = User.query.filter(User.email == email, User.id != user.id).first()

        if check_username or check_email:
            return jsonify({"error": "Username/Email exists"}), 406
        else:
            user.username = username
            user.email = email
            user.password = password

            db.session.commit()
            return jsonify({"Success": "Updated successfully"}), 200

    return jsonify({"error": "User doesn't exist!"}), 404


@user_bp.route("/users/<int:user_id>", methods=['DELETE'])
def delete_user(user_id):
    user = User.query.get(user_id)

    if user:
        db.session.delete(user)
        db.session.commit()
        return jsonify({"success": "Deleted successfully"}), 200

    else:
        return jsonify({"error": "User being deleted doesn't exist"}), 404
