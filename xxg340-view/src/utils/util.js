import { isArray } from '@/utils/type';

// 获取用户登录后跳转的第一个页面
export function getHomeUrl(currentMenu) {
	const firstMenu = currentMenu[0]
	let path = firstMenu.path
	if (firstMenu.children &&firstMenu.children.length > 0 ) {
		path = firstMenu.children[0].path
	} 
	return path
}

/**
 * @description 获取localStorage
 * @param {String} key Storage名称
 * @return string
 */
export function localGet(key) {
	const value = window.localStorage.getItem(key);
	try {
		return JSON.parse(window.localStorage.getItem(key));
	} catch (error) {
		return value;
	}
}

/**
 * @description 存储localStorage
 * @param {String} key Storage名称
 * @param {Any} value Storage值
 * @return void
 */
export function localSet(key, value) {
	window.localStorage.setItem(key, JSON.stringify(value));
}

/**
 * @description 清除localStorage
 * @param {String} key Storage名称
 * @return void
 */
export function localRemove(key) {
	window.localStorage.removeItem(key);
}

/**
 * @description 清除所有localStorage
 * @return void
 */
export function localClear() {
	window.localStorage.clear();
}

/**
 * @description 判断数据类型
 * @param {Any} val 需要判断类型的数据
 * @return string
 */
export function isType(val) {
	if (val === null) return 'null';
	if (typeof val !== 'object') return typeof val;
	else return Object.prototype.toString.call(val).slice(8, -1).toLocaleLowerCase();
}

/**
 * 判断两个对象是否相同
 * @param a 要比较的对象一
 * @param b 要比较的对象二
 * @returns 相同返回 true，反之则反
 */
export function isObjectValueEqual(a, b) {
	if (!a || !b) return false;
	let aProps = Object.getOwnPropertyNames(a);
	let bProps = Object.getOwnPropertyNames(b);
	if (aProps.length != bProps.length) return false;
	for (let i = 0; i < aProps.length; i++) {
		let propName = aProps[i];
		let propA = a[propName];
		let propB = b[propName];
		if (!b.hasOwnProperty(propName)) return false;
		if (propA instanceof Object) {
			if (!isObjectValueEqual(propA, propB)) return false;
		} else if (propA !== propB) {
			return false;
		}
	}
	return true;
}

/**
 * @description 生成随机数
 * @param {Number} min 最小值
 * @param {Number} max 最大值
 * @return number
 */
export function randomNum(min, max) {
	let num = Math.floor(Math.random() * (min - max) + max);
	return num;
}

/**
 * @description 获取当前时间
 * @return string
 */
export function getTimeState() {
	// 获取当前时间
	let timeNow = new Date();
	// 获取当前小时
	let hours = timeNow.getHours();
	// 判断当前时间段
	if (hours >= 6 && hours <= 10) return `早上好 ⛅`;
	if (hours >= 10 && hours <= 14) return `中午好 🌞`;
	if (hours >= 14 && hours <= 18) return `下午好 🌞`;
	if (hours >= 18 && hours <= 24) return `晚上好 🌛`;
	if (hours >= 0 && hours <= 6) return `凌晨好 🌛`;
}

/**
 * @description 获取浏览器默认语言
 * @return string
 */
export function getBrowserLang() {
	let browserLang = navigator.language ? navigator.language : navigator.browserLanguage;
	let defaultBrowserLang = '';
	if (browserLang.toLowerCase() === 'cn' || browserLang.toLowerCase() === 'zh' || browserLang.toLowerCase() === 'zh-cn') {
		defaultBrowserLang = 'zh';
	} else {
		defaultBrowserLang = 'en';
	}
	return defaultBrowserLang;
}

/**
 * @description 递归查询当前路由所对应的路由
 * @param {Array} menuList 所有菜单列表
 * @param {String} path 当前访问地址
 * @return array
 */
export function filterCurrentRoute(menuList, path) {
	let result = {};
	for (let item of menuList) {
		if (item.path === path) return item;
		if (item.children) {
			const res = filterCurrentRoute(item.children, path);
			if (Object.keys(res).length) result = res;
		}
	}
	return result;
}

/**
 * @description 扁平化数组对象(主要用来处理路由菜单)
 * @param {Array} menuList 所有菜单列表
 * @return array
 */
export function getFlatArr(menulist) {
	return menulist.reduce((pre, current) => {
		let flatArr = [...pre, current];
		if (current.children) flatArr = [...flatArr, ...getFlatArr(current.children)];
		return flatArr;
	}, []);
}

/**
 * @description 使用递归，过滤需要缓存的路由
 * @param {Array} menuList 所有菜单列表
 * @param {Array} cacheArr 缓存的路由菜单 name ['**','**']
 * @return array
 * */
export function getKeepAliveRouterName(menuList, keepAliveArr = []) {
	menuList.forEach(item => {
		item.meta.isKeepAlive && item.name && keepAliveArr.push(item.name);
		item.children?.length && getKeepAliveRouterName(item.children, keepAliveArr);
	});
	return keepAliveArr;
}

/**
 * @description 使用递归，过滤出需要渲染在左侧菜单的列表（剔除 isHide == true 的菜单）
 * @param {Array} menuList 所有菜单列表
 * @return array
 * */
export function getShowMenuList(menuList) {
	let newMenuList = JSON.parse(JSON.stringify(menuList));
	return newMenuList.filter(item => {
		item.children?.length && (item.children = getShowMenuList(item.children));
		return !item.meta?.isHide;
	});
}

/**
 * @description 使用递归处理路由菜单 path，生成一维数组(第一版本地路由鉴权会用到)
 * @param {Array} menuList 所有菜单列表
 * @param {Array} menuPathArr 菜单地址的一维数组 ['**','**']
 * @return array
 */
