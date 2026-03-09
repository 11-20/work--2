# myapp/middleware.py
from work.utils.ResponseJson import ResponseJsonData
from work.utils.Utils import Utils
import jwt

class AuthMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        # 定义白名单
        self.excluded_paths = ["index","show","/signin", "/register","/uploadsinglefile"]

    def __call__(self, request):
        # 在请求到达之前执行的代码
        print(f"接受到请求 [{request.method}]--{request.path}--start")
        print("该请求前端传递的参数是", request.GET)
        print(f"接受到请求 [{request.method}]--{request.path}--end")
        
        # 静态文件直接放行
        if self.is_static_file(request.path):
            print(f"Allowing access to static file: {request.path}")
            return self.get_response(request)
        # 如果当前请求路径在白名单中，则直接放行
        if any(path in request.path for path in self.excluded_paths):
            print("请求路径在白名单中，直接放行")
            return self.get_response(request)

        # 在这里实现你的 JWT 验证逻辑
        auth_header = request.headers.get('Authorization')
        if auth_header and auth_header.startswith('Bearer '):
            # 提取 Token
            token = auth_header[7:]
            print(f"token是 [{token}]")
            try:
                claims  = jwt.decode(token, 'jwtSecret', algorithms=['HS256'])
                # 判断 claims 不为 null
                if claims:
                    # 将用户信息存储在请求中
                    print("当前登录用户：")
                    print(claims)
                    request.user = {
                        'user_id': claims.get('user_id'),
                        'id': claims.get('user_id'),
                        'user_name': claims.get('user_name'),
                        'avatar': claims.get('avatar'),
                        'is_super': claims.get('is_super'),
                        'phone': claims.get('phone'),
                        'email': claims.get('email'),
                        'role_id': claims.get('role_id'),
                        'sex': claims.get('sex'),
                    }
                    return self.get_response(request)
                else:
                    return ResponseJsonData(errcode=500, errmsg='登录已过期，请重新登录', retobj="token无效").to_json_response()

            except jwt.ExpiredSignatureError:
                return ResponseJsonData(errcode=500, errmsg='登录已过期，请重新登录', retobj="token无效").to_json_response()
            except jwt.InvalidTokenError:
                return ResponseJsonData(errcode=500, errmsg='登录已过期，请重新登录', retobj="token无效").to_json_response()


        response = self.get_response(request)


        return response

    @staticmethod
    def is_static_file(path):
        # 实现你的判断逻辑，判断是否是静态文件
        # 这里简单地通过路径中是否包含 '/uploads/' 来判断
        return '/uploads/' in path
