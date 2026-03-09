import { HOME_URL, LOGIN_URL } from '@/config/config';

/**
 * staticRouter(静态路由)
 */
export const staticRouter = [
	{
		path: '/',
		redirect: LOGIN_URL
	},
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

	{
		path: '/layout',
		name: 'layout',
		component: () => import('@/layouts/index.vue'),
		redirect: HOME_URL,
		children: [
			{
				path: '/user/edit',
				name: 'useredit',
				component: () => import('@/views/user/edit.vue'),
				meta: {
					title: '个人信息'
				}
			},
			{
				path: '/user/manage',
				name: 'userm',
				component: () => import('@/views/sys/usermanage.vue'),
				meta: {
					title: '用户管理'
				}
			},
		]
	},
	
];

