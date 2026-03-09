import { HOME_URL, LOGIN_URL } from '@/config/config';
import  dynamicRouter  from '@/routers/modules/dynamicRouter';

/**
 * staticRouter(静态路由)
 */
export const staticRouter = [
	
	{
		path: LOGIN_URL,
		name: 'login',
		component: () => import('@/views/login/index.vue'),
		meta: {
			title: '登录页'
		}
	},
	{
		path: '/dashboard/index',
		name: 'dashboard',
		component: () => import('@/views/dashboard/index/index.vue'),
		meta: {
			title: '数据大屏'
		}
	},
			// ...dynamicRouter,
	
	{
		path: '/layout',
		name: 'layout',
		component: () => import('@/layouts/index.vue'),
		redirect: HOME_URL,
		children: [
			...dynamicRouter,
			{
				path: '/',
				component: () => import('@/views/index/index/index.vue'),
			},
			{
				path: '/user/edit',
				component: () => import('@/views//user/edit.vue'),
			},
			{
				path: '/payment',
				component: () => import('@/views/payment/index.vue'),
			},
			
		]
	},
	
];

/**
 * errorRouter(错误页面路由)
 */
export const errorRouter = [
	
];

/**
 * notFoundRouter(找不到路由)
 */
export const notFoundRouter = {
	path: '/:pathMatch(.*)*',
	name: 'notFound',
	redirect: { name: '404' }
};
