import { defineStore } from 'pinia';
import UserService from '@/api/user';
import { getKeepAliveRouterName, getShowMenuList, getAllBreadcrumbList } from '@/utils/util';
import piniaPersistConfig from '@/config/piniaPersist';


// AuthStore
export const AuthStore = defineStore({
	id: 'AuthState',
	state: () => ({
		authButtonList: {},
		// menuList 作为动态路由，不会做持久化存储
		authMenuList: []
	}),
	getters: {
		// 后端返回的菜单列表
		authMenuListGet: state => state.authMenuList,
		// 后端返回的菜单列表 ==> 左侧菜单栏渲染，需要去除 isHide == true
		showMenuListGet: state => getShowMenuList(state.authMenuList),
		// 面包屑导航列表
		breadcrumbListGet: state => getAllBreadcrumbList(state.authMenuList),
		// 需要缓存的菜单 name，用作页面 keepAlive
		keepAliveRouterGet: state => getKeepAliveRouterName(state.authMenuList)
	},
	actions: {
		
		// 获取菜单列表
		async getAuthMenuList() {
			const { data } = await UserService.getMenuList();
			console.log('菜单列表是=====', data)
			this.authMenuList = data;
		}
	},
});
