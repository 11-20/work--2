<template>
  <div class="home-container">
    <!-- 轮播图区域 -->
    <div class="carousel-section">
      <div class="carousel-wrapper" ref="carouselRef">
        <div
          class="carousel-item"
          v-for="(item, index) in carouselList"
          :key="item.id"
          :class="{ active: currentIndex == index }"
        >
          <img :src="item.ca_cover" :alt="item.ca_title" />
          <div class="carousel-overlay">
            <h2>{{ item.ca_title }}</h2>
            <p>{{ item.ca_excerpt }}</p>
          </div>
        </div>
      </div>
      <div class="carousel-indicators">
        <span
          v-for="(item, index) in carouselList"
          :key="item.id"
          @click="setCurrentIndex(index)"
          :class="{ active: currentIndex == index }"
        ></span>
      </div>
    </div>

    <!-- 健康资讯区域 -->
    <div class="healthnews-section">
      <h3 class="section-title">最新健康资讯</h3>
      <div class="news-grid">
        <div
          v-for="news in healthNewsList"
          :key="news.id"
          class="news-card"
          @click="goToDetail(news.id)"
        >
          <div class="news-cover">
            <img :src="news.hn_cover" :alt="news.hn_title" />
          </div>
          <div class="news-content">
            <h4>{{ news.hn_title }}</h4>
            <p class="excerpt">{{ news.hn_excerpt }}</p>
            <div class="news-meta">
              <span>{{ news.cd }}</span>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- 健康统计汇总区域 -->
    <div class="healthsummary-section">
      <h3 class="section-title">健康统计汇总</h3>
      <div class="summary-cards">
        <div class="summary-card" v-for="summary in healthSummaryList" :key="summary.id">
          <div class="summary-header">
            <h4>{{ summary.hs_type }} - {{ summary.hs_date }}</h4>
          </div>
          <div class="summary-stats">
            <div class="stat-item">
              <span class="label">平均BMI</span>
              <span class="value">{{ summary.hs_avgbmi }}</span>
            </div>
            <div class="stat-item">
              <span class="label">平均收缩压</span>
              <span class="value">{{ summary.hs_avgsbp }}</span>
            </div>
            <div class="stat-item">
              <span class="label">平均舒张压</span>
              <span class="value">{{ summary.hs_avgdbp }}</span>
            </div>
            <div class="stat-item">
              <span class="label">平均总胆固醇</span>
              <span class="value">{{ summary.hs_avgchol }}</span>
            </div>
            <div class="stat-item">
              <span class="label">高风险比例</span>
              <span class="value">{{ summary.hs_highriskrate }}%</span>
            </div>
            <div class="stat-item">
              <span class="label">正常指标比例</span>
              <span class="value">{{ summary.hs_normalrate }}%</span>
            </div>
          </div>
          <div class="chart-container" ref="chartRefs" :data-id="summary.id"></div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import {
  ref,
  onMounted,
  nextTick
} from 'vue';

import { request } from "@/http/index";
import { GlobalStore } from "@/stores";
import { useRoute, useRouter } from "vue-router";
import * as echarts from "echarts";

const router = useRouter();
const route = useRoute();
const globalStore = GlobalStore();

const userInfo = globalStore.userInfo;

// 轮播图相关
const carouselList = ref([]);
const currentIndex = ref(0);
const carouselRef = ref(null);
let carouselInterval = null;

// 健康资讯
const healthNewsList = ref([]);

// 健康统计
const healthSummaryList = ref([]);
const chartRefs = ref([]);

const goToDetail = (id) => {
  router.push({ path: '/healthnews/detail', query: { id } });
};

const setCurrentIndex = (index) => {
  currentIndex.value = index;
};

const startCarousel = () => {
  if (carouselInterval) clearInterval(carouselInterval);
  if (carouselList.value.length <= 1) return;
  carouselInterval = setInterval(() => {
    currentIndex.value = (currentIndex.value + 1) % carouselList.value.length;
  }, 5000);
};

const initCharts = async () => {
  await nextTick();
  const chartElements = document.querySelectorAll('.chart-container');
  chartElements.forEach(el => {
    const id = el.getAttribute('data-id');
    const summary = healthSummaryList.value.find(s => s.id == id);
    if (!summary) return;

    try {
      const chartData = JSON.parse(summary.hs_summarydata);
      const chart = echarts.init(el);
      const option = {
        tooltip: {
          trigger: 'axis'
        },
        legend: {
          data: Object.keys(chartData)
        },
        xAxis: {
          type: 'category',
          data: ['指标']
        },
        yAxis: {
          type: 'value'
        },
        series: Object.entries(chartData).map(([name, value]) => ({
          name,
          type: 'bar',
          data: [parseFloat(value) || 0]
        }))
      };
      chart.setOption(option);
    } catch (e) {
      console.warn('Invalid summary data JSON:', e);
    }
  });
};

