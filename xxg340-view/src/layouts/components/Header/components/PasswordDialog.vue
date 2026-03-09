<template>
	<el-dialog v-model="dialogVisible" title="修改密码" width="500px" draggable>
		<el-form>
			<el-form-item prop="username">
				<el-input v-model="passwordForm.password" placeholder="请输入密码"  show-password autocomplete="new-password">
		
				</el-input>
			</el-form-item>
			<el-form-item prop="password">
				<el-input type="password" v-model="passwordForm.confirmPassword" 
				placeholder="请再次输入密码" show-password autocomplete="new-password">
			
				</el-input>
			</el-form-item>
		</el-form>
		<template #footer>
			<span class="dialog-footer">
				<el-button @click="dialogVisible = false">取消</el-button>
				<el-button type="primary" @click="sure">确定</el-button>
			</span>
		</template>
	</el-dialog>
</template>

<script setup>
import { ref,  } from 'vue';
import { request } from '@/http/index';
import { GlobalStore } from "@/stores";
import { ElMessage } from 'element-plus'
const globalStore = GlobalStore();
const dialogVisible = ref(false);
const passwordForm = ref({
	password: '',
	confirmPassword: '',
	userId: globalStore.userInfo.id,
	id: globalStore.userInfo.id,
})
// openDialog
const openDialog = () => {
	dialogVisible.value = true;
};

const sure = () => {
	if (passwordForm.value.password != passwordForm.value.confirmPassword) {
		ElMessage({ message: '两次密码不一致', type: 'warning' })
	} else {
		request('/ucuser/resetPassword', passwordForm.value, 'post').then(res => {
			ElMessage({ message: '修改成功', type: 'success' })
			dialogVisible.value = false
		})
	}
}

defineExpose({ openDialog });
</script>
