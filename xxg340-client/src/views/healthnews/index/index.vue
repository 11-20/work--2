<template>
  <div class="health-news-container">
    <div class="header">
      <h1>健康资讯</h1>
      <p>了解心血管健康，掌握科学预防知识</p>
    </div>

    <div class="news-grid">
      <div
        v-for="item in newsList"
        :key="item.id"
        class="news-card"
        @click="goToDetail(item.id)"
      >
        <div class="card-image" v-if="item.hn_cover">
          <img :src="item.hn_cover" alt="资讯封面" />
        </div>
        <div class="card-content">
          <h3 class="title">{{ item.hn_title }}</h3>
          <p class="excerpt">{{ item.hn_excerpt }}</p>
          <div class="meta">
            <span class="date">{{ item.cd }}</span>
          </div>
        </div>
      </div>
    </div>

    <!-- 分页区域（如果需要） -->
    <!-- 此处根据需求可添加分页，但题目未明确要求，暂不实现 -->
  </div>
</template>

<script setup lang="ts">
import {
  ref,
  onMounted
} from 'vue';

import { request } from "@/http/index";
import { GlobalStore } from "@/stores";
import { useRoute, useRouter } from "vue-router";

const router = useRouter();
const route = useRoute();
const globalStore = GlobalStore();

const newsList = ref([]);

const goToDetail = (id) => {
  router.push({ path: '/healthnews/detail', query: { id } });
};

onMounted(async () => {
  const res = await request('/healthnews/index', {}, 'get');
  newsList.value = res.data;
});
</script>

<style scoped>
.health-news-container {
  padding: 2rem;
  background: #f9fbfd;
  min-height: 100vh;
}

.header {
  text-align: center;
  margin-bottom: 2.5rem;
}

.header h1 {
  font-size: 2.25rem;
  font-weight: 700;
  color: #1a56db;
  margin-bottom: 0.5rem;
}

.header p {
  font-size: 1.125rem;
  color: #4b5563;
  max-width: 600px;
  margin: 0 auto;
}

.news-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(320px, 1fr));
  gap: 1.5rem;
}

.news-card {
  background: white;
  border-radius: 16px;
  overflow: hidden;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
  transition: transform 0.3s ease, box-shadow 0.3s ease;
  cursor: pointer;
  display: flex;
  flex-direction: column;
  height: 100%;
}

.news-card:hover {
  transform: translateY(-6px);
  box-shadow: 0 8px 20px rgba(26, 86, 219, 0.15);
}

.card-image img {
  width: 100%;
  height: 180px;
  object-fit: cover;
  display: block;
}

.card-content {
  padding: 1.25rem;
  flex: 1;
  display: flex;
  flex-direction: column;
}

.title {
  font-size: 1.25rem;
  font-weight: 600;
  color: #1e293b;
  margin-bottom: 0.75rem;
  line-height: 1.4;
}

.excerpt {
  font-size: 0.95rem;
  color: #475569;
  line-height: 1.6;
  flex: 1;
  display: -webkit-box;
  -webkit-line-clamp: 3;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.meta {
  margin-top: 1rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.date {
  font-size: 0.875rem;
  color: #64748b;
  background: #f1f5f9;
  padding: 0.25rem 0.5rem;
  border-radius: 20px;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .health-news-container {
    padding: 1.25rem;
  }

  .header h1 {
    font-size: 1.75rem;
  }

  .news-grid {
    grid-template-columns: 1fr;
    gap: 1.25rem;
  }

  .card-image img {
    height: 160px;
  }
}
</style>