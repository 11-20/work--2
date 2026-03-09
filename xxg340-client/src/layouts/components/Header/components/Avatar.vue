<template>
	<el-dropdown trigger="click">
		<div class="user-msg">
			<span class="username">{{ globalStore.userInfo.user_name }}</span>
			<div class="avatar" v-if="globalStore.userInfo.avatar">
				<img :src="globalStore.userInfo.avatar" alt="avatar" />
			</div>
		</div>
		<template #dropdown>
			<el-dropdown-menu>
				<el-dropdown-item @click="openDialog('passwordRef')">
					修改密码
				</el-dropdown-item>
				<el-dropdown-item @click="toEdit">
					个人设置
				</el-dropdown-item>
				<el-dropdown-item @click="logout">
					注销
				</el-dropdown-item>
			</el-dropdown-menu>
			
		</template>
	</el-dropdown>

	<!-- infoDialog -->
	<InfoDialog ref="infoRef"></InfoDialog>
	<!-- passwordDialog -->
	<PasswordDialog ref="passwordRef"></PasswordDialog>
</template>

<script setup >
import { ref } from "vue";
import { useRouter } from "vue-router";
import { GlobalStore } from "@/stores";
import { LOGIN_URL } from "@/config/config";
import { ElMessageBox, ElMessage } from "element-plus";
import InfoDialog from "./InfoDialog.vue";
import PasswordDialog from "./PasswordDialog.vue";

const router = useRouter();
const globalStore = GlobalStore();

const toEdit = () => {
	router.push('/user/edit')
}
// 退出登录
const logout = () => {
	router.replace(LOGIN_URL);
	globalStore.setToken("");
	localStorage.removeItem("menuData")

};


const infoRef = ref(null);
const passwordRef = ref(null);
// 打开修改密码和个人信息弹窗
const openDialog = (refName) => {
	if (refName == "infoRef") return infoRef.value?.openDialog();
	passwordRef.value?.openDialog();
};
</script>

<style scoped lang="scss">
.user-msg {
	display: flex;
	align-items: center;
}
.avatar {
	display: inline-block;
	width: 40px;
	height: 40px;
	overflow: hidden;
	cursor: pointer;
	border-radius: 50%;
	margin-left: 10px;
	
}
.avatar img {
	width: 100%;
	height: 100%;
}
</style>
