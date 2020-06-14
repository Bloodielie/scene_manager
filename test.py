def get_module_dir(user_object):
    return {dir_ for dir_ in dir(user_object) if not dir_.endswith('__')}


class SceneConfigMetaclass(type):
    def __init__(cls, class_name, parents, attributes):
        if parents:
            new_config = getattr(cls, "Config")
            old_config = getattr(parents[0], "Config")
            for user_attr in get_module_dir(old_config):
                try:
                    getattr(new_config, user_attr)
                except AttributeError:
                    setattr(new_config, user_attr, getattr(old_config, user_attr))

        super().__init__(class_name, parents, attributes)


class MessageScene(metaclass=SceneConfigMetaclass):
    class Config:
        content_types = "text"
        agagagag = 1

    @classmethod
    def generate_config_dict(self):
        a = get_module_dir(self.Config)
        dict_ = {}
        for i in a:
            dict_[i] = getattr(self.Config, i)
        return dict_


class A(MessageScene):
    class Config:
        agagagag = 123
        bbbabab = 12313


class B(A):
    pass


a = B()
a.Config.content_types = '123'
print(a.Config.agagagag)
print(a.generate_config_dict())
