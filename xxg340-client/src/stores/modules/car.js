import { defineStore } from 'pinia';
import UserService from '@/api/user';
import { getKeepAliveRouterName, getShowMenuList, getAllBreadcrumbList } from '@/utils/util';
import piniaPersistConfig from '@/config/piniaPersist';

// CarStore
export const CarStore = defineStore({
	id: 'CarState',
	state: () => ({
        list:[],
		//选中商品_id
		selectedList:[]
	}),
	getters: {
		//是否全选
		selectAll:(state)=>{
			return state.list.length === state.selectedList.length
		},
		//合计价格
		countPrice:(state)=>{
			let total = 0
			state.list.forEach(v=>{
                console.log("v",v)
				if(state.selectedList.indexOf(v.id)>-1){
					total+=Number(v.price) * Number(v.num)
				}
			})
			return total
		},
		// 已经选中的商品
		selectGoods:(state)=>{
			return state.list.filter(item=>{
				if(item.checked){
					return item
				}
			})
		},
		// 统计所有价格，包含选中与未选中
		countAllPrice:(state)=>{
			let total = 0
			state.list.forEach(v=>{
				total+=v.price*v.num
			})
			return total
		},
		//合计商品
		countCar:(state)=>{
			let arr = state.list.map(function(item){
			    return item.num;
			})
			if(arr.length==0)return
			let res = arr.reduce(function(tem,item,index){
			    return tem+item;
			})
			return res
		},
		//禁止全选
		disabledAll:(state)=>{
			return state.list.length === 0
		}
	},
	actions: {
		// 购物车选择
		selectCar(ids) {
            this.selectedList = ids
            this.list.forEach(item=>{
                if (ids.includes(item.id)) {
                    item.checked = true
                } else {
                    item.checked = false
                }
            })
		},
		//添加购物车
		doAddCar(item) {
			let goods = this.list.find(car=>{
				return car.id == item.id
			})
			if(!goods){
				this.list.push({
					checked:false,
					id:item.id,
					title:item.title,
					cover:item.cover,
					price:item.price,
					business_id:item.business_id,
					num:item.num || 1,
					minnum:1,
					maxnum:item.max,
					excerpt:item.excerpt,
					level: item.level
				})
			}else{
				goods.num = goods.num + item.num
			}
			console.log(this.list)
		},
		//删除选中商品
		delGoods(){
			this.list = this.list.filter(v=>{
				return this.selectedList.indexOf(v.id)===-1
			})
		},
		delGoodsById(id){
			this.list = this.list.filter(v=>{
				return v.id != id
			})
		},
		//全选
		doSelectAll(){
			this.selectedList = this.list.map(v=>{
				v.checked = true
				return v.id
			})
		},
		//取消全选
		unselectAll(){
			this.selectedList = []
			this.list.forEach(v=>{
				v.checked = false
			})
		},
		updateCar(items){
			items.forEach(item=>{
				let obj =  {
					checked:false,
					id:item.goods_id,
					name:item.name,
					cover:item.cover,
					business_id:item.business_id,
					price:item.price,
					num:item.num,
					minnum:1,
					maxnum:item.max,
					excerpt:item.excerpt	
			    }
			    this.list.push(obj)
			})
		},
		clearGoods(){
			this.list = []
			this.selectedList = []
		},
		findGoods(id){
			let goods = null
			this.list.some(item=>{
				if(item.id == id){
					goods = item
                    return true
				}
			})
			return goods
		}
	},
    persist: piniaPersistConfig('GlobalState')
});



