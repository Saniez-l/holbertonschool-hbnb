from flask_restx import Namespace, Resource, fields
from app.services import facade
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_cors import cross_origin

api = Namespace('reviews', description='Review operations')


review_model = api.model('Review', {
    'id': fields.String(description='The review unique identifier'),
    'text': fields.String(required=True, description='Text of the review'),
    'rating': fields.Integer(required=True, description='Rating of the place (1-5)'),
    'user_id': fields.String(required=True, description='ID of the user who wrote the review'),
    'place_id': fields.String(required=True, description='ID of the place being reviewed')
})

review_input_model = api.model('ReviewInput', {
    'text': fields.String(required=True, description='Text of the review'),
    'rating': fields.Integer(required=True, description='Rating of the place (1-5)'),
})


@api.route('/<review_id>')
class ReviewResource(Resource):
    """Resource pour une review spécifique (GET, PUT, DELETE)"""
    
    def options(self, review_id):
        """Handle preflight CORS request"""
        return {}, 200
    
    @api.marshal_with(review_model)
    @api.response(200, 'Review details retrieved successfully')
    @api.response(404, 'Review not found')
    def get(self, review_id):
        """Get review details by ID"""
        try:
            review = facade.get_review(review_id)
            if not review:
                api.abort(404, "Review not found")
            
            return review, 200
        except Exception as e:
            return {"error": f"Review not found: {str(e)}"}, 404

    @api.expect(review_model)
    @api.response(200, 'Review updated successfully')
    @api.response(404, 'Review not found')
    @api.response(400, 'Invalid input data')
    @jwt_required()
    def put(self, review_id):
        """Update a review's information"""
        current_user = get_jwt_identity()
        try:
            review_put = facade.get_review(review_id)
            if not review_put:
                api.abort(404, "Review not found")
                
            review_data = api.payload
            
            review_put.text = review_data.get('text', review_put.text)
            review_put.rating = review_data.get('rating', review_put.rating)
            review_put.user_id = review_data.get('user_id', review_put.user_id)
            review_put.place_id = review_data.get('place_id', review_put.place_id)
            
            
            return {"message": "Review updated successfully"}, 200

        except Exception as e:
            return {"error": f"Review not found: {str(e)}"}, 404

    @api.response(200, 'Review deleted successfully')
    @api.response(404, 'Review not found')
    @jwt_required()
    def delete(self, review_id):
        """Delete a review"""
        current_user = get_jwt_identity()
        try:
            review_del = facade.get_review(review_id)
            if not review_del:
                api.abort(404, "review does not exist.")
            
            facade.delete_review(review_id)
            return {"message": "Review deleted successfully"}, 200
            
        except Exception as e:
            return {"error": f"Not Found: {str(e)}"}, 404


@api.route('/<place_id>/reviews', strict_slashes=False)
class PlaceReviewList(Resource):
    """Resource pour la création (POST) et la liste (GET) des reviews d'une place"""
    
    def options(self, place_id):
        """Handle preflight CORS request"""
        return {}, 200
    
    @api.expect(review_input_model)
    @api.response(201, 'Review successfully created', review_model) 
    @api.response(400, 'Invalid input data')
    @jwt_required()
    def post(self, place_id): 
        """Register a new review for a specific place"""
        current_user_id = get_jwt_identity()
        
        try:
            review_data = dict(api.payload) 
        
            review_data['user_id'] = current_user_id
            review_data['place_id'] = place_id
            
            review_place = facade.get_place(place_id)
            if not review_place:
                return {"error": "Place doesn't exist"}, 404
            
            if str(review_place.owner_id) == str(current_user_id):
                return {'error': 'You cannot review your own place.'}, 400
            
            if facade.compare_review(current_user_id, place_id):
                return {'error': 'You have already reviewed this place.'}, 400
            
            new_review = facade.create_review(review_data)
            return {"text": new_review.text, "rating": new_review.rating}, 201 
            
        except ValueError as e:
            return {"error": str(e)}, 400
        except Exception as e:
             return {"error": f"Internal server error: {str(e)}"}, 500

    @api.response(200, 'List of reviews for the place retrieved successfully')
    @api.response(404, 'Place not found')
    def get(self, place_id):
        """Get all reviews for a specific place"""
        try:
            place = facade.get_place(place_id)
            if not place:
                return {"error": "Place not found"}, 404
            
            review = facade.get_reviews_by_place(place_id)
            reviews = [{
                "id": r.id,
                "text": r.text,
                "rating": r.rating
            } for r in review]
            return reviews, 200
        except Exception as e:
            return {"error": f"Review listing error: {str(e)}"}, 404