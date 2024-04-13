from sanic import Sanic, response
from util.database import Database

app = Sanic(__name__)
db = Database('database.db')
db.create_table()

@app.route('/board/<int:board_id>/<int:post_id>', methods=['GET', 'PATCH', 'DELETE'])
async def post_details(request, board_id, post_id):
    if request.method == 'GET':
        post = db.get_post_by_id(board_id, post_id)
        if post:
            return response.json(post)
        else:
            return response.json({"error": "Post not found"}), 404
    elif request.method == 'PATCH':
        data = request.json
        title = data.get('title')
        content = data.get('content')
        if title and content:
            success = db.update_post(board_id, post_id, title, content)
            if success:
                return response.json({"message": "Post updated successfully"}, status=200)
            else:
                return response.json({"error": "Post not found"}, status=404)
        else:
            return response.json({"error": "Title and content are required for updating"}, status=400)
    elif request.method == 'DELETE':
        success = db.delete_post(board_id, post_id)
        if success:
            return response.json({"message": "Post deleted successfully"})
        else:
            return response.json({"error": "Post not found"}, status=404)

@app.route('/board/<int:board_id>/write_post', methods=['POST'])
async def write_post(request, board_id):
    '''
    새 글 작성
    '''
    data = request.json
    user_id = data.get('user_id')
    title = data.get('title')
    content = data.get('content')
    if user_id and title and content:
        db.write_post(board_id, user_id, title, content)
        return response.json({"message": "Post created successfully"}, status=201)
    else:
        return response.json({"error": "User ID, title, and content are required"}, status=400)

@app.route('/board/<int:board_id>/<int:post_id>/like', methods=['PUT'])
async def like_post(request, board_id, post_id):
    '''
    post_id 추천 수 증가
    '''
    post = db.get_post_by_id(board_id, post_id)
    if post:
        db.like_post(post_id)
        return response.json({"message": "Post liked successfully"})
    else:
        return response.json({"error": "Post not found"}, status=404)

@app.route('/board/<int:board_id>/<int:post_id>/dislike', methods=['PATCH'])
async def dislike_post(request, board_id, post_id):
    '''
    post_id 추천 수 감소
    '''
    post = db.get_post_by_id(board_id, post_id)
    if post:
        db.dislike_post(post_id)
        return response.json({"message": "Post disliked successfully"})
    else:
        return response.json({"error": "Post not found"}, status=404)

@app.route('/board/<int:board_id>/popular_posts', methods=['GET'])
async def get_popular_posts(request, board_id):
    '''
    인기 글 반환
    '''
    popular_posts = db.get_popular_posts(board_id)
    return response.json(popular_posts, status=200)
