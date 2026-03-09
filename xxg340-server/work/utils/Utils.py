import jwt

class Utils:
    @staticmethod
    def convert_to_tree(data: object) -> object:
        map_dict = {}
        tree = []

        for node in data:
            map_dict[node['id']] = {**node, 'children': []}

        for node in map_dict.values():
            if node['parentId'] != 0:
                parent_node = map_dict.get(node['parentId'])
                if parent_node:
                    parent_node['children'].append(node)
            else:
                tree.append(node)

        return tree

    def parse_token(auth_token):
        try:
            # 解码 JWT 令牌
            decoded_token = jwt.decode(auth_token, 'jwtSecret', algorithms=['HS256'])

            # 返回解码后的信息
            return decoded_token
        except jwt.ExpiredSignatureError:
            # 处理令牌过期的情况
            return {'error': 'Token has expired'}
        except jwt.InvalidTokenError:
            # 处理无效的令牌
            return {'error': 'Invalid token'}