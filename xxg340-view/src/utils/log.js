// utils/logger.js
import { request } from '@/http/index.js';
import { GlobalStore } from '@/stores';
import axios from 'axios';

/**
 * 获取用户标识（代替IP）
 */
export const getUserIdentifier = () => {
    const globalStore = GlobalStore();
    const token = globalStore.token;
    
    if (token) {
        return `user_${globalStore.userInfo?.id || 'unknown'}`;
    }
    
    let sessionId = sessionStorage.getItem('session_id');
    if (!sessionId) {
        sessionId = `anon_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;
        sessionStorage.setItem('session_id', sessionId);
    }
    
    return sessionId;
};

export const getClientIP = () => {
    return getUserIdentifier();
};

/**
 * 限制日志内容长度
 */
const limitLogContent = (content, maxLength = 1000) => {
    if (typeof content === 'string' && content.length > maxLength) {
        return content.substring(0, maxLength) + '... [内容过长已截断]';
    }
    return content;
};

/**
 * 简化数据记录，避免记录过多内容
 */
const simplifyData = (data, maxProperties = 5) => {
    if (!data || typeof data !== 'object') return data;
    
    if (Array.isArray(data)) {
        // 如果是数组，只记录前几个元素
        return data.slice(0, 3).map(item => 
            typeof item === 'object' ? '[对象]' : item
        );
    }
    
    // 如果是对象，只记录前几个属性
    const simplified = {};
    let count = 0;
    for (const key in data) {
        if (data.hasOwnProperty(key) && count < maxProperties) {
            const value = data[key];
            if (typeof value === 'object' && value !== null) {
                simplified[key] = '[对象]';
            } else {
                simplified[key] = value;
            }
            count++;
        }
    }
    if (Object.keys(data).length > maxProperties) {
        simplified['_message'] = `... [还有${Object.keys(data).length - maxProperties}个属性未显示]`;
    }
    return simplified;
};

/**
 * 生成请求日志数据
 */
export const generateRequestLog = (config, level = 'info') => {
    const { url, method, params, data, headers } = config;
    
    // 敏感信息过滤
    const safeData = data && typeof data === 'object' ? { ...data } : { rawData: data };
    if (safeData.password) safeData.password = '***';
    if (safeData.token) safeData.token = '***';
    if (safeData.authorization) safeData.authorization = '***';
    
    const logContent = {
        url,
        method: method?.toUpperCase(),
        params: simplifyData(params),
        data: simplifyData(safeData),
        timestamp: new Date().toISOString()
    };

    return {
        logstitle: `API请求 - ${method?.toUpperCase()} ${getSimpleUrl(url)}`,
        loglevel: level,
        logcontent: limitLogContent(JSON.stringify(logContent, null, 2)),
        logip: getClientIP()
    };
};

/**
 * 生成响应日志数据
 */
export const generateResponseLog = (config, response, level = 'info') => {
    const { url, method } = config;
    const { status, data: responseData } = response;
    
    const logLevel = status >= 400 ? 'error' : level;
    
    const logContent = {
        url,
        method: method?.toUpperCase(),
        status,
        responseData: simplifyData(responseData && typeof responseData === 'object' ? 
            (responseData.retobj || responseData) : 
            { rawData: responseData }),
        timestamp: new Date().toISOString()
    };

    return {
        logstitle: `API响应 - ${method?.toUpperCase()} ${status} ${getSimpleUrl(url)}`,
        loglevel: logLevel,
        logcontent: limitLogContent(JSON.stringify(logContent, null, 2)),
        logip: getClientIP()
    };
};

/**
 * 生成错误日志数据
 */
export const generateErrorLog = (config, error, level = 'error') => {
    if (!config) {
        return {
            logstitle: '未知请求错误',
            loglevel: 'error',
            logcontent: `错误信息: ${error?.message || '未知错误'}`,
            logip: getClientIP()
        };
    }

    const { url, method, params, data } = config;
    const { message, code, response } = error;
    
    // 敏感信息过滤
    const safeData = data && typeof data === 'object' ? { ...data } : { rawData: data };
    if (safeData.password) safeData.password = '***';
    if (safeData.token) safeData.token = '***';
    if (safeData.authorization) safeData.authorization = '***';
    
    const errorContent = {
        url,
        method: method?.toUpperCase(),
        params: simplifyData(params),
        requestData: simplifyData(safeData),
        error: {
            message: message || '未知错误',
            code: code || 'UNKNOWN_ERROR',
            status: response?.status,
            statusText: response?.statusText
        },
        timestamp: new Date().toISOString()
    };

    return {
        logstitle: `API错误 - ${method?.toUpperCase()} ${getSimpleUrl(url)}`,
        loglevel: level,
        logcontent: limitLogContent(JSON.stringify(errorContent, null, 2)),
        logip: getClientIP()
    };
};

/**
 * 生成业务错误日志数据
 */
export const generateBusinessErrorLog = (config, errorData, level = 'error') => {
    const { url, method } = config;
    const { errcode, errmsg } = errorData;
    
    const logContent = {
        url,
        method: method?.toUpperCase(),
        errorCode: errcode,
        errorMessage: errmsg,
        timestamp: new Date().toISOString()
    };

    return {
        logstitle: `业务错误 - ${method?.toUpperCase()} ${getSimpleUrl(url)}`,
        loglevel: level,
        logcontent: limitLogContent(JSON.stringify(logContent, null, 2)),
        logip: getClientIP()
    };
};

/**
 * 简化URL显示
 */
const getSimpleUrl = (url) => {
    if (!url) return 'unknown';
    // 移除基础URL部分，只显示路径
    const baseURL = axios.defaults.baseURL;
    if (baseURL && url.startsWith(baseURL)) {
        return url.replace(baseURL, '');
    }
    return url;
};


export const recordSysLog = async (logData) => {
    return
    try {
        // 检查是否是日志记录自身的请求，如果是则跳过
        if (window._isLoggingRequest) {
            return;
        }
        
        const { logstitle, loglevel = 'info', logcontent, logip, ...extraData } = logData;
        
        // 检查日志内容是否包含 syslog 相关请求，如果是则跳过
        let shouldSkip = false;
        
        // 方法1：检查日志标题是否包含 syslog
        if (logstitle && logstitle.toLowerCase().includes('syslog')) {
            shouldSkip = true;
        }
        
        // 方法2：检查日志内容是否包含 syslog 相关路径
        if (logcontent && typeof logcontent === 'string') {
            const syslogPaths = ['/syslog/store', '/syslog/index', '/syslog/clear', '/syslog/destroy'];
            if (syslogPaths.some(path => logcontent.includes(path))) {
                shouldSkip = true;
            }
        }
        
        // 方法3：如果是对象形式的日志内容，检查URL字段
        if (logcontent && typeof logcontent === 'object') {
            const contentStr = JSON.stringify(logcontent).toLowerCase();
            if (contentStr.includes('/syslog/')) {
                shouldSkip = true;
            }
        }
        
        if (shouldSkip) {
            console.log('跳过 syslog 相关请求的日志记录');
            return;
        }
        
        const logPayload = {
            logstitle: logstitle || '系统日志',
            loglevel,
            logcontent: typeof logcontent === 'object' ? JSON.stringify(logcontent, null, 2) : String(logcontent),
            logip: logip || getClientIP(),
            ...extraData
        };

        // 设置标记，表示正在记录日志
        window._isLoggingRequest = true;
        
        // 异步记录日志，不阻塞主流程
        setTimeout(() => {
            request('/syslog/store', logPayload, 'POST')
                .catch(error => {
                    console.error('记录日志失败:', error);
                })
                .finally(() => {
                    // 清除标记
                    window._isLoggingRequest = false;
                });
        }, 0);
        
    } catch (error) {
        console.error('日志记录异常:', error);
        window._isLoggingRequest = false;
    }
};