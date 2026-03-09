<template>
  <el-upload
    drag
    multiple
    class="upload-demo"
    action="#"
    v-model:file-list="fileList"
    :http-request="handleHttpUpload"
    :on-success="uploadSuccess"
    :on-error="uploadError"
	:on-preview="previewFile"
  >
    <el-icon class="el-icon--upload"><upload-filled /></el-icon>
    <div class="el-upload__text">
      拖拽文件 或者 <em>点击上传</em>
    </div>
  </el-upload>
</template>

<script lang="ts" setup>
import { ref, computed } from "vue";
import { ElNotification } from "element-plus";
import { Plus } from '@element-plus/icons-vue'
import SystemService from "@/api/system";
import type { UploadProps, UploadUserFile } from 'element-plus'
// 国际化函数
import app from '@/main.js'

// 接受父组件参数
const props = defineProps({
	fileUrl: {
		type: String,
		default:'[]'
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


const fileList = computed(()=>{
	console.log("props.fileUrl",props.fileUrl)
	return  typeof props.fileUrl == 'object' ? props.fileUrl : JSON.parse(props.fileUrl || "[]")
})


const dialogfileUrl = ref('')
const fileUrlList = ref([])
const deleteUrl = ref([])
const handleRemove: UploadProps['onRemove'] = (uploadFile, uploadFiles) => {
  console.log(uploadFile, uploadFiles)
}



const emit = defineEmits(['update:fileUrl', 'check-validate'])


const handleHttpUpload = async (options) => {
	let formData = new FormData();
	formData.append("file", options.file);
	try {
		const data = await SystemService.uploadImg(formData);
		let fileArr = typeof props.fileUrl == 'object' ? props.fileUrl : JSON.parse(props.fileUrl || '[]')
		fileArr.push({name:options.file.name ,url: data})
    	fileUrlList.value = fileArr.filter(item=>!deleteUrl.value.includes(item.url))
		emit("update:fileUrl", JSON.stringify(fileUrlList.value));
		emit("check-validate");
	} catch (error) {
    console.log("error",error)
		options.onError(error);
	}
};


const beforeRemove = (e) => {
  	deleteUrl.value.push(e.url)
	let fileArr = typeof props.fileUrl == 'object' ? props.fileUrl : JSON.parse(props.fileUrl || '[]')
	const image = fileArr.filter(item=>!deleteUrl.value.includes(item.url))
	emit("update:fileUrl", JSON.stringify(image));
	return false
}



const uploadSuccess = () => {
	ElNotification({
		title: '提示',
		message: '上传成功',
		type: "success"
	});
};


// 图片上传错误提示
const uploadError = () => {
	ElNotification({
		title: '提示',
		message: '上传失败',
		type: "error"
	});
};



const previewFile = (e) => {
	window.open(e.url)
}
</script>

<style scoped>
.upload-demo {
    min-width: 300px;
}
</style>