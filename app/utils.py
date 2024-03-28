from flask import jsonify

class StandardResponse:
    def __init__(self, msg="", status_code=200, content=None):
        if content is None:
            content = {}
        self.msg = msg
        self.status_code = status_code
        self.content = content

    def to_dict(self):
        return {
            'status_code': self.status_code,
            'msg': self.msg,
            'content': self.content
        }

def make_standard_response(user_token="", status_code=200, content=None):
    response = StandardResponse(user_token, status_code, content)
    return jsonify(response.to_dict()), status_code


# zheliyaoxieprompt