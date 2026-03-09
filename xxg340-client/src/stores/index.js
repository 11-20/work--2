import { defineStore, createPinia } from 'pinia';
import { DEFAULT_PRIMARY } from '@/config/config';
import piniaPersistConfig from '@/config/piniaPersist';
import piniaPluginPersistedstate from 'pinia-plugin-persistedstate';
import { request } from '@/http/index';
// defineStore 调用后返回一个函数，调用该函数获得 Store 实体
export const GlobalStore = defineStore({
	// id: 必须的，在所有 Store 中唯一
	id: 'GlobalState',
	// state: 返回对象的函数
	state: () => ({
		siteName: 'Vue3-cms',
		version: '1.0.0',
		// token
		token: '2019',
		button: [],
		// userInfo
		userInfo: '',
		// element组件大小
		assemblySize: 'medium',
		// language
		language: 'cn',
		// themeConfig
		themeConfig: {
			// 布局切换 ==>  纵向：vertical | 经典：classic | 横向：transverse | 分栏：columns
			layout: 'transverse',
			// 默认 primary 主题颜色
			primary: '#FF7F47',
			// 主要颜色 如header背景 side背景
			mainColor: '#FF7F47',
			// 深色模式
			isDark: false,
			// 灰色模式
			isGrey: false,
			// 色弱模式
			isWeak: false,
			// 折叠菜单
			isCollapse: false,
			// 面包屑导航
			breadcrumb: true,
			// 面包屑导航图标
			breadcrumbIcon: true,
			// 标签页
			tabs: true,
			// 标签页图标
			tabsIcon: true,
			// 页脚
			footer: false,
			// 当前页面是否全屏
			maximize: false
		}
	}),
	getters: {},
	actions: {
		setGlobalState(data) {
			for (const key in data) {
				if (Object.hasOwnProperty.call(data, key) && Object.hasOwnProperty.call(this, key)) {
					const newData = data[key]
					this[key] = newData
				}
			}
		},
		// setToken
		setToken(token) {
			this.token = token;
		},
		// setUserInfo
		setUserInfo(userInfo) {
			this.userInfo = userInfo;
		},
		// setAssemblySizeSize
		setAssemblySizeSize(assemblySize) {
			this.assemblySize = assemblySize;
		},
		// updateLanguage
		updateLanguage(language) {
			this.language = language;
		},
		// setThemeConfig
		setThemeConfig(themeConfig) {
			this.themeConfig = themeConfig;
		},
		async getWebSiteMsg() {
			const data = await request("/basic/getwebsiteinfo", {})
			if (!data) return;
			this.setGlobalState({
				
				userInfo: data.currentUser,
				button: data.button
			})
			const makeMapData = (menu) => {
				menu.forEach(item=>{
					if (item.children) {
						makeMapData(item.children)
					}
					item.children = item.children || []
					item.path = "/"+(item.url ? item.url :item.id)
					item.component = "/"+(item.url ? item.url :item.id)
					item.path = item.path.replace("//","/")
					item.component = item.component.replace("//","/")
					item.meta =  {
						"icon": item.icon,
						"title": item.name,
						"isLink": "",
						"isHide": false,
						"isFull": false,
						"isAffix": true,
						"isKeepAlive": true
					}
				})
				return menu
			}
			const menus = makeMapData(data.menu)
			localStorage.setItem("menuData",JSON.stringify(menus))

		}
	},
	persist: piniaPersistConfig('GlobalState')
});

// piniaPersist(持久化)
const pinia = createPinia();
pinia.use(piniaPluginPersistedstate);

export default pinia;
