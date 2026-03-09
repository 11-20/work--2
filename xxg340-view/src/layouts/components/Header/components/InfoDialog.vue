<template>
	<el-dialog v-model="dialogVisible" :title="'个人信息'" width="700px" draggable>
		 <UserInfo :registerForm="registerForm" :showPassword="false" />
		  <template #footer class="dialog-footer">
			<el-button type="primary" @click="doUpdateUser">确定</el-button>
      	</template>
	</el-dialog>
</template>

<script setup>
import { ref,reactive } from "vue";
import { request } from '@/http/index';
import UserInfo from "@/components/UserInfo/index.vue";
import { GlobalStore } from "@/stores";
import { ElMessage } from 'element-plus'
const globalStore = GlobalStore();


const registerForm = reactive({
    openId:"",
    user_name:  globalStore.userInfo.user_name,
    phone: globalStore.userInfo.phone, // 随机用户名防止重复
    sex: globalStore.userInfo.sex,
    strRoleId: globalStore.userInfo.userRoleList,
    email:  globalStore.userInfo.email,
    organId: null,
    isEmployee: 1,
    status: 1,
    roleNames: "",
    isSuper: globalStore.userInfo.isSuper,
    password:"",
    avatar: globalStore.userInfo.avatar,
	userId: globalStore.userInfo.id,
	id: globalStore.userInfo.id,
})

const dialogVisible = ref(false);

// openDialog
const openDialog = () => {
	dialogVisible.value = true;
};
defineExpose({ openDialog });

const doUpdateUser = () => {
  	request('/ucuser/updateUser', registerForm, 'post').then(res => {
		globalStore.setUserInfo(registerForm)
        ElMessage({ message: '更新成功', type: 'success' })
    })
}

</script>
