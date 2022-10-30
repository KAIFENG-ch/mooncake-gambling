class JsonResponse:
    """
    统一的json格式
    """

    def __init__(self, data, code, msg):
        self.data = data
        self.code = code
        self.msg = msg

    @classmethod
    def success(cls, data=None, code=0, msg='success'):
        return cls(data, code, msg)

    @classmethod
    def error(cls, data=None, code=-1, msg='error'):
        return cls(data, code, msg)

    def to_dict(self):
        """
        将数据转化为json值返回
        :return:json的值
        """
        return {
            'code': self.code,
            'data': self.data,
            'msg': self.msg
        }
