<template>
  <div class="health-data-list">
    <div class="header">
      <h1>我的健康数据记录</h1>
      <div class="actions">
        <button class="btn-primary" @click="goToEdit">+ 添加新记录</button>
      </div>
    </div>

    <div class="filters">
      <div class="filter-item">
        <label>按日期筛选：</label>
        <input
          type="date"
          v-model="filterDate"
          @change="applyDateFilter"
          class="date-input"
        />
      </div>
    </div>

    <div class="data-grid" v-if="healthDataList.length > 0">
      <div
        v-for="item in displayedData"
        :key="item.id"
        class="data-card"
        @click="viewDetail(item.id)"
      >
        <div class="card-header">
          <span class="record-date">{{ item.hd_date }}</span>
          <span class="edit-icon">✎</span>
        </div>
        <div class="metrics-grid">
          <MetricItem label="收缩压 (mmHg)" :value="item.hd_sbp" :is-abnormal="isHighBloodPressure(item.hd_sbp, item.hd_dbp)" />
          <MetricItem label="舒张压 (mmHg)" :value="item.hd_dbp" :is-abnormal="isHighBloodPressure(item.hd_sbp, item.hd_dbp)" />
          <MetricItem label="血糖 (mmol/L)" :value="item.hd_glucose" :is-abnormal="isHighGlucose(item.hd_glucose)" />
          <MetricItem label="BMI" :value="item.hd_bmi" :is-abnormal="isAbnormalBMI(item.hd_bmi)" />
          <MetricItem label="总胆固醇" :value="item.hd_cholesterol" :is-abnormal="isHighCholesterol(item.hd_cholesterol)" />
          <MetricItem label="甘油三酯" :value="item.hd_triglycerides" :is-abnormal="isHighTriglycerides(item.hd_triglycerides)" />
        </div>
        <div class="lifestyle-info">
          <span class="tag" :class="{ 'tag-danger': item.hd_smoking == 2 }">
            吸烟：{{ item.hd_smoking == 2 ? '是' : '否' }}
          </span>
          <span class="tag" :class="{ 'tag-danger': item.hd_alcohol == 2 }">
            饮酒：{{ item.hd_alcohol == 2 ? '是' : '否' }}
          </span>
          <span class="tag">运动：{{ item.hd_exercise }} 小时/周</span>
        </div>
      </div>
    </div>

    <div v-else class="empty-state">
      <img src="https://cdn-icons-png.flaticon.com/512/2972/2972185.png" alt="无数据" />
      <p>暂无健康数据记录</p>
      <button class="btn-primary" @click="goToEdit">立即添加</button>
    </div>

    <!-- 图表分析区域 -->
    <div class="chart-section" ref="chartRef" v-if="healthDataList.length > 0"></div>
  </div>
</template>

<script setup lang="ts">
import {
  ref,
  onMounted,
  computed,
  nextTick
} from 'vue';

import { request } from "@/http/index";
import { GlobalStore } from "@/stores";
import { useRoute, useRouter } from "vue-router";
import { ElMessage } from 'element-plus'
import * as echarts from "echarts";

const router = useRouter();
const route = useRoute();
const globalStore = GlobalStore();
const userInfo = globalStore.userInfo;

const healthDataList = ref([]);
const filterDate = ref('');
const chartRef = ref(null);

// 获取健康数据
const fetchHealthData = async () => {
  const res = await request('/healthdata/index', {
    userid: userInfo.id,
    limit: 999
  }, 'get');
  healthDataList.value = res.data;
  // 按时间倒序（假设 hd_date 是 YYYY-MM-DD 格式）
  healthDataList.value.sort((a, b) => new Date(b.hd_date) - new Date(a.hd_date));
};

// 跳转到编辑页
const goToEdit = () => {
  router.push({ path: '/healthdata/edit' });
};

// 查看详情（跳转编辑页带id）
const viewDetail = (id) => {
  router.push({ path: '/healthdata/edit', query: { id } });
};

// 日期筛选
const displayedData = computed(() => {
  if (!filterDate.value) return healthDataList.value;
  return healthDataList.value.filter(item => item.hd_date == filterDate.value);
});

const applyDateFilter = () => {
  // computed 自动更新，无需额外逻辑
};

// 异常值判断函数
const isHighBloodPressure = (sbp, dbp) => {
  const s = parseFloat(sbp);
  const d = parseFloat(dbp);
  return s >= 140 || d >= 90;
};

const isHighGlucose = (glucose) => {
  const g = parseFloat(glucose);
  return g >= 7.0; // 空腹血糖 ≥7.0 mmol/L 为异常
};

const isAbnormalBMI = (bmi) => {
  const b = parseFloat(bmi);
  return b < 18.5 || b >= 24.0;
};

const isHighCholesterol = (cholesterol) => {
  const c = parseFloat(cholesterol);
  return c >= 5.2; // 总胆固醇 ≥5.2 mmol/L 异常
};

const isHighTriglycerides = (triglycerides) => {
  const t = parseFloat(triglycerides);
  return t >= 1.7; // 甘油三酯 ≥1.7 mmol/L 异常
};

