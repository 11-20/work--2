import { request } from '@/http/index';
export default class UserService {
  static async getUserData(params) {
    return request('/user/data', params, 'get')
  }
}