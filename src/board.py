from quart import Quart, request, jsonify
from util.database import Database

app = Quart(__name__)
db = Database('database.db')
db.create_table()

@app.route('/board/write_post', methods=['POST'])
async def write_post():
    '''
    새 글 작성
    '''
    data = await request.json
    board_id = data.get('board_id')
    title = data.get('title')
    content = data.get('content')

    if board_id and title and content:
        db.write_post(board_id, title, content)
        return jsonify({"message": "Post created successfully"}), 201
    else:
        return jsonify({"error": "Board ID, title, and content are required"}), 400

@app.route('/board/popular_posts', methods=['GET'])
async def popular_posts():
    '''
    인기 글 반환
    '''
    posts = db.get_popular_posts()
    return jsonify(posts)

@app.route('/board/like_post/<int:post_id>', methods=['POST'])
async def like_post(post_id):
    '''
    post_id 추천 수 증가
    '''
    db.like_post(post_id)
    return jsonify({"message": "Post liked successfully"}), 200

@app.route('/board/dislike_post/<int:post_id>', methods=['POST'])
async def dislike_post(post_id):
    '''
    post_id 추천 수 감소
    '''
    db.dislike_post(post_id)
    return jsonify({"message": "Post disliked successfully"}), 200

