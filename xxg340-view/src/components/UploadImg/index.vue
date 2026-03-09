<template>
	<div class="upload-box">

		<el-upload
			action="#"
			:id="id"
			:class="['upload']"
			:multiple="false"
			:disabled="disabled"
			:show-file-list="false"
			:http-request="handleHttpUpload"
			:on-success="uploadSuccess"
			:on-error="uploadError"
			:style="uploadStyle"
			:drag="drag"
			accept="image/jpeg,image/jpeg,image/png"
		>
			<img v-if="imageUrl" :src="imageUrl" class="upload-image" />
			<el-icon v-else class="upload-icon"><Plus /></el-icon>
			<div v-if="imageUrl" class="upload-handle" @click.stop>
				<div class="handle-icon" @click="editImg" v-if="!disabled">
					<el-icon><Edit /></el-icon>
					<span>编辑</span>
				</div>
				<div class="handle-icon" @click="imageView">
					<el-icon><ZoomIn /></el-icon>
					<span>查看</span>
				</div>
				<div class="handle-icon" @click="deleteImg" v-if="!disabled">
					<el-icon><Delete /></el-icon>
					<span>删除</span>
				</div>
			</div>
		</el-upload>
		<div class="el-upload__tip">
			<slot name="tip"></slot>
		</div>
		<el-image-viewer v-if="dialogVisible" @close="imageView" :url-list="[imageUrl]" />
	</div>
</template>

<script setup name="uploadImg">
import { ref } from "vue";
import { ElNotification } from "element-plus";
import { Plus } from "@element-plus/icons-vue";
import SystemService from "@/api/system";
import app from '@/main.js'

// 接受父组件参数
const props = defineProps({
	imageUrl: {
		type: String,
		default:''
	},
	id: {
		type: String,
		default: 'upload',
	},
	drag: {
		type: Boolean,
		default: true
	},
	disabled: {
		type: Boolean,
		default: false
	},
	fileSize: {
		type: Number,
		default: 5,
	},
	uploadStyle: {
		type: Object,
		default: () => ({ width: "175px", height: "175px" })
	}
})

const emit = defineEmits(['update:imageUrl', 'check-validate'])

/**
 * @description 图片上传
 * @param options 上传的文件
 * 
 * */
const handleHttpUpload = async (options) => {
	let formData = new FormData();
	formData.append("file", options.file);
	try {
		const  data  = await SystemService.uploadImg(formData);
		console.log("datais",data)
		emit("update:imageUrl", data);
		emit("check-validate");
	} catch (error) {
		options.onError(error);
	}
};

/**
 * @description 删除图片
 * */
const deleteImg = () => {
	emit("update:imageUrl", "");
};

/**
 * @description 编辑图片
 * */
const editImg = () => {
	const dom = document.querySelector(`#${props.id} .el-upload__input`);
	dom?.dispatchEvent(new MouseEvent("click"));
};



// 图片上传成功提示
const uploadSuccess = () => {
	ElNotification({
		title: "提示",
		message: "上传成功",
		type: "success"
	});
};

// 图片上传错误提示
const uploadError = () => {
	ElNotification({
		title: "提示",
		message: "上传失败",
		type: "error"
	});
};

// 查看图片
const dialogVisible = ref(false);
const imageView = () => {
	dialogVisible.value = !dialogVisible.value;
};
</script>

<style scoped lang="scss">
@import "./index.scss";
</style>
