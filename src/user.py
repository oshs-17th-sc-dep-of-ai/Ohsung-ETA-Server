from sanic import Sanic, response
from sanic_session import Session, InMemorySessionInterface
from util.database import Database

app = Sanic(__name__)
session = Session(app, interface=InMemorySessionInterface())
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
            request['session']['user_id'] = user_id
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
    session_data = request['session']
    if 'user_id' in session_data:
        del session_data['user_id']
        return response.json({"message": "Logout successful"})
    else:
        return response.json({"error": "You are already logged out"}, status=400)

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
