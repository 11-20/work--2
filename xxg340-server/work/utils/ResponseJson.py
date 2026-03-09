from django.http import JsonResponse

class ResponseJsonData:
    def __init__(self, errcode=0, errmsg='', retobj=None):
        self.errcode = errcode
        self.errmsg = errmsg
        self.retobj = retobj

    async def to_json_response_async(self):
        response_data = {
            'errcode': self.errcode,
            'errmsg': self.errmsg,
            'retobj': self.retobj
        }
        return JsonResponse(response_data)

    def to_json_response(self):
        response_data = {
            'errcode': self.errcode,
            'errmsg': self.errmsg,
            'retobj': self.retobj
        }
        return JsonResponse(response_data)