// 渲染图表
const renderChart = () => {
  if (!chartRef.value || healthDataList.value.length == 0) return;

  const chart = echarts.init(chartRef.value);

  const dates = healthDataList.value.map(item => item.hd_date);
  const sbpData = healthDataList.value.map(item => parseFloat(item.hd_sbp));
  const dbpData = healthDataList.value.map(item => parseFloat(item.hd_dbp));
  const glucoseData = healthDataList.value.map(item => parseFloat(item.hd_glucose));

  const option = {
    tooltip: {
      trigger: 'axis',
      axisPointer: {
        type: 'cross'
      }
    },
    legend: {
      data: ['收缩压', '舒张压', '血糖'],
      bottom: 0
    },
    grid: {
      left: '3%',
      right: '4%',
      bottom: '15%',
      top: '20%',
      containLabel: true
    },
    xAxis: {
      type: 'category',
      boundaryGap: false,
      data: dates
    },
    yAxis: [
      {
        type: 'value',
        name: '血压 (mmHg)',
        min: 60,
        max: 180,
        position: 'left',
        axisLine: {
          lineStyle: {
            color: '#5470C6'
          }
        }
      },
      {
        type: 'value',
        name: '血糖 (mmol/L)',
        min: 3,
        max: 12,
        position: 'right',
        axisLine: {
          lineStyle: {
            color: '#91CC75'
          }
        },
        splitLine: {
          show: false
        }
      }
    ],
    series: [
      {
        name: '收缩压',
        type: 'line',
        yAxisIndex: 0,
        data: sbpData,
        smooth: true,
        lineStyle: {
          width: 2
        },
        markLine: {
          silent: true,
          data: [{ yAxis: 140, label: { show: false } }]
        }
      },
      {
        name: '舒张压',
        type: 'line',
        yAxisIndex: 0,
        data: dbpData,
        smooth: true,
        lineStyle: {
          width: 2
        },
        markLine: {
          silent: true,
          data: [{ yAxis: 90, label: { show: false } }]
        }
      },
      {
        name: '血糖',
        type: 'line',
        yAxisIndex: 1,
        data: glucoseData,
        smooth: true,
        lineStyle: {
          width: 2,
          color: '#91CC75'
        },
        markLine: {
          silent: true,
          data: [{ yAxis: 7.0, label: { show: false } }]
        }
      }
    ]
  };

  chart.setOption(option);
};

// 响应式调整图表
const resizeChart = () => {
  if (chartRef.value) {
    const chart = echarts.getInstanceByDom(chartRef.value);
    if (chart) chart.resize();
  }
};

onMounted(async () => {
  await fetchHealthData();
  await nextTick();
  renderChart();
  window.addEventListener('resize', resizeChart);
});

// 组件卸载时移除监听
onBeforeUnmount(() => {
  window.removeEventListener('resize', resizeChart);
});
</script>

<style scoped>
.health-data-list {
  padding: 24px;
  background-color: #f8fafc;
  min-height: 100vh;
}

.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 24px;
}

.header h1 {
  font-size: 28px;
  font-weight: 700;
  color: #1e293b;
}

.btn-primary {
  background: linear-gradient(135deg, #3b82f6, #1d4ed8);
  color: white;
  border: none;
  padding: 10px 20px;
  border-radius: 8px;
  font-size: 16px;
  cursor: pointer;
  transition: all 0.3s ease;
  box-shadow: 0 4px 6px rgba(59, 130, 246, 0.2);
}

.btn-primary:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 8px rgba(59, 130, 246, 0.3);
}

.filters {
  background: white;
  padding: 16px 24px;
  border-radius: 12px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.05);
  margin-bottom: 24px;
  display: flex;
  gap: 16px;
  align-items: center;
}

.filter-item label {
  font-weight: 600;
  color: #334155;
  margin-right: 8px;
}

.date-input {
  padding: 8px 12px;
  border: 1px solid #cbd5e1;
  border-radius: 8px;
  font-size: 15px;
  outline: none;
  transition: border-color 0.3s;
}

.date-input:focus {
  border-color: #3b82f6;
}

.data-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(320px, 1fr));
  gap: 20px;
  margin-bottom: 40px;
}

.data-card {
  background: white;
  border-radius: 16px;
  overflow: hidden;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
  transition: transform 0.3s ease, box-shadow 0.3s ease;
  cursor: pointer;
}

.data-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 6px 16px rgba(0, 0, 0, 0.12);
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 16px 20px;
  background: #f1f5f9;
  border-bottom: 1px solid #e2e8f0;
}

.record-date {
  font-weight: 600;
  color: #1e293b;
  font-size: 16px;
}

.edit-icon {
  color: #64748b;
  font-size: 18px;
}

.metrics-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 16px;
  padding: 20px;
}

.metric-item {
  display: flex;
  flex-direction: column;
}

.metric-label {
  font-size: 13px;
  color: #64748b;
  margin-bottom: 4px;
}

.metric-value {
  font-size: 18px;
  font-weight: 700;
  color: #1e293b;
}

.metric-value.abnormal {
  color: #ef4444;
}

.lifestyle-info {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  padding: 0 20px 20px;
  border-top: 1px dashed #e2e8f0;
}

.tag {
  background: #f1f5f9;
  color: #334155;
  padding: 4px 10px;
  border-radius: 20px;
  font-size: 13px;
  font-weight: 500;
}

.tag-danger {
  background: #fee2e2;
  color: #dc2626;
}

.empty-state {
  text-align: center;
  padding: 60px 20px;
  background: white;
  border-radius: 16px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
}

.empty-state img {
  width: 100px;
  height: 100px;
  margin-bottom: 20px;
  opacity: 0.7;
}

.empty-state p {
  font-size: 18px;
  color: #64748b;
  margin-bottom: 24px;
}

.chart-section {
  background: white;
  border-radius: 16px;
  padding: 24px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.05);
  height: 400px;
}

/* 长文本隐藏（虽然本页面无长文本，但按要求保留） */
.text-ellipsis {
  display: -webkit-box;
  -webkit-line-clamp: 3;
  -webkit-box-orient: vertical;
  overflow: hidden;
}
</style>