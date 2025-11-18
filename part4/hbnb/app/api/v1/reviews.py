from flask_restx import Namespace, Resource, fields
from app.services import facade
from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt_identity

api = Namespace('reviews', description='Review operations')

# Define the review model for input validation and documentation
review_model = api.model('Review', {
    'text': fields.String(required=True, description='Text of the review'),
    'rating': fields.Integer(required=True, description='Rating of the place (1-5)'),
    'user_id': fields.String(required=True, description='ID of the user'),
    'place_id': fields.String(required=True, description='ID of the place')
})

@api.route('/')
class ReviewList(Resource):
    @api.expect(review_model)
    @api.response(201, 'Review successfully created')
    @api.response(400, 'Invalid input data')
    @jwt_required()
    def post(self):
        """Register a new review"""
        current_user = get_jwt_identity()
        try:
            review_data = api.payload
            if not review_data.get('user_id'):
                return {"error": "user id must not be empty"}, 400
            if not review_data.get('place_id'):
                return {"error": "place id must not be empty"}, 400
            review_place = facade.get_place(review_data.get('place_id'))
            if not review_place:
                return {"error": "place doesn't exist"}, 403
            
            if str(review_place.owner_id) == str(current_user):
                return {'error': 'You cannot review your own place.'}, 400
            if facade.compare_review(current_user, review_data['place_id']):
                return {'error': 'You have already reviewed this place.'}, 400
            
            new_review = facade.create_review(review_data)
            

            return {
                'id': new_review.id, 
                'text': new_review.text, 
                'rating': new_review.rating,
                'user_id': new_review.user_id,
                'place_id': new_review.place_id,
            }, 201
        except ValueError as e:
            return {"error": str(e)}, 400


    @api.response(200, 'List of reviews retrieved successfully')
    def get(self):
        """Retrieve a list of all reviews"""
        try:
            all_review = facade.get_all_reviews()
            reviews = [{
                "id": r.id,
                "text": r.text,
                "rating": r.rating
            } for r in all_review]
            return reviews, 200
        except Exception as e:
            return {"error": f"Review not found: {str(e)}"}, 404

@api.route('/<review_id>')
class ReviewResource(Resource):
    @api.response(200, 'Review details retrieved successfully')
    @api.response(404, 'Review not found')
    def get(self, review_id):
        """Get review details by ID"""
        try:
            review = facade.get_review(review_id)
            return {
                "id": review.id,
                "text": review.text,
                "rating": review.rating,
                "user_id": review.user_id,
                "place_id": review.place_id
            }, 200
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
            review_data = api.payload
            #if review_put.owner_id != current_user:
                #return {'error': 'Unauthorized action'}, 403

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
            review = facade.get_review(review_id)
            review_del = facade.get_review(review_id)
            if not review:
                return {"error": "review does not exist."}, 404
            
        except Exception as e:
            return {"error": f"Not Found: {str(e)}"}, 404
        facade.delete_review(review_id)
        return {"message": "Review deleted successfully"}, 200

@api.route('/places/<place_id>/reviews')
class PlaceReviewList(Resource):
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
            return {"error": f"Review not found: {str(e)}"}, 404
