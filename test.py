def get_module_dir(user_object):
    return {dir_ for dir_ in dir(user_object) if not dir_.endswith('__')}


class SceneConfigMetaclass(type):
    def __init__(cls, class_name, parents, attributes):
        if not parents:
            super().__init__(class_name, parents, attributes)
            return

        new_config = attributes.get("Config")
        if new_config is None:
            super().__init__(class_name, parents, attributes)
            return

        for parent in parents:
            old_config = getattr(parent, "Config")
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
    class Config:
        a = 1231

from time import time

time1 = time()
for i in range(10000000):
    B()
print(time()-time1)
