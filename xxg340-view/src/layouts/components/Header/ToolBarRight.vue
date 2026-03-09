<template>
	<div class="tool-bar-ri">
		<Avatar />
	</div>
</template>

<script setup>
import Language from "./components/Language.vue";
import SearchMenu from './components/SearchMenu.vue';
import Fullscreen from './components/Fullscreen.vue';
import ThemeSetting from './components/ThemeSetting.vue';
import Avatar from './components/Avatar.vue';
</script>

<style scoped lang="scss">
.tool-bar-ri {
	display: flex;
	align-items: center;
	justify-content: center;
	margin: 0 30px;
}
.header-icon {
	display: flex;
	align-items: center;
	justify-content: space-between;
	margin-right: 22px;
	width: 140px;
}
.header-icon:nth-child(1) {
	margin-right: 20px;
}
</style>
