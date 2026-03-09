<template>
  <div class="healthdata-detail-container">
    <div class="header">
      <h1>健康数据详情</h1>
      <div class="back-btn" @click="goBack">
        <img src="https://cdn-icons-png.flaticon.com/512/2223/2223615.png" alt="返回" />
        返回
      </div>
    </div>

    <div class="info-card">
      <div class="user-info">
        <img v-if="healthData.useravatar" :src="healthData.useravatar" class="avatar" />
        <div class="user-text">
          <span class="username">{{ healthData.username }}</span>
          <span class="record-date">记录日期：{{ healthData.hd_date }}</span>
        </div>
      </div>

      <div class="data-section">
        <h2>基础指标</h2>
        <div class="metrics-grid">
          <div class="metric-item">
            <label>身高</label>
            <span>{{ healthData.hd_height }} cm</span>
          </div>
          <div class="metric-item">
            <label>体重</label>
            <span>{{ healthData.hd_weight }} kg</span>
          </div>
          <div class="metric-item">
            <label>BMI指数</label>
            <span>{{ healthData.hd_bmi }}</span>
          </div>
        </div>
      </div>

      <div class="data-section">
        <h2>血压指标</h2>
        <div class="metrics-grid">
          <div class="metric-item">
            <label>收缩压 (SBP)</label>
            <span>{{ healthData.hd_sbp }} mmHg</span>
          </div>
          <div class="metric-item">
            <label>舒张压 (DBP)</label>
            <span>{{ healthData.hd_dbp }} mmHg</span>
          </div>
        </div>
      </div>

      <div class="data-section">
        <h2>血液指标</h2>
        <div class="metrics-grid">
          <div class="metric-item">
            <label>血糖水平</label>
            <span>{{ healthData.hd_glucose }} mmol/L</span>
          </div>
          <div class="metric-item">
            <label>总胆固醇</label>
            <span>{{ healthData.hd_cholesterol }} mmol/L</span>
          </div>
          <div class="metric-item">
            <label>高密度脂蛋白 (HDL)</label>
            <span>{{ healthData.hd_hdl }} mmol/L</span>
          </div>
          <div class="metric-item">
            <label>低密度脂蛋白 (LDL)</label>
            <span>{{ healthData.hd_ldl }} mmol/L</span>
          </div>
          <div class="metric-item">
            <label>甘油三酯</label>
            <span>{{ healthData.hd_triglycerides }} mmol/L</span>
          </div>
        </div>
      </div>

      <div class="data-section lifestyle-section">
        <h2>生活方式</h2>
        <div class="metrics-grid">
          <div class="metric-item">
            <label>是否吸烟</label>
            <span>{{ healthData.hd_smoking == 1 ? '否' : '是' }}</span>
          </div>
          <div class="metric-item">
            <label>是否饮酒</label>
            <span>{{ healthData.hd_alcohol == 1 ? '否' : '是' }}</span>
          </div>
          <div class="metric-item">
            <label>每周运动时长</label>
            <span>{{ healthData.hd_exercise }} 小时</span>
          </div>
        </div>
      </div>
    </div>

    <div class="chart-container" ref="chartRef"></div>
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
import * as echarts from "echarts";

const router = useRouter();
const route = useRoute();
const globalStore = GlobalStore();

const healthData = ref({});
const chartRef = ref(null);

const goBack = () => {
  router.push({ path: '/healthdata/list' });
};

