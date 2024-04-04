from quart import Quart, request, jsonify
from util.database import Database

app = Quart(__name__)

@app.route('/user/register', methods=['POST'])
async def register():
    '''
    가입
    '''
    
@app.route('/user/login', method=['POST'])
async def login():
    '''
    로그인
    '''
    
@app.route('/user/logout', method=['POST'])
async def login():
    '''
    로그아웃
    '''

@app.route('/user/profile/<user_id>', method=['GET'])
async def profile():
    '''
    사용자 프로필 반환
    '''

@app.route('/user/patch', method=['GET'])
async def profile():
    '''
    계정 정보 수정
    '''

