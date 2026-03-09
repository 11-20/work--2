<template>
  <div class="risk-trend-container">
    <div class="header">
      <h1>心血管疾病风险趋势分析</h1>
      <p>基于您的历史预测记录，展示风险变化趋势</p>
    </div>

    <div class="chart-wrapper">
      <div id="riskTrendChart" class="chart"></div>
    </div>

    <div class="records-section">
      <h2>预测记录详情</h2>
      <div class="records-list">
        <div v-for="record in predictionRecords" :key="record.id" class="record-card">
          <div class="record-header">
            <span class="model-info">{{ record.wywpm_name }} (v{{ record.nubpm_version }})</span>
            <span class="time">{{ record.pr_predictiontime }}</span>
          </div>
          <div class="risk-level">
            <span>风险等级: </span>
            <span class="level-badge" :class="getRiskLevelClass(record.pr_risklevel)">
              {{ record.pr_risklevel }}
            </span>
          </div>
          <div class="probability">
            预测概率: {{ parseFloat(record.pr_probability).toFixed(2) }}%
          </div>
          <div class="prediction-details">
            <div class="detail-item">
              <span>年龄:</span>
              <span>{{ record.pr_age }}</span>
            </div>
            <div class="detail-item">
              <span>性别:</span>
              <span>{{ record.pr_sex == 2 ? '男' : '女' }}</span>
            </div>
            <div class="detail-item">
              <span>胸痛类型:</span>
              <span>{{ record.pr_cp }}</span>
            </div>
            <div class="detail-item">
              <span>静息血压:</span>
              <span>{{ record.pr_trestbps }}</span>
            </div>
            <div class="detail-item">
              <span>血清胆固醇:</span>
              <span>{{ record.pr_chol }}</span>
            </div>
            <div class="detail-item">
              <span>最大心率:</span>
              <span>{{ record.pr_thalach }}</span>
            </div>
          </div>
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

const predictionRecords = ref([]);

// 风险等级样式映射
const getRiskLevelClass = (level) => {
  if (level.includes('高')) return 'high';
  if (level.includes('中')) return 'medium';
  if (level.includes('低')) return 'low';
  return '';
};

// 初始化图表
const initChart = () => {
  const chartDom = document.getElementById('riskTrendChart');
  if (!chartDom) return;
  
  const myChart = echarts.init(chartDom);
  
  // 按模型分组数据
  const modelDataMap = new Map();
  predictionRecords.value.forEach(record => {
    const modelName = `${record.wywpm_name} (v${record.nubpm_version})`;
    if (!modelDataMap.has(modelName)) {
      modelDataMap.set(modelName, []);
    }
    modelDataMap.get(modelName).push({
      time: record.pr_predictiontime,
      risk: parseFloat(record.pr_probability)
    });
  });

  // 准备系列数据
  const series = [];
  const legendData = [];
  
  for (const [modelName, data] of modelDataMap) {
    // 按时间排序
    data.sort((a, b) => new Date(a.time) - new Date(b.time));
    
    series.push({
      name: modelName,
      type: 'line',
      smooth: true,
      symbol: 'circle',
      symbolSize: 6,
      lineStyle: {
        width: 3
      },
      emphasis: {
        focus: 'series'
      },
      data: data.map(item => [item.time, item.risk])
    });
    
    legendData.push(modelName);
  }

  const option = {
    tooltip: {
      trigger: 'axis',
      formatter: function(params) {
        let result = params[0].axisValue + '<br/>';
        params.forEach(param => {
          result += `<span style="display:inline-block;margin-right:5px;border-radius:10px;width:10px;height:10px;background-color:${param.color};"></span>
                    ${param.seriesName}: ${param.value[1]}%<br/>`;
        });
        return result;
      }
    },
    legend: {
      data: legendData,
      bottom: 10
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
      axisLine: {
        lineStyle: {
          color: '#666'
        }
      },
      axisLabel: {
        rotate: 45
      }
    },
    yAxis: {
      type: 'value',
      min: 0,
      max: 100,
      axisLabel: {
        formatter: '{value}%'
      },
      splitLine: {
        lineStyle: {
          type: 'dashed',
          color: '#eee'
        }
      }
    },
    series: series
  };

  myChart.setOption(option);
  
  // 响应式
  window.addEventListener('resize', () => {
    myChart.resize();
  });
};

onMounted(async () => {
  // 获取用户所有预测记录
  const res = await request('/predictionrecord/index', {
    userid: userInfo.id,
    limit: 999
  }, 'get');
  
  predictionRecords.value = res.data;
  
  // 等待DOM更新后初始化图表
  await nextTick();
  initChart();
});
</script>

<style scoped>
.risk-trend-container {
  padding: 24px;
  background: linear-gradient(135deg, #f5f7fa 0%, #e4edf9 100%);
  min-height: 100vh;
}

.header {
  text-align: center;
  margin-bottom: 32px;
}

.header h1 {
  font-size: 28px;
  font-weight: 700;
  color: #1a365d;
  margin-bottom: 8px;
}

.header p {
  font-size: 16px;
  color: #4a5568;
  max-width: 600px;
  margin: 0 auto;
}

.chart-wrapper {
  background: white;
  border-radius: 12px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
  padding: 24px;
  margin-bottom: 32px;
}

.chart {
  height: 400px;
  width: 100%;
}

.records-section h2 {
  font-size: 22px;
  font-weight: 600;
  color: #1a365d;
  margin-bottom: 24px;
  padding-bottom: 12px;
  border-bottom: 2px solid #e2e8f0;
}

.records-list {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(320px, 1fr));
  gap: 24px;
}

.record-card {
  background: white;
  border-radius: 12px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.06);
  padding: 20px;
  transition: transform 0.2s ease, box-shadow 0.2s ease;
}

.record-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 6px 16px rgba(0, 0, 0, 0.1);
}

.record-header {
  display: flex;
  justify-content: space-between;
  margin-bottom: 16px;
  padding-bottom: 12px;
  border-bottom: 1px solid #edf2f7;
}

.model-info {
  font-weight: 600;
  color: #2b6cb0;
  font-size: 16px;
}

.time {
  color: #718096;
  font-size: 14px;
}

.risk-level {
  margin-bottom: 12px;
  display: flex;
  align-items: center;
  gap: 8px;
}

.risk-level span:first-child {
  font-weight: 500;
  color: #4a5568;
}

.level-badge {
  padding: 4px 12px;
  border-radius: 20px;
  font-size: 14px;
  font-weight: 600;
  text-transform: uppercase;
}

.level-badge.high {
  background-color: #fee2e2;
  color: #dc2626;
}

.level-badge.medium {
  background-color: #fef3c7;
  color: #d97706;
}

.level-badge.low {
  background-color: #dcfce7;
  color: #16a34a;
}

.probability {
  font-weight: 600;
  color: #1a365d;
  margin-bottom: 16px;
  font-size: 16px;
}

.prediction-details {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 12px;
}

.detail-item {
  display: flex;
  justify-content: space-between;
  padding: 6px 0;
  border-bottom: 1px dashed #edf2f7;
}

.detail-item:last-child {
  border-bottom: none;
}

.detail-item span:first-child {
  font-weight: 500;
  color: #4a5568;
}

.detail-item span:last-child {
  color: #2d3748;
  font-weight: 500;
}

@media (max-width: 768px) {
  .risk-trend-container {
    padding: 16px;
  }
  
  .chart {
    height: 300px;
  }
  
  .records-list {
    grid-template-columns: 1fr;
  }
  
  .prediction-details {
    grid-template-columns: 1fr;
  }
}
</style>