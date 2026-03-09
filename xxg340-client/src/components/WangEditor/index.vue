<template>
	<div :class="['editor-box', disabled ? 'editor-disabled' : '']">
		<Toolbar class="editor-toolbar" :editor="editorRef" :defaultConfig="toolbarConfig" :mode="mode" v-if="!hideToolBar" />
		<Editor
			:style="{ height }"
			class="editor-content"
			v-model="valueHtml"
			:defaultConfig="editorConfig"
			:mode="mode"
			@on-created="handleCreated"
			@on-blur="handleBlur"
		/>
	</div>
</template>

<script setup name="wangEditor">
import { nextTick, computed, shallowRef, onBeforeUnmount, defineProps } from "vue";
import { Editor, Toolbar } from "@wangeditor/editor-for-vue";
import SystemService from "@/api/system";
import "@wangeditor/editor/dist/css/style.css";

// 富文本 DOM 元素
const editorRef = shallowRef();

// 实列化编辑器
const handleCreated = (editor) => {
	editorRef.value = editor;
};
// 
const props = defineProps({
	toolbarConfig: {
		type: Object,
		default: () => {
			return {
				excludeKeys: []
			}
		}
	},
	editorConfig: {
		type: Object,
		default: () => {
			return {
				placeholder: "请输入内容...",
				MENU_CONF: {}
			};
		},
	},
	height: {
		type: String,
		default: '500px',
	},
	mode: {
		type: String,
		default: 'default'
	},
	hideToolBar: {
		type: Boolean,
		default: false
	},
	disabled: {
		type: Boolean,
		default: false
	},
	value: {
		type: String,
		default: ''
	}

})

// 判断当前富文本编辑器是否禁用
if (props.disabled) nextTick(() => editorRef.value.disable());

// 富文本的内容监听，触发父组件改变，实现双向数据绑定
const emit = defineEmits(['update:value', 'check-validate']);
const valueHtml = computed({
	get() {
		return props.value;
	},
	set(val) {
		// 防止富文本内容为空时，校验失败
		if (editorRef.value.isEmpty()) val = "";
		emit("update:value", val);
	}
});

/**
 * @description 图片自定义上传
 * @param file 上传的文件
 * @param insertFn 上传成功后的回调函数（插入到富文本编辑器中）
 * uploadImage 必须存在
 * */
props.editorConfig.MENU_CONF["uploadImage"] = {
	async customUpload(file, insertFn) {
		if (!uploadImgValidate(file)) return;
		let formData = new FormData();
		formData.append("file", file);
		try {
			const data = await SystemService.uploadImg(formData);
			insertFn(data);
		} catch (error) {
			console.log(error);
		}
	}
};

// 图片上传前判断
const uploadImgValidate = (file) => {
	console.log(file);
	return true;
};

/**
 * @description 视频自定义上传
 * @param file 上传的文件
 * @param insertFn 上传成功后的回调函数（插入到富文本编辑器中）
 * uploadVideo 必须存在
 * */

props.editorConfig.MENU_CONF["uploadVideo"] = {
	async customUpload(file, insertFn) {
		if (!uploadVideoValidate(file)) return;
		let formData = new FormData();
		formData.append("file", file);
		try {
			const { data } = await SystemService.uploadVideo(formData);
			insertFn(data.fileUrl);
		} catch (error) {
			console.log(error);
		}
	}
};

// 视频上传前判断
const uploadVideoValidate = (file) => {
	console.log(file);
	return true;
};

// 编辑框失去焦点时触发
const handleBlur = () => {
	emit("check-validate");
};

// 组件销毁时，也及时销毁编辑器
onBeforeUnmount(() => {
	if (!editorRef.value) return;
	editorRef.value.destroy();
});

defineExpose({
	editor: editorRef
});
</script>

<style scoped lang="scss">
@import "./index.scss";

</style>
