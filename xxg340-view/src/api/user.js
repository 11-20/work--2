import { request } from '@/http/index';
import DynamicRouter from "@/assets/json/dynamicRouter.js";
import { ElMessage, ElMessageBox } from 'element-plus'

/**
 * 根据角色id得出相关菜单
 * @param {*} roleId 
 * @param {*} rolesData 
 * @returns 
 */
const findRoleMenuById = (roleId, rolesData) => {
  const addMenuProperties = (menus, parentId = null) => {
    return menus.map((menu, index) => {
      const customId = parentId ? `${parentId}-${index + 1}` : `${index + 1}`; 
      const updatedMenu = {
        ...menu, 
        meta: {
          title: menu.name,
          isLink: "",
          isHide: false,
          isFull: false,
          isAffix: true,
          isKeepAlive: true
        }
      };
      if (!updatedMenu.component) {
        updatedMenu.component = updatedMenu.path;
      }
      if (!updatedMenu.path) {
        updatedMenu.path = `/${customId}`;
      }
      if (!updatedMenu.hasOwnProperty('children')) {
        updatedMenu.children = [];
      }
      if (updatedMenu.children && updatedMenu.children.length > 0) {
        updatedMenu.children = addMenuProperties(updatedMenu.children, customId);
      }
      const filteredMenu = {
        id: customId,  
        name: updatedMenu.name,
        meta: updatedMenu.meta,
        children: updatedMenu.children,
        path: updatedMenu.path,
        component: updatedMenu.component
      };
      return filteredMenu;
    });
  };

  for (const roleKey in rolesData) {
    if (rolesData[roleKey].roleId == roleId) {
      const menusWithProperties = addMenuProperties(rolesData[roleKey].menus);
      return menusWithProperties;
    }
  }
  return null; 
};


export default class UserService {
  static async getMenuList(params) {
    const userInfo = (JSON.parse( localStorage.getItem("AdminGlobalState")))?.userInfo
    const sysset = false
    const roleId = userInfo.role_id
    const men = findRoleMenuById(roleId,DynamicRouter)
    const menuData = men//JSON.parse(localStorage.getItem("menuData"))
    console.log("menudata",menuData)
    if (!menuData) {
       ElMessage.error('无权限！');
    }
    
    if (sysset) {
  menuData.push({
      "path": "/sys/index",
      "name": "系统设置1",
      meta:{
        isKeepAlive:false,
      },
      children: [
        {
          "path":"/sys/logs",
          component:'/sys/logs',
          name:"系统日志",
            meta:{
        isKeepAlive:false,
      },
        },
         {
          "path":"/sys/settings",
             component:'/sys/settings',
          name:"系统参数",
            meta:{
        isKeepAlive:false,
      },
        },
         {
          "path":"/sys/backup",
             component:'/sys/backup',
          name:"数据备份",
            meta:{
        isKeepAlive:false,
      },
        }
      ]
    })
    }
  
    const data = {
      "code": 200,
      "data": menuData
    }
    return data;
  }
  static async getUserData(params) {
    return request('/user/data', params, 'get')
  }
}
