<template>
	<el-config-provider  :key="$route.fullPath" :button="config" :size="assemblySize" :locale="zhCn">
		<router-view></router-view>
	</el-config-provider>
</template>

<script setup>
import { reactive, computed } from 'vue';
import { GlobalStore } from '@/stores';
import zhCn from '@/lang/zh-cn.js'

const globalStore = GlobalStore();
// 配置element按钮文字中间是否有空格
const config = reactive({
	autoInsertSpace: false
});


// 配置全局组件大小 (small/default(medium)/large)
const assemblySize = computed(() => globalStore.assemblySize);
</script>

<style  lang="scss">
:root {
	--main-color:#06c;
	--main-color-light-1: #1975d1;
	--main-color-light-2:  #3384d6;
	--main-color-light-3: #4c93db;
	--main-color-light-4: #66a3e0;
	--main-color-light-5: #7fb2e5;
	--main-color-light-6: #99c1ea;
	--main-color-light-7: #b2d1ef;
	--main-color-light-8: #cce0f4;
	--main-color-light-9: #e5eff9;
}
.el-menu-item:hover{ 
	background: var(--main-color-light-1)!important;
}

// :deep(input[type=text], input[type=email],input[type=number]){ 
//     border:none!important;
//     height: initial!important;
//     padding:0!important
// }
</style>
