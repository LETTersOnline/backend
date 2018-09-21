class Choices:
    @classmethod
    def choices(cls):
        d = cls.__dict__
        ret = [d[item] for item in d.keys() if not item.startswith("__")]
        ret.sort(reverse=True)
        return ret

    @classmethod
    def model_choices(cls):
        # 通过这种方式生成model当中使用的choices，显示为属性名，存储为属性值
        d = cls.__dict__
        ret = [(d[item], item) for item in d.keys() if not item.startswith("__")]
        ret.sort(reverse=True)
        return ret


class RegisterMethod(Choices):
    """
    三种注册类型设置
    1. 无限制
    2. 邀请码注册
    3. 禁止注册
    """
    ANY = 'any'
    CODE = 'code'
    BAN = 'ban'


class UserType(Choices):
    REGULAR = 1  # 普通用户
    LETTERS = 2  # LETTers队员
    COACH = 3  # 教练
    ADMIN = 4  # 管理员
    SUPER_ADMIN = 5  # 超级管理员