export function getMenuListPath(menuList, menuPathArr = []) {
	menuList.forEach((item) => {
		typeof item === 'object' && item.path && menuPathArr.push(item.path);
		item.children?.length && getMenuListPath(item.children, menuPathArr);
	});
	return menuPathArr;
}

/**
 * @description 使用递归，过滤出当前路径匹配的面包屑地址
 * @param {String} path 当前访问地址
 * @param {Array} menuList 所有菜单列表
 * @returns array
 */
export function getCurrentBreadcrumb(path, menuList) {
	let tempPath = [];
	try {
		const getNodePath = (node) => {
			tempPath.push(node);
			if (node.path === path) throw new Error('Find IT!');
			if (node.children?.length) node.children.forEach(item => getNodePath(item));
			tempPath.pop();
		};
		menuList.forEach(item => getNodePath(item));
	} catch (e) {
		return tempPath;
	}
}

/**
 * @description 双重递归找出所有面包屑存储到 pinia/vuex 中
 * @param {Array} menuList 所有菜单列表
 * @returns array
 */
export function getAllBreadcrumbList(menuList) {
	let handleBreadcrumbList = {};
	const loop = (menuItem) => {
		if (menuItem?.children?.length) menuItem.children.forEach(item => loop(item));
		else handleBreadcrumbList[menuItem.path] = getCurrentBreadcrumb(menuItem.path, menuList);
	};
	menuList.forEach(item => loop(item));
	return handleBreadcrumbList;
}

/**
 * @description 格式化表格单元格默认值(el-table-column)
 * @param {Number} row 行
 * @param {Number} col 列
 * @param {String} callValue 当前单元格值
 * @return string
 * */
export function defaultFormat(row, col, callValue) {
	// 如果当前值为数组,使用 / 拼接（根据需求自定义）
	if (isArray(callValue)) return callValue.length ? callValue.join(' / ') : '--';
	return callValue ?? '--';
}

/**
 * @description 处理无数据情况
 * @param {String} callValue 需要处理的值
 * @return string
 * */
export function formatValue(callValue) {
	// 如果当前值为数组,使用 / 拼接（根据需求自定义）
	if (isArray(callValue)) return callValue.length ? callValue.join(' / ') : '--';
	return callValue ?? '--';
}

/**
 * @description 根据枚举列表查询当需要的数据（如果指定了 label 和 value 的 key值，会自动识别格式化）
 * @param {String} callValue 当前单元格值
 * @param {Array} enumData 枚举列表
 * @param {String} type 过滤类型（目前只有 tag）
 * @return string
 * */
export function filterEnum(callValue, enumData, searchProps, type) {
	const value = searchProps?.value ?? 'value';
	const label = searchProps?.label ?? 'label';
	let filterData = {};
	if (Array.isArray(enumData)) filterData = enumData.find((item) => item[value] === callValue);
	if (type == 'tag') return filterData?.tagType ? filterData.tagType : '';
	return filterData ? filterData[label] : '--';
}


export function isFalse(data){
	const allowData = [0,"0"]
	return ( !data && !allowData.includes(data) )
}

export function getDate(date, format= 'yyyy-MM-dd') {
    date = new Date(date)
    let year = (date.getFullYear()).toString()
    let month = (date.getMonth() + 1).toString()
    let day = (date.getDate()).toString()
    let hour = (date.getHours() + 1).toString()
    let min = (date.getMinutes()).toString()
    let sec = (date.getSeconds()).toString()
    if (month.length < 2) {
      month = '0' + month
    }
    if (day.length < 2) {
      day = '0' + day
    }
    if (hour.length < 2) hour = '0' + hour
    if (min.length < 2) min = '0' + min
    if (sec.length < 2) sec = '0' + sec
    if (format == 'yyyy-MM-dd') {
      return `${year}-${month}-${day}`
    }else {
      return `${year}-${month}-${day} ${hour}:${min}:${sec}`
    }

}

export function isJSON(str) {
    if (typeof str == 'string') {
        try {
            var obj=JSON.parse(str);
            if(typeof obj == 'object' && obj ){
                return true;
            }else{
                return false;
            }

        } catch(e) {
            console.log('error：'+str+'!!!'+e);
            return false;
        }
    }
}

export function getRandomNumber(num){
	return Math.floor((Math.random()+Math.floor(Math.random()*9+1))*Math.pow(10,num-1));
}


export function getRangeStr(prefix,num) {
	if (!prefix) {
		return getRandomNumber(num)
	} else {
		return `${prefix}${getRandomNumber(num)}`
	}
}

export function downloadBlob (blob, fileName) {
	try {
		const href = window.URL.createObjectURL(blob); //创建下载的链接
		if (window.navigator.msSaveBlob) {
			window.navigator.msSaveBlob(blob, fileName);
		} else {
			// 谷歌浏览器 创建a标签 添加download属性下载
			const downloadElement = document.createElement("a");
			downloadElement.href = href;
			downloadElement.target = "_blank";
			downloadElement.download = fileName;
			document.body.appendChild(downloadElement);
			downloadElement.click(); // 点击下载
			document.body.removeChild(downloadElement); // 下载完成移除元素
			window.URL.revokeObjectURL(href); // 释放掉blob对象
		}
	} catch (e) {
		console.log("下载失败");
	}
};

export async function doDownloadFile(url,name,callback) {
	let data = await fetch(url)
		.then((response) => response.blob())
		.then((res) => {
			console.log(res);
			let blod = new Blob([res]);
			downloadBlob(blod, name);
		});
	return data;
}
