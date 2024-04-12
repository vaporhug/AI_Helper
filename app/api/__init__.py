from .chat import *
from .note import *
from .ques import *
from .user_auth import *

def init_api(api):
    api.add_resource(SignIn, '/account/sign_in')
    api.add_resource(SignUp, '/account/sign_up')
    api.add_resource(CheckCode, '/account/check_code')
    api.add_resource(UpdateUserInfo, '/account/update_info')

    api.add_resource(Ques, '/ques/search_ques')
    api.add_resource(RecommendQues, '/ques/recommend')

    api.add_resource(GetChatSession, '/chat/chat_session')
    api.add_resource(GetAnswer, '/chat/ongoing')
    api.add_resource(NewChat, '/chat/new')

    api.add_resource(GetNoteFileURL, '/note/get_note_url')
