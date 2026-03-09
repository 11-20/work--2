import { request } from '@/http/index';
export default class SystemService {
   
    // 图片上传
    static async uploadImg (params) {
        return request ('/basic/uploadsinglefile',params,'post')
        
    };
    
    // * 视频上传
    static async uploadVideo (params) {
        return request ('/file/upload/video',params,'get')
    };
    
}


