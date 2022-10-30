from flask import Flask, jsonify

from app.serialize.response import JsonResponse


class JsonFlask(Flask):
    def make_response(self, rv):
        """
        视图函数可以直接返回list, dict, none
        :param rv:
        :return:
        """
        if rv is None or isinstance(rv, (list, dict)):
            rv = JsonResponse.success(rv)

        if isinstance(rv, JsonResponse):
            rv = jsonify(rv.to_dict())

        return super().make_response(rv)
