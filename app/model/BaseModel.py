from sqlalchemy.orm import synonym

from app import db


class BaseModel:
    """
    数据库映射的基类
    """

    def __commit(self):
        """
        提交数据库，失败时回滚
        :return:
        """
        from sqlalchemy.exc import IntegrityError

        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()

    def delete(self):
        """
        从数据库中删除数据
        :return:
        """
        db.session.delete(self)
        self.__commit()

    def save(self):
        """
        从数据库中增加模型
        :return:
        """
        db.session.add(self)
        self.__commit()
        return self

    @classmethod
    def from_dict(cls, model_dict):
        return cls(**model_dict).save()


def check_length(attribute, length):
    """
    获取类型长度
    :param attribute:
    :param length:
    :return:
    """
    try:
        return bool(attribute) and len(attribute) <= length
    except:
        return False
