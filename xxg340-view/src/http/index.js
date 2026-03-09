import axios from 'axios';
import { showFullScreenLoading, tryHideFullScreenLoading } from '@/config/serviceLoading';
import { ElMessage } from 'element-plus';
import { showMessage } from './status';
import { AxiosCanceler } from './axiosCancel';
import { GlobalStore } from '@/stores';


// 递归处理对象和数组中的 JSON 字符串
function parseJsonInData(data) {
    if (typeof data === 'string') {
        try {
            // 如果是字符串，尝试解析 JSON
            return JSON.parse(data);
        } catch (e) {
            // 如果解析失败，返回原始字符串
            return data;
        }
    } else if (Array.isArray(data)) {
        // 如果是数组，递归处理数组中的每个元素
        return data.map(item => parseJsonInData(item));
    } else if (typeof data === 'object' && data !== null) {
        // 如果是对象，递归处理对象的每个属性
        const parsedObject = {};
        for (const key in data) {
            if (data.hasOwnProperty(key)) {
                parsedObject[key] = parseJsonInData(data[key]);
            }
        }
        return parsedObject;
    }
    // 如果是其他类型，直接返回
    return data;
}

// 取消重复请求类
const axiosCanceler = new AxiosCanceler();
// 设置接口超时时间
axios.defaults.timeout = 2000000 // 10分钟
// 请求地址
axios.defaults.baseURL = import.meta.env.VITE_API_URL // 请求地址 读取.env文件里面的地址
// 请求拦截器
axios.interceptors.request.use(
    config => {
        const globalStore = GlobalStore();
        const token = globalStore.token
        // * 将当前请求添加到 pending 中 去除重复请求 显示loading
        // axiosCanceler.addPending(config);
        // showFullScreenLoading();
        config.headers = {
            'Content-Type': 'application/json;charset=UTF-8',    // 传参方式json
            Authorization: `Bearer ${token}`
        };

        // 检查 PUT 请求的 URL 中是否包含 id 参数
        if (config.method?.toLowerCase() === 'put') {
            const hasIdInUrl = config.url.includes('id=');
            if (!hasIdInUrl && config.data) {
                // 从载荷中获取 id
                let idValue;
                if (typeof config.data === 'object') {
                    idValue = config.data.id;
                } else if (typeof config.data === 'string') {
                    try {
                        const parsedData = JSON.parse(config.data);
                        idValue = parsedData.id;
                    } catch (e) {
                        console.warn('无法解析请求数据', e);
                    }
                }
                // 如果获取到 id，添加到 URL 中
                if (idValue !== undefined) {
                    const separator = config.url.includes('?') ? '&' : '?';
                    config.url += `${separator}id=${idValue}`;
                    console.log('自动添加 id 参数到 URL:', config.url);
                }
            }
        }

        // 处理 GET 请求的 limit 参数
        if (config.method?.toLowerCase() === 'get' && config.params) {
            const limitParam = config.params.limit;
            Object.keys(config.params).forEach(item => {
                if (!config.params[item] && config.params[item] !== 0 && config.params[item] !== false) {
                    delete config.params[item];
                }
            })
            // 检查 limit 参数是否存在且为汉字
            if (limitParam && typeof limitParam === 'string' && /[\u4e00-\u9fa5]/.test(limitParam)) {
                config.params.limit = '99999';
                console.log('检测到汉字 limit 参数，已自动改为 99999');
            }
        }


        return config;
    },
    error => {
        return Promise.reject(error)
    }
);


// 响应拦截器
axios.interceptors.response.use(
    response => {
        const { data, config } = response;
        const globalStore = GlobalStore();
        // * 在请求结束后，移除本次请求，并关闭请求 loading
        // axiosCanceler.removePending(config);
        tryHideFullScreenLoading()

        console.log("datais",data)
        if (data.errcode && data.errcode != 0) {
            ElMessage.error(data.errmsg)
               return Promise.reject(data.errmsg);
        } else {
            if (Array.isArray(data?.retobj?.data)) {
                data.retobj.data.list = data.retobj.data
                data.retobj.data.data = data.retobj.data

            }
            const returndata = parseJsonInData(data.retobj || data)
            return returndata
        }

    },
    error => {


        tryHideFullScreenLoading();
        const { response } = error;
        if (response) {
            // 传入状态码，匹配响应码对应信息
            console.log(response)
            showMessage(response.status);
            return Promise.reject(response.data);
        } else {
            if (error.code != 'ERR_CANCELED') {
                ElMessage.warning('网络连接异常，请稍后再试！')

            }
        }
    }
);



export function request(url = '', params = {}, type = 'GET') {
    // 设置 url params type 的默认值
    const methodType = type.toUpperCase()
    return new Promise((resolve, reject) => {
        let promise
        const isFileUpload = hasFile(params);
        if (methodType === 'GET' || methodType === 'DELETE') {
            promise = axios({
                method: methodType,
                url,
                params,
            })
        } else if (methodType === 'POST' || methodType === 'PUT') {
            promise = axios({
                method: methodType,
                url,
                data: isFileUpload ? params : processParams(params)
            })
        }
        // 处理返回
        promise.then(res => {
            resolve(res)
        }).catch(err => {
            reject(err)
        })
    })
}




function hasFile(params) {
    return params instanceof FormData
    if (!params || typeof params !== 'object') return false;
    if (Array.isArray(params)) {
        return params.some(item => item instanceof File || item instanceof Blob);
    }

    return Object.values(params).some(value => value instanceof File || value instanceof Blob);
}


function processParams(params) {
    if (!params || typeof params !== 'object') return params;
    if (Array.isArray(params)) return params.map(item => processParams(item));

    const result = {};
    for (const key in params) {
        if (params.hasOwnProperty(key)) {
            const value = params[key];
            if (value instanceof Date) {
                result[key] = formatDate(value);
            } else if (typeof value === 'string' && isISODateString(value)) {
                result[key] = formatDate(new Date(value));
            } else if (typeof value === 'object' && value !== null) {
                result[key] = processParams(value);
            } else {
                result[key] = value;
            }
        }
    }
    return result;
}

// 支持 "2025-06-24T17:14" 和 "2025-06-24T17:14:00Z"
function isISODateString(value) {
    return /^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}(:\d{2})?(\.\d+)?(Z|[+-]\d{2}:\d{2})?$/.test(value);
}

// 格式化为 YYYY-MM-DD HH:mm:ss
function formatDate(date) {
    const year = date.getFullYear();
    const month = String(date.getMonth() + 1).padStart(2, '0');
    const day = String(date.getDate()).padStart(2, '0');
    const hours = String(date.getHours()).padStart(2, '0');
    const minutes = String(date.getMinutes()).padStart(2, '0');
    const seconds = String(date.getSeconds()).padStart(2, '0');
    return `${year}-${month}-${day} ${hours}:${minutes}:${seconds}`;
}