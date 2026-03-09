<template>
  <div class="healthnews-detail-container">
    <div class="content-wrapper">
      <!-- 返回按钮 -->
      <div class="back-button" @click="goBack">
        <img src="https://cdn-icons-png.flaticon.com/512/2223/2223615.png" alt="返回" />
        <span>返回资讯列表</span>
      </div>

      <!-- 资讯标题 -->
      <h1 class="news-title">{{ healthNews.hn_title }}</h1>

      <!-- 封面图（如果存在） -->
      <div v-if="healthNews.hn_cover" class="cover-image">
        <img :src="healthNews.hn_cover" alt="资讯封面" />
      </div>

      <!-- 资讯内容 -->
      <div class="news-content" v-html="healthNews.hn_content"></div>
    </div>
  </div>
</template>

<script setup lang="ts">
// 固定引入只能增加不能减少
import { 
  ref, 
  reactive, 
  onMounted, 
  onUpdated, 
  onBeforeUnmount, 
  computed, 
  watch, 
  watchEffect, 
  provide, 
  inject, 
  nextTick 
} from 'vue';

import { request } from "@/http/index";
import { GlobalStore } from "@/stores";
import { useRoute, useRouter } from "vue-router";
import { ElMessage, ElMessageBox } from 'element-plus'
import * as echarts from "echarts"; // echarts图表 需要时直接使用
import "@/utils/echarts-wordcloud.min.js" // 词云图组件，有词云图组件在引入

const router = useRouter();
const route = useRoute();
const globalStore = GlobalStore();

/**
全局组件可直接使用：
富文本编辑：<WangEditor height="400px" v-model:value="字段名称" />
单图上传：<UploadImg  v-model:imageUrl="字段名称" />
多图上传：<UploadManyImg  v-model:imageUrl="字段名称" />
文件上传： <UploadFile  v-model:fileUrl="字段名称" />
*/

const userInfo = globalStore.userInfo

const healthNews = ref({
  hn_title: '',
  hn_excerpt: '',
  hn_content: '',
  hn_cover: ''
})

const goBack = () => {
  router.push({ path: '/healthnews', query: {} })
}

onMounted(async () => {
  const id = route.query.id;
  if (!id) {
    ElMessage.error('缺少资讯ID');
    router.push('/healthnews');
    return;
  }

  const res = await request('/healthnews/show', {
    id: id
  }, 'get');
  
  healthNews.value = res;
});
</script>

<style scoped>
.healthnews-detail-container {
  background-color: #f9f9f9;
  min-height: 100vh;
  padding: 20px;
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
}

.content-wrapper {
  max-width: 800px;
  margin: 0 auto;
  background: white;
  border-radius: 12px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
  padding: 40px;
  position: relative;
}

.back-button {
  display: flex;
  align-items: center;
  gap: 8px;
  color: #409eff;
  font-size: 14px;
  cursor: pointer;
  width: fit-content;
  margin-bottom: 24px;
  transition: opacity 0.2s;
}

.back-button:hover {
  opacity: 0.8;
}

.back-button img {
  width: 16px;
  height: 16px;
}

.news-title {
  font-size: 28px;
  font-weight: 700;
  color: #333;
  margin-bottom: 24px;
  line-height: 1.4;
}

.cover-image {
  margin: 24px 0;
  text-align: center;
}

.cover-image img {
  max-width: 100%;
  height: auto;
  border-radius: 8px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
}

.news-content {
  font-size: 16px;
  line-height: 1.8;
  color: #444;
  word-wrap: break-word;
}

.news-content p {
  margin: 16px 0;
  text-align: justify;
}

.news-content img {
  max-width: 100%;
  height: auto;
  display: block;
  margin: 20px auto;
  border-radius: 6px;
}

.news-content h2,
.news-content h3 {
  margin: 24px 0 16px;
  color: #2c3e50;
}

.news-content ul,
.news-content ol {
  margin: 16px 0;
  padding-left: 24px;
}

.news-content li {
  margin: 8px 0;
}
</style>