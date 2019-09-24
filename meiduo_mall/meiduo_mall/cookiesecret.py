import json
import pickle
import base64

#
# data_dict = {
#     1:{
#         2:{
#             'count':3,
#             'selected':True
#
#         }
#
#
#     }
#
# }
# json_str = json.dumps(data_dict)
#
#
# json_dict = json.loads(json_str)
#
# pickle_bytes = pickle.dumps(data_dict)
#
# pickle_data = pickle.loads(pickle_bytes)
#
#
# base64_encode = base64.b64encode(pickle_bytes)
# print(base64_encode.decode())
#
#
# base64_decode = base64.b64decode(base64_encode.decode())



class CookieSecret(object):
    @classmethod
    def dumps(cls,data):
        pickle_bytes = pickle.dumps(data)
        base64_encode=base64.b64encode(pickle_bytes)

        return base64_encode.decode()

    @classmethod
    def loads(cls,data):
        base64_decode = base64.b64decode(data)
        data = pickle.loads(base64_decode)


        return data

