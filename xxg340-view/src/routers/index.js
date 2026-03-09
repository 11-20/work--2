import { createRouter, createWebHashHistory } from 'vue-router';
import { AUTH_WHITE_LIST } from '@/config/config';
import { ElNotification } from 'element-plus';
import { initDynamicRouter } from '@/routers/modules/dynamicRouter';
import { staticRouter } from '@/routers/modules/staticRouter';
import NProgress from '@/config/nprogress';
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
	routes: [...staticRouter ],
	strict: false,
	scrollBehavior: () => ({ left: 0, top: 0 })
});

/**
 * @description 路由拦截 beforeEach
 * */
router.beforeEach(async (to, from, next) => {

	// NProgress 开始
	NProgress.start();

	// 如果是访问登陆页，直接放行
	if ( AUTH_WHITE_LIST.includes(to.path) ) return next();

	// 判断是否有 Token，没有重定向到 login
	// const globalStore = GlobalStore();
	// if (!globalStore.token) return next({ path: LOGIN_URL, replace: true });

	// 如果没有菜单列表，就重新请求菜单列表并添加动态路由
	const authStore = AuthStore();

	if (!authStore.authMenuListGet.length) {
		console.log('没有菜单列表')
		await initDynamicRouter();

		return next({ ...to, replace: true });
	}
    console.log('有菜单列表',authStore.authMenuListGet)
	
	next();
});

/**
 * @description 路由跳转结束
 * */
router.afterEach(() => {
	NProgress.done();
});

/**
 * @description 路由跳转错误
 * */
router.onError(error => {
	NProgress.done();
	console.log('error', error)
	ElNotification.error({ title: '路由错误', message: error.message });
});

export default router;