onMounted(async () => {
  // 获取轮播图
  const carouselRes = await request('/carousel/index', {}, 'get');
  carouselList.value = carouselRes.data;
  startCarousel();

  // 获取健康资讯
  const newsRes = await request('/healthnews/index', { limit: 6 }, 'get');
  healthNewsList.value = newsRes.data;

  // 获取健康统计
  const summaryRes = await request('/healthsummary/index', { userid: userInfo.id }, 'get');
  healthSummaryList.value = summaryRes.data;

  // 初始化图表
  await nextTick();
  initCharts();
});

// 清理定时器
onBeforeUnmount(() => {
  if (carouselInterval) clearInterval(carouselInterval);
});
</script>

<style scoped>
.home-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
}

/* 轮播图样式 */
.carousel-section {
  position: relative;
  height: 400px;
  border-radius: 12px;
  overflow: hidden;
  box-shadow: 0 8px 20px rgba(0, 0, 0, 0.15);
  margin-bottom: 40px;
}

.carousel-wrapper {
  position: relative;
  width: 100%;
  height: 100%;
}

.carousel-item {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  opacity: 0;
  transition: opacity 0.5s ease-in-out;
}

.carousel-item.active {
  opacity: 1;
}

.carousel-item img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.carousel-overlay {
  position: absolute;
  bottom: 0;
  left: 0;
  right: 0;
  background: linear-gradient(to top, rgba(0, 0, 0, 0.8), transparent);
  color: white;
  padding: 30px 20px 20px;
}

.carousel-overlay h2 {
  font-size: 24px;
  margin: 0 0 10px;
}

.carousel-overlay p {
  font-size: 16px;
  line-height: 1.5;
  max-height: 60px;
  overflow: hidden;
}

.carousel-indicators {
  position: absolute;
  bottom: 20px;
  left: 50%;
  transform: translateX(-50%);
  display: flex;
  gap: 8px;
}

.carousel-indicators span {
  width: 12px;
  height: 12px;
  border-radius: 50%;
  background: rgba(255, 255, 255, 0.5);
  cursor: pointer;
  transition: background 0.3s;
}

.carousel-indicators span.active {
  background: white;
}

/* 健康资讯样式 */
.section-title {
  font-size: 28px;
  color: #2c3e50;
  margin-bottom: 24px;
  font-weight: 600;
  position: relative;
  padding-bottom: 10px;
}

.section-title::after {
  content: '';
  position: absolute;
  bottom: 0;
  left: 0;
  width: 60px;
  height: 4px;
  background: #3498db;
  border-radius: 2px;
}

.healthnews-section {
  margin-bottom: 40px;
}

.news-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 24px;
}

.news-card {
  background: white;
  border-radius: 12px;
  overflow: hidden;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  transition: transform 0.3s, box-shadow 0.3s;
  cursor: pointer;
}

.news-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 8px 20px rgba(0, 0, 0, 0.15);
}

.news-cover img {
  width: 100%;
  height: 180px;
  object-fit: cover;
}

.news-content {
  padding: 20px;
}

.news-content h4 {
  font-size: 18px;
  color: #2c3e50;
  margin: 0 0 12px;
  line-height: 1.4;
}

.excerpt {
  font-size: 14px;
  color: #7f8c8d;
  line-height: 1.6;
  display: -webkit-box;
  -webkit-line-clamp: 3;
  -webkit-box-orient: vertical;
  overflow: hidden;
  margin-bottom: 12px;
}

.news-meta {
  display: flex;
  justify-content: space-between;
  color: #95a5a6;
  font-size: 13px;
}

/* 健康统计样式 */
.healthsummary-section {
  margin-bottom: 40px;
}

.summary-cards {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(350px, 1fr));
  gap: 24px;
}

.summary-card {
  background: white;
  border-radius: 12px;
  padding: 24px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
}

.summary-header h4 {
  font-size: 18px;
  color: #2c3e50;
  margin: 0 0 20px;
  font-weight: 600;
}

.summary-stats {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 16px;
  margin-bottom: 20px;
}

.stat-item {
  display: flex;
  flex-direction: column;
}

.label {
  font-size: 13px;
  color: #7f8c8d;
  margin-bottom: 4px;
}

.value {
  font-size: 18px;
  font-weight: 600;
  color: #2c3e50;
}

.chart-container {
  height: 200px;
  width: 100%;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .home-container {
    padding: 15px;
  }

  .carousel-section {
    height: 280px;
  }

  .news-grid,
  .summary-cards {
    grid-template-columns: 1fr;
  }

  .summary-stats {
    grid-template-columns: 1fr;
  }
}
</style>