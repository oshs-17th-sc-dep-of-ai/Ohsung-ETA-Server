from quart import Quart, request, jsonify
from util.database import Database

app = Quart(__name__)

@app.route('/chat/user/<user_id>', methods=['POST'])
async def user():
    '''
    유저 채팅
    '''
    
@app.route('/chat/group/<group_id>', method=['POST'])
async def login():
    '''
    그룹 채팅
    '''