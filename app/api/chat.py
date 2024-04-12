from flask_restful import Resource, reqparse
from flask_jwt_extended import  get_jwt_identity, jwt_required
from ..db import User,db,ConversationHistory
from ..utils import StandardResponse
from datetime import datetime
from ..utils import get_conversation_title,pack_query, get_conversation_title_with_question, get_response_for_chat

class GetChatSession(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('page', type=int, required=True)
        self.parser.add_argument('per_page', type=int, required=False, default=10,
                                 help='per_page is optional')

    @jwt_required()
    def post(self):
        args = self.parser.parse_args()
        token = args['token']
        page = args['page']
        per_page = args['per_page']
        user_email = get_jwt_identity()
        user = User.query.filter_by(email=user_email).first()

        if user is None:
            return StandardResponse(code=500, message='token失效或者用户被注销').to_dict()

        pagination = user.conversation_history.paginate(page, per_page, False)
        conversations = pagination.items
        print(conversations)
        return StandardResponse(data=conversations).to_dict()



class GetAnswer(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('chatId', type=int, required=True)
        self.parser.add_argument('ques', type=str, required=True)

    def post(self,):
        global get_answer_times
        args = self.parser.parse_args()
        token = args['token']
        chat_id = args['chatId']
        ques = args['ques']
        args = self.parser.parse_args()
        user_email = get_jwt_identity()
        user = User.query.filter_by(email=user_email).first()

        if user is None:
            return StandardResponse(code=500, message='token失效或者用户被注销').to_dict()

        conversation_history = ConversationHistory.query.filter_by(user_id=user.id).filter_by(id=args[chat_id]).first()
        if conversation_history is None:
            return StandardResponse(code=500, message='用户没有此对话记录，chatid可能有误').to_dict()
        chat_context = conversation_history.content.append(ques)
        response = get_response_for_chat(chat_context)
        conversation_history.content.append(response)
        db.session.commit()

        return StandardResponse(data={'ans':response}).to_dict()


class NewChat(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('query', type=str,required=True)  # 用户关于问题的提问，如果此次回答并非来自一个具体问题，只是普通Ti问，下面的fromQues字段为False
        self.parser.add_argument('ques', type=str, required=False, default=None)

    @jwt_required()
    def post(self):
        args = self.parser.parse_args()
        query = args['query']
        ques = args['ques']
        user_email = get_jwt_identity()
        user = User.query.filter_by(email=user_email).first()

        if user is None:
            return StandardResponse(code=500, message='token失效或者用户被注销').to_dict()

        new_conversation = ConversationHistory(
            user_id=user.id,
            title="",
            last_modified=datetime.now(),
            content=[]
        )
        if ques:
            new_conversation.title = get_conversation_title_with_question(ques,query)
            query = pack_query(query,'title') # 这里mode还没确定
        else:
            new_conversation.title = get_conversation_title(query)

        response = get_response_for_chat([query])
        new_conversation.content.append(query)
        new_conversation.content.append(response)
        db.session.add(new_conversation)
        db.session.commit()
        chat_id = new_conversation.id

        return StandardResponse(data={
            'chatId': chat_id,
            'ans': response,
            'title': new_conversation.title
        }).to_dict()

class GetChatHistory(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('chatId', type=int, required=True)
        self.parser.add_argument('page', type=int, required=True)
        self.parser.add_argument('per_page', type=int, required=False, default=10,
                                 help='per_page is optional')

    def post(self):
        args = self.parser.parse_args()
        page = args['page']
        per_page = args['per_page']
        user_email = get_jwt_identity()
        user = User.query.filter_by(email=user_email).first()

        if user is None:
            return StandardResponse(code=500, message='token失效或者用户被注销').to_dict()

        conversation_history = ConversationHistory.query.filter_by(user_id=user.id).filter_by(id = args['chatId']).first()
        if conversation_history is None:
            return StandardResponse(code=500, message='用户没有此对话记录，chatid可能有误').to_dict()
        return StandardResponse(data=conversation_history.content[(page-1)*per_page+1:(page)*per_page+1]).to_dict()