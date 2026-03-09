<template>
    <el-form :model="props.registerForm" label-width="120px">
        <el-form-item label="用户名">
          <el-input v-model="props.registerForm.user_name"   autocomplete="off"></el-input>
        </el-form-item>
        <el-form-item label="头像">
           <UploadImg id="avatar1" v-model:imageUrl="props.registerForm.avatar" />
        </el-form-item>
       
        <el-form-item :label="'手机号'">
          <el-input v-model="props.registerForm.phone" autocomplete="off"></el-input>
        </el-form-item>
        <el-form-item label="邮箱">
          <el-input v-model="props.registerForm.email" autocomplete="off"></el-input>
        </el-form-item>
        <el-form-item label="密码" v-if="showPassword">
          <el-input v-model="props.registerForm.password" placeholder="" autocomplete="off"></el-input>
        </el-form-item>
      </el-form>
</template>
<script setup name="UserInfo">
import UploadImg from "@/components/UploadImg/index.vue";
import { GlobalStore } from "@/stores";

const globalStore = GlobalStore();
const props = defineProps({
    registerForm: {
        type: Object
    },
    showPassword: {
      type: Boolean,
      default: true
    }
})
</script>
<style lang="css" scoped>

</style>