import json
import models
from flask import Response, abort, Blueprint


class BaseView:
    __model_class__ = None
    __includes__ = None


    def get(self):
        return [i.serialize() for i in self.__model_class__.query.all()]


    def post(self, info):
        self.__model_class__.post_data(info)

    def update(self, obj_id, info):
        print('update api')
        self.__model_class__.query.get(obj_id).put_data(info)
        print('updated api')
        # return Response("updated", 200)

    def delete(self, obj_id):
        self.__model_class__.query.get(obj_id).delete_data()
        return Response("deleted", 200)

    @staticmethod
    def check_fields(fields, request):
        error = []
        for field in fields:
            if field not in request.values:
                error.append({"key": field, "message": "Value can not be empty"})
            elif request.values[field] is None or not request.values[field].strip():
                error.append({"key": field, "message": "Value can not be empty"})

        return error


class UserModelView(BaseView):
    __model_class__ = models.User
    __prefix__ = "user"