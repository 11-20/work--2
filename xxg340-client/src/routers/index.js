import { createRouter, createWebHashHistory } from 'vue-router';
import { AUTH_WHITE_LIST } from '@/config/config';
import { ElNotification } from 'element-plus';
import { staticRouter, errorRouter } from '@/routers/modules/staticRouter';

import { GlobalStore } from '@/stores';
import { AuthStore } from '@/stores/modules/auth';
import { LOGIN_URL } from '@/config/config'
/**
 * @description 动态路由参数配置简介
 * @param path ==> 菜单路径
 * @param name ==> 菜单别名
 * @param redirect ==> 重定向地址
 * @param component ==> 视图文件路径
 * @param meta ==> 菜单信息
 * @param meta.icon ==> 菜单图标
 * @param meta.title ==> 菜单标题
 * @param meta.isLink ==> 是否外链
 * @param meta.isHide ==> 是否隐藏
 * @param meta.isFull ==> 是否全屏(示例：数据大屏页面)
 * @param meta.isAffix ==> 是否固定在 tabs nav
 * @param meta.isKeepAlive ==> 是否缓存
 * */
const router = createRouter({
	history: createWebHashHistory(),
	routes: [...staticRouter, ...errorRouter],
	strict: false,
	scrollBehavior: () => ({ left: 0, top: 0 })
});

/**
 * @description 路由拦截 beforeEach
 * */
router.beforeEach(async (to, from, next) => {

	// 如果是访问登陆页，直接放行
	if ( AUTH_WHITE_LIST.includes(to.path) ) return next();

	// 判断是否有 Token，没有重定向到 login
	const globalStore = GlobalStore();
	if (!globalStore.token) return next({ path: LOGIN_URL, replace: true });
	
	next();
});


/**
 * @description 路由跳转错误
 * */
router.onError(error => {
	console.log('error', error)
	ElNotification.error({ title: '路由错误', message: error.message });
});

export default router;
