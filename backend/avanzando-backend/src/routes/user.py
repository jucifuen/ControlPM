from flask import Blueprint, jsonify, request
from src.models.user import User, db, UserRole
from src.middleware.auth import token_required, admin_required

user_bp = Blueprint("user", __name__)

@user_bp.route("/users", methods=["GET"])
@token_required
def get_users(current_user):
    users = User.query.all()
    return jsonify([user.to_dict() for user in users])

@user_bp.route("/users", methods=["POST"])
@token_required
@admin_required
def create_user(current_user):
    data = request.json
    
    # Crear usuario cliente por defecto
    user = User(
        nombre=data["nombre"], 
        email=data.get("email", f'{data["nombre"].lower().replace(" ", ".")}@cliente.com'),
        rol=UserRole.RECURSO
    )
    user.set_password("defaultpassword123")  # Password por defecto para clientes
    db.session.add(user)
    db.session.commit()
    return jsonify({"user": user.to_dict()}), 201

@user_bp.route("/users/<int:user_id>", methods=["GET"])
@token_required
def get_user(current_user, user_id):
    user = User.query.get_or_404(user_id)
    return jsonify(user.to_dict())

@user_bp.route("/users/<int:user_id>", methods=["PUT"])
@token_required
@admin_required
def update_user(current_user, user_id):
    user = User.query.get_or_404(user_id)
    data = request.json
    user.nombre = data.get("nombre", user.nombre)
    user.email = data.get("email", user.email)
    db.session.commit()
    return jsonify(user.to_dict())

@user_bp.route("/users/<int:user_id>", methods=["DELETE"])
@token_required
@admin_required
def delete_user(current_user, user_id):
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    return "", 204
