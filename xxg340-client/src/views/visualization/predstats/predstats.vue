<template>
  <div class="pred-stats-container">
    <div class="header">
      <h1>预测结果统计分析</h1>
      <p>基于您的历史预测记录，可视化展示心血管疾病风险等级分布</p>
    </div>

    <div class="chart-wrapper">
      <div id="risk-pie-chart" class="chart"></div>
    </div>

    <div class="stats-summary">
      <div class="summary-card">
        <div class="icon">
          <img src="https://cdn-icons-png.flaticon.com/512/3096/3096673.png" alt="总记录" />
        </div>
        <div class="content">
          <span class="label">总预测次数</span>
          <span class="value">{{ totalRecords }}</span>
        </div>
      </div>
      <div class="summary-card">
        <div class="icon">
          <img src="https://cdn-icons-png.flaticon.com/512/2972/2972475.png" alt="高风险" />
        </div>
        <div class="content">
          <span class="label">高风险次数</span>
          <span class="value">{{ highRiskCount }}</span>
        </div>
      </div>
      <div class="summary-card">
        <div class="icon">
          <img src="https://cdn-icons-png.flaticon.com/512/2972/2972480.png" alt="中风险" />
        </div>
        <div class="content">
          <span class="label">中风险次数</span>
          <span class="value">{{ mediumRiskCount }}</span>
        </div>
      </div>
      <div class="summary-card">
        <div class="icon">
          <img src="https://cdn-icons-png.flaticon.com/512/2972/2972485.png" alt="低风险" />
        </div>
        <div class="content">
          <span class="label">低风险次数</span>
          <span class="value">{{ lowRiskCount }}</span>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { 
  ref, 
  onMounted, 
  onBeforeUnmount
} from 'vue';

import { request } from "@/http/index";
import { GlobalStore } from "@/stores";
import { useRoute, useRouter } from "vue-router";
import * as echarts from "echarts";

const router = useRouter();
const route = useRoute();
const globalStore = GlobalStore();

const userInfo = globalStore.userInfo;

// 统计数据
const totalRecords = ref(0);
const highRiskCount = ref(0);
const mediumRiskCount = ref(0);
const lowRiskCount = ref(0);

let chartInstance = null;

const initChart = () => {
  const chartDom = document.getElementById('risk-pie-chart');
  if (!chartDom) return;
  
  chartInstance = echarts.init(chartDom);
  
  const option = {
    tooltip: {
      trigger: 'item',
      formatter: '{a} <br/>{b}: {c} ({d}%)'
    },
    legend: {
      orient: 'horizontal',
      bottom: '0%',
      data: ['高风险', '中风险', '低风险'],
      textStyle: {
        color: '#555'
      }
    },
    series: [
      {
        name: '风险等级分布',
        type: 'pie',
        radius: ['40%', '70%'],
        avoidLabelOverlap: false,
        itemStyle: {
          borderRadius: 10,
          borderColor: '#fff',
          borderWidth: 2
        },
        label: {
          show: true,
          position: 'outside',
          formatter: '{b}\n{d}%',
          fontSize: 14,
          fontWeight: 'bold'
        },
        emphasis: {
          label: {
            show: true,
            fontSize: 16,
            fontWeight: 'bold'
          }
        },
        data: [
          { value: highRiskCount.value, name: '高风险', itemStyle: { color: '#e74c3c' } },
          { value: mediumRiskCount.value, name: '中风险', itemStyle: { color: '#f39c12' } },
          { value: lowRiskCount.value, name: '低风险', itemStyle: { color: '#2ecc71' } }
        ]
      }
    ]
  };

  chartInstance.setOption(option);
};

const fetchData = async () => {
  const res = await request('/predictionrecord/index', {
    userid: userInfo.id,
    limit: 999
  }, 'get');
  
  const records = res.data;
  totalRecords.value = records.length;
  
  // 重置计数
  highRiskCount.value = 0;
  mediumRiskCount.value = 0;
  lowRiskCount.value = 0;
  
  // 统计各风险等级
  records.forEach(record => {
    const riskLevel = record.pr_risklevel.toLowerCase();
    if (riskLevel == '高风险' || riskLevel == 'high') {
      highRiskCount.value++;
    } else if (riskLevel == '中风险' || riskLevel == 'medium') {
      mediumRiskCount.value++;
    } else if (riskLevel == '低风险' || riskLevel == 'low') {
      lowRiskCount.value++;
    }
  });
  
  // 初始化或更新图表
  if (chartInstance) {
    chartInstance.setOption({
      series: [{
        data: [
          { value: highRiskCount.value, name: '高风险', itemStyle: { color: '#e74c3c' } },
          { value: mediumRiskCount.value, name: '中风险', itemStyle: { color: '#f39c12' } },
          { value: lowRiskCount.value, name: '低风险', itemStyle: { color: '#2ecc71' } }
        ]
      }]
    });
  } else {
    initChart();
  }
};

onMounted(async () => {
  await fetchData();
  window.addEventListener('resize', () => {
    if (chartInstance) {
      chartInstance.resize();
    }
  });
});

onBeforeUnmount(() => {
  if (chartInstance) {
    chartInstance.dispose();
  }
  window.removeEventListener('resize', () => {
    if (chartInstance) {
      chartInstance.resize();
    }
  });
});
</script>

<style scoped>
.pred-stats-container {
  padding: 30px;
  background: linear-gradient(135deg, #f5f7fa 0%, #e4edf5 100%);
  min-height: 100vh;
}

.header {
  text-align: center;
  margin-bottom: 40px;
}

.header h1 {
  font-size: 2.5rem;
  color: #2c3e50;
  margin-bottom: 12px;
  font-weight: 700;
}

.header p {
  font-size: 1.1rem;
  color: #7f8c8d;
  max-width: 700px;
  margin: 0 auto;
  line-height: 1.6;
}

.chart-wrapper {
  display: flex;
  justify-content: center;
  margin-bottom: 50px;
}

.chart {
  width: 600px;
  height: 500px;
  background: white;
  border-radius: 16px;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.08);
  padding: 20px;
}

.stats-summary {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
  gap: 24px;
  max-width: 1000px;
  margin: 0 auto;
}

.summary-card {
  background: white;
  border-radius: 16px;
  padding: 24px;
  display: flex;
  align-items: center;
  box-shadow: 0 6px 20px rgba(0, 0, 0, 0.06);
  transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.summary-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 12px 25px rgba(0, 0, 0, 0.12);
}

.icon {
  width: 60px;
  height: 60px;
  margin-right: 20px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.icon img {
  width: 40px;
  height: 40px;
}

.content .label {
  display: block;
  font-size: 1rem;
  color: #7f8c8d;
  margin-bottom: 8px;
}

.content .value {
  display: block;
  font-size: 1.8rem;
  font-weight: 700;
  color: #2c3e50;
}

@media (max-width: 768px) {
  .pred-stats-container {
    padding: 20px 15px;
  }
  
  .header h1 {
    font-size: 2rem;
  }
  
  .chart {
    width: 100%;
    height: 400px;
    padding: 15px;
  }
  
  .stats-summary {
    grid-template-columns: 1fr;
  }
}
</style>