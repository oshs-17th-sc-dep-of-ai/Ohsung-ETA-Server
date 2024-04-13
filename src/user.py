from sanic import Sanic, response
from util.database import Database

app = Sanic(__name__)
db = Database('database.db')
db.create_users_table()

@app.route('/user/register', methods=['POST'])
async def register(request):
    '''
    가입
    '''
    data = request.json
    username = data.get('username')
    password = data.get('password')
    if username and password:
        user_id = db.register_user(username, password)
        if user_id:
            return response.json({"user_id": user_id, "message": "User registered successfully"}, status=201)
        else:
            return response.json({"error": "Username already exists"}, status=400)
    else:
        return response.json({"error": "Username and password are required"}, status=400)

@app.route('/user/login', methods=['POST'])
async def login(request):
    '''
    로그인
    '''
    data = request.json
    username = data.get('username')
    password = data.get('password')
    if username and password:
        user_id = db.authenticate_user(username, password)
        if user_id:
            # TODO : 로그인 처리
            return response.json({"user_id": user_id, "message": "Login successful"})
        else:
            return response.json({"error": "Invalid username or password"}, status=401)
    else:
        return response.json({"error": "Username and password are required"}, status=400)

@app.route('/user/logout', methods=['POST'])
async def logout(request):
    '''
    로그아웃
    '''
    # TODO : 로그아웃 처리
    return response.json({"message": "Logout successful"})

@app.route('/user/profile/<int:user_id>', methods=['GET', 'PATCH'])
async def profile(request, user_id):
    if request.method == 'GET':
        '''
        사용자 프로필 반환
        '''
        user_profile = db.get_user_profile(user_id)
        if user_profile:
            return response.json(user_profile)
        else:
            return response.json({"error": "User not found"}, status=404)
    elif request.method == 'PATCH':
        '''
        계정 정보 수정
        '''
        data = request.json
        new_username = data.get('username')
        new_password = data.get('password')
        if new_username or new_password:
            success = db.update_user_profile(user_id, new_username, new_password)
            if success:
                return response.json({"message": "Profile updated successfully"})
            else:
                return response.json({"error": "User not found"}, status=404)
        else:
            return response.json({"error": "No changes to update"}, status=400)