const renderChart = () => {
  if (!chartRef.value) return;
  
  const chart = echarts.init(chartRef.value);
  
  const option = {
    title: {
      text: '心血管风险指标分析',
      left: 'center',
      textStyle: {
        fontSize: 18,
        fontWeight: 'bold'
      }
    },
    tooltip: {
      trigger: 'axis',
      axisPointer: {
        type: 'shadow'
      }
    },
    legend: {
      data: ['当前值', '正常范围上限'],
      bottom: 10
    },
    grid: {
      left: '3%',
      right: '4%',
      bottom: '15%',
      containLabel: true
    },
    xAxis: {
      type: 'category',
      data: ['收缩压', '舒张压', '血糖', '总胆固醇', 'HDL', 'LDL', '甘油三酯'],
      axisLabel: {
        rotate: 30
      }
    },
    yAxis: {
      type: 'value',
      name: '数值',
      min: 0
    },
    series: [
      {
        name: '当前值',
        type: 'bar',
        barWidth: '40%',
        data: [
          parseFloat(healthData.value.hd_sbp) || 0,
          parseFloat(healthData.value.hd_dbp) || 0,
          parseFloat(healthData.value.hd_glucose) || 0,
          parseFloat(healthData.value.hd_cholesterol) || 0,
          parseFloat(healthData.value.hd_hdl) || 0,
          parseFloat(healthData.value.hd_ldl) || 0,
          parseFloat(healthData.value.hd_triglycerides) || 0
        ],
        itemStyle: {
          color: '#FF6B6B'
        }
      },
      {
        name: '正常范围上限',
        type: 'line',
        data: [140, 90, 7.0, 5.2, 1.6, 3.4, 1.7],
        itemStyle: {
          color: '#4ECDC4'
        },
        lineStyle: {
          width: 2
        }
      }
    ]
  };
  
  chart.setOption(option);
  
  window.addEventListener('resize', () => {
    chart.resize();
  });
};

onMounted(async () => {
  const id = route.query.id;
  if (!id) {
    router.push({ path: '/healthdata/list' });
    return;
  }
  
  const res = await request('/healthdata/show', {
    id: id
  }, 'get');
  
  healthData.value = res;
  
  // 等待DOM更新后再渲染图表
  await new Promise(resolve => setTimeout(resolve, 100));
  renderChart();
});
</script>

<style scoped>
.healthdata-detail-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
  background: #f8f9fa;
  min-height: 100vh;
}

.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 30px;
  padding-bottom: 20px;
  border-bottom: 2px solid #e9ecef;
}

.header h1 {
  font-size: 28px;
  color: #2c3e50;
  font-weight: 700;
}

.back-btn {
  display: flex;
  align-items: center;
  gap: 8px;
  background: #3498db;
  color: white;
  padding: 8px 16px;
  border-radius: 20px;
  cursor: pointer;
  transition: all 0.3s ease;
  font-weight: 500;
}

.back-btn:hover {
  background: #2980b9;
  transform: translateY(-2px);
}

.back-btn img {
  width: 16px;
  height: 16px;
}

.info-card {
  background: white;
  border-radius: 16px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
  overflow: hidden;
  padding: 30px;
}

.user-info {
  display: flex;
  align-items: center;
  margin-bottom: 30px;
  padding-bottom: 20px;
  border-bottom: 1px solid #eee;
}

.avatar {
  width: 60px;
  height: 60px;
  border-radius: 50%;
  object-fit: cover;
  margin-right: 20px;
  border: 2px solid #3498db;
}

.user-text .username {
  font-size: 20px;
  font-weight: 700;
  color: #2c3e50;
  display: block;
  margin-bottom: 5px;
}

.user-text .record-date {
  color: #7f8c8d;
  font-size: 14px;
}

.data-section {
  margin-bottom: 30px;
}

.data-section h2 {
  font-size: 20px;
  color: #2c3e50;
  margin-bottom: 20px;
  padding-bottom: 10px;
  border-bottom: 2px solid #3498db;
  display: inline-block;
}

.metrics-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
  gap: 20px;
}

.metric-item {
  background: #f8f9fa;
  padding: 15px;
  border-radius: 12px;
  border-left: 4px solid #3498db;
  transition: transform 0.2s ease;
}

.metric-item:hover {
  transform: translateY(-3px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.metric-item label {
  display: block;
  color: #7f8c8d;
  font-size: 14px;
  margin-bottom: 8px;
  font-weight: 500;
}

.metric-item span {
  font-size: 18px;
  font-weight: 600;
  color: #2c3e50;
}

.lifestyle-section .metrics-grid {
  grid-template-columns: repeat(auto-fill, minmax(180px, 1fr));
}

.chart-container {
  height: 400px;
  margin-top: 30px;
  background: white;
  border-radius: 16px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
  padding: 20px;
}
</style>