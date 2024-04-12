import time

from flask import jsonify, request
from flask_restful import Resource, reqparse
from app.utils import StandardResponse,get_text_from_picture_rb,get_question_from_raw_img_text,get_question_answer,get_recommended_questions
from flask_jwt_extended import  get_jwt_identity, jwt_required
ques_times = 0


class Ques(Resource):
    @jwt_required
    def post(self):
        global ques_times
        img = request.files['pic']
        # 保存图片
        answer = get_question_answer(get_question_from_raw_img_text(get_text_from_picture_rb(img)))
        return StandardResponse(data={'question_explaination': answer}).to_dict()


class RecommendQues(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('quesId', type=int, required=False)
        self.parser.add_argument('ques', type=str, required=False)

    @jwt_required
    def post(self):
        args = self.parser.parse_args()
        ques = args['ques']
        # ques和quesId只能有一个, 如果说这道题题库中有，那么肯定客户端发quesId,因为你在之前发的数据就有quesId,但是如果之前的解释题库没有，当时quesId就是空的，这时会直接发ques，根据ques提供相似题目
        return StandardResponse(data={'recommended_questions': get_recommended_questions(ques)}).to_dict()