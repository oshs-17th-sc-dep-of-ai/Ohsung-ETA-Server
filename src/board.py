from quart import Quart, request, jsonify
from util.database import Database

app = Quart(__name__)
db = Database('database.db')
db.create_table()

@app.route('/board/<int:board_id>/<int:post_id>', methods=['GET', 'PATCH', 'DELETE'])
async def post_details(board_id, post_id):
    if request.method == 'GET':
        post = db.get_post_by_id(board_id, post_id)
        if post:
            return jsonify(post), 200
        else:
            return jsonify({"error": "Post not found"}), 404
    elif request.method == 'PATCH':
        data = request.json
        title = data.get('title')
        content = data.get('content')
        if title and content:
            success = db.update_post(post_id, title, content)
            if success:
                return jsonify({"message": "Post updated successfully"}), 200
            else:
                return jsonify({"error": "Post not found"}), 404
        else:
            return jsonify({"error": "Title and content are required for updating"}), 400
    elif request.method == 'DELETE':
        success = db.delete_post(post_id)
        if success:
            return jsonify({"message": "Post deleted successfully"}), 200
        else:
            return jsonify({"error": "Post not found"}), 404

@app.route('/board/<int:board_id>/write_post', methods=['POST'])
async def write_post(board_id):
    '''
    새 글 작성
    '''
    data = await request.json
    user_id = data.get('user_id')
    title = data.get('title')
    content = data.get('content')
    if user_id and title and content:
        db.write_post(board_id, user_id, title, content)
        return jsonify({"message": "Post created successfully"}), 201
    else:
        return jsonify({"error": "User ID, title, and content are required"}), 400

@app.route('/board/<int:board_id>/like_post/<int:post_id>', methods=['POST'])
def like_post(board_id, post_id):
    '''
    post_id 추천 수 증가
    '''
    post = db.get_post_by_id(board_id, post_id)
    if post:
        db.like_post(post_id)
        return jsonify({"message": "Post liked successfully"}), 200
    else:
        return jsonify({"error": "Post not found"}), 404

@app.route('/board/<int:board_id>/dislike_post/<int:post_id>', methods=['POST'])
def dislike_post(board_id, post_id):
    '''
    post_id 추천 수 감소
    '''
    post = db.get_post_by_id(board_id, post_id)
    if post:
        db.dislike_post(post_id)
        return jsonify({"message": "Post disliked successfully"}), 200
    else:
        return jsonify({"error": "Post not found"}), 404

@app.route('/board/<int:board_id>/popular_posts', methods=['GET'])
def get_popular_posts(board_id):
    '''
    인기 글 반환
    '''
    popular_posts = db.get_popular_posts(board_id)
    return jsonify(popular_posts), 200