<template>
  <el-upload
    action="#"
    v-model:file-list="fileList"
    list-type="picture-card"
    :http-request="handleHttpUpload"
    :on-success="uploadSuccess"
    :on-error="uploadError"
    :before-remove="beforeRemove"
      :on-preview="handlePictureCardPreview"
    accept="image/jpeg,image/jpeg,image/png"
  >
    <el-icon><Plus /></el-icon>
  </el-upload>

  <el-dialog v-model="dialogVisible">
    <img w-full style="width:100%" :src="dialogImageUrl" alt="Preview Image" />
  </el-dialog>
</template>

<script lang="ts" setup>
import { ref, computed } from "vue";
import { ElNotification } from "element-plus";
import { Plus } from '@element-plus/icons-vue'
import SystemService from "@/api/system";
import type { UploadProps, UploadUserFile } from 'element-plus'
import app from '@/main.js'

// 接受父组件参数
const props = defineProps({
	imageUrl: {
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
	console.log("props.imageUrl",props.imageUrl)
	return  typeof props.imageUrl == 'object' ? props.imageUrl : JSON.parse(props.imageUrl || "[]")
  
})



const dialogImageUrl = ref('')
const imageList = ref([])
const deleteUrl = ref([])
const handleRemove: UploadProps['onRemove'] = (uploadFile, uploadFiles) => {
  console.log(uploadFile, uploadFiles)
}

const handlePictureCardPreview: UploadProps['onPreview'] = (uploadFile) => {
  dialogImageUrl.value = uploadFile.url!
  dialogVisible.value = true
}

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
		const data = await SystemService.uploadImg(formData);
		let imageArr = typeof props.imageUrl == 'object' ? props.imageUrl : JSON.parse(props.imageUrl || '[]')
		imageArr.push({url: data})
    	imageList.value = imageArr.filter(item=>!deleteUrl.value.includes(item.url))
		emit("update:imageUrl", JSON.stringify(imageList.value));
		emit("check-validate");
	} catch (error) {
    console.log("error",error)
		options.onError(error);
	}
};


const beforeRemove = (e) => {
  	deleteUrl.value.push(e.url)
	let imageArr = typeof props.imageUrl == 'object' ? props.imageUrl : JSON.parse(props.imageUrl || '[]')
	const image = imageArr.filter(item=>!deleteUrl.value.includes(item.url))
	emit("update:imageUrl", JSON.stringify(image));
	return false
}

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
		title:"提示",
		message: "上传成功",
		type: "success"
	});
};

// 图片上传错误提示
const uploadError = () => {
	ElNotification({
		title:"提示",
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
