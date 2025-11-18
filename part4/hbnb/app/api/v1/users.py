from flask_jwt_extended import jwt_required, get_jwt
from flask_restx import Namespace, Resource, fields
from app.services import facade

api = Namespace('users', description='User operations')
api = Namespace('admin', description='Admin operations')

# Define the user model for input validation and documentation
user_model = api.model('User', {
    'first_name': fields.String(required=True, description='First name of the user'),
    'last_name': fields.String(required=True, description='Last name of the user'),
    'email': fields.String(required=True, description='Email of the user'),
    'password': fields.String(required=True, description='Password of the user'),
    'is_admin': fields.Boolean(required=True, description='Permission level of the user')
})

@api.route('/')
class UserCreate(Resource):
    @api.expect(user_model, validate=True)
    @api.response(201, 'User successfully created')
    @api.response(400, 'Email already registered')
    @api.response(400, 'Invalid input data')
    def post(self):
        """Register a new user"""
        user_data = api.payload
        email = user_data.get('email')

        # Check if email is already in use
        if facade.get_user_by_email(email):
            return {'error': 'Email already registered'}, 400

        try:
            new_user = facade.create_user(user_data)
        except Exception as e:
            return {'error': str(e)}, 400

        return {'id': new_user.id, 'first_name': new_user.first_name, 'last_name': new_user.last_name, 'email': new_user.email}, 201

    @api.response(200, 'list of user')
    @api.response(500, 'Internal server error')
    def get(self):
        """
        retrieves all users
        """
        try:
            user_all = facade.all_users()
            user_list = []
            for user in user_all:
                user_list.append({
                'id': user.id,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'email': user.email
                })
            return user_list, 200
        except Exception as e:
            return {"error": f"error user list: {str(e)}"}, 500

@api.route('/admin')
class AdminUserCreate(Resource):
    """Class and endpoint used to create as Admin
    As opposed to regular / from where users can be
    created by non-admin;

    This is to test our endpoints more easily
    """
    @api.expect(user_model, validate=True)
    @api.response(201, 'User successfully created')
    @api.response(400, 'Email already registered')
    @api.response(400, 'Invalid input data')
    @jwt_required()
    def post(self):
        current_user = get_jwt()
        if not current_user.get('is_admin'):
           return {'error': 'Admin privileges required'}, 403

        user_data = api.payload
        email = user_data.get('email')

        # Check if email is already in use
        if facade.get_user_by_email(email):
            return {'error': 'Email already registered'}, 400

        try:
            new_user = facade.create_user(user_data)
        except Exception as e:
            return {'error': str(e)}, 400

        return {'id': new_user.id, 'first_name': new_user.first_name, 'last_name': new_user.last_name, 'email': new_user.email}, 201

@api.route('/<user_id>')
class AdminUserResource(Resource):
    @api.response(200, 'User details retrieved successfully')
    @api.response(404, 'User not found')
    def get(self, user_id):
        """Get user details by ID"""
        user = facade.get_user(user_id)
        if not user:
            return {'error': 'User not found'}, 404
        return {'id': user.id, 'first_name': user.first_name, 'last_name': user.last_name, 'email': user.email}, 200
    
    @api.expect(user_model)
    @api.response(200, 'User details retrieved successfully')
    @api.response(404, 'User not found')
    @jwt_required()
    def put(self, user_id):
        """update user after verifying autorisations"""
        current_user = get_jwt()
        
        # If 'is_admin' is part of the identity payload
        is_admin = current_user.get('is_admin', False)
        is_owner = current_user.get('id') == user_id
        
        if not (is_admin or is_owner):
            return {'error': 'Unauthorised action'}, 403

        user_put = facade.get_user(user_id)
        if not user_put:
            return {'error': 'User not found'}, 404
        
        user_data = api.payload

        try:
            facade.update_user(user_id, user_data)

        except:
            return {'error': 'invalid input data'}, 400
        
        return {'id': user_put.id, 'first_name': user_put.first_name, 'last_name': user_put.last_name, 'email': user_put.email}, 200
