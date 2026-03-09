<template>
  <div class="health-dist-container">
    <div class="header">
      <h1>健康指标分布分析</h1>
      <p>基于您的历史健康数据，可视化展示各项关键指标的分布情况</p>
    </div>

    <div class="charts-grid" ref="chartsContainer">
      <div class="chart-card" v-for="(config, index) in chartConfigs" :key="index">
        <h3>{{ config.title }}</h3>
        <div class="chart-wrapper">
          <div :id="`chart-${index}`" class="chart"></div>
        </div>
        <div class="reference-line" v-if="config.reference">
          正常范围参考线: {{ config.reference }}
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
import * as echarts from "echarts";

const globalStore = GlobalStore();
const userInfo = globalStore.userInfo;
const chartsContainer = ref(null);
const healthData = ref([]);

// 定义各指标的配置
const chartConfigs = [
  {
    key: 'hd_sbp',
    title: '收缩压 (mmHg)',
    reference: '正常范围: 90-120'
  },
  {
    key: 'hd_dbp',
    title: '舒张压 (mmHg)',
    reference: '正常范围: 60-80'
  },
  {
    key: 'hd_glucose',
    title: '血糖水平 (mmol/L)',
    reference: '空腹正常: 3.9-6.1'
  },
  {
    key: 'hd_cholesterol',
    title: '总胆固醇 (mmol/L)',
    reference: '理想值: <5.2'
  },
  {
    key: 'hd_hdl',
    title: '高密度脂蛋白 (mmol/L)',
    reference: '理想值: >1.0 (男), >1.3 (女)'
  },
  {
    key: 'hd_ldl',
    title: '低密度脂蛋白 (mmol/L)',
    reference: '理想值: <3.4'
  },
  {
    key: 'hd_triglycerides',
    title: '甘油三酯 (mmol/L)',
    reference: '理想值: <1.7'
  },
  {
    key: 'hd_bmi',
    title: 'BMI指数',
    reference: '正常范围: 18.5-24'
  }
];

// 存储echarts实例
const chartInstances = [];

onMounted(async () => {
  // 获取健康数据
  const res = await request('/healthdata/index', {
    userid: userInfo.id,
    limit: 999
  }, 'get');
  
  healthData.value = res.data;

  // 初始化图表
  await nextTick();
  initCharts();
});

onBeforeUnmount(() => {
  // 销毁echarts实例
  chartInstances.forEach(instance => {
    if (instance) instance.dispose();
  });
  chartInstances.length = 0;
});

const initCharts = () => {
  chartConfigs.forEach((config, index) => {
    const chartDom = document.getElementById(`chart-${index}`);
    if (!chartDom) return;

    const myChart = echarts.init(chartDom);
    chartInstances.push(myChart);

    // 提取该指标的数据
    const values = healthData.value
      .map(item => parseFloat(item[config.key]))
      .filter(val => !isNaN(val));

    if (values.length == 0) {
      myChart.setOption({
        title: {
          text: '暂无数据',
          left: 'center',
          top: 'middle',
          textStyle: {
            color: '#999',
            fontSize: 14
          }
        }
      });
      return;
    }

    // 计算箱线图所需数据
    const sortedValues = [...values].sort((a, b) => a - b);
    const count = sortedValues.length;
    const min = sortedValues[0];
    const max = sortedValues[count - 1];
    const median = count % 2 == 0 
      ? (sortedValues[Math.floor(count / 2) - 1] + sortedValues[Math.floor(count / 2)]) / 2
      : sortedValues[Math.floor(count / 2)];
    
    const q1Index = Math.floor(count * 0.25);
    const q3Index = Math.floor(count * 0.75);
    const q1 = sortedValues[q1Index];
    const q3 = sortedValues[q3Index];

    const option = {
      tooltip: {
        trigger: 'item',
        formatter: function(params) {
          if (params.seriesType == 'boxplot') {
            return `
              最小值: ${params.data[0]}<br/>
              第一四分位数(Q1): ${params.data[1]}<br/>
              中位数: ${params.data[2]}<br/>
              第三四分位数(Q3): ${params.data[3]}<br/>
              最大值: ${params.data[4]}
            `;
          }
          return params.value;
        }
      },
      grid: {
        left: '10%',
        right: '10%',
        bottom: '15%',
        top: '10%'
      },
      xAxis: {
        type: 'value',
        name: config.key.includes('pressure') ? '血压 (mmHg)' : 
               config.key.includes('glucose') ? '血糖 (mmol/L)' :
               config.key.includes('cholesterol') || config.key.includes('hdl') || config.key.includes('ldl') || config.key.includes('triglycerides') ? '血脂 (mmol/L)' :
               '数值',
        nameLocation: 'middle',
        nameGap: 30,
        axisLabel: {
          color: '#666'
        },
        axisLine: {
          lineStyle: {
            color: '#ddd'
          }
        }
      },
      yAxis: {
        type: 'category',
        data: [''],
        axisLabel: {
          show: false
        },
        axisTick: {
          show: false
        },
        axisLine: {
          show: false
        }
      },
      series: [{
        type: 'boxplot',
        data: [[min, q1, median, q3, max]],
        itemStyle: {
          color: '#409EFF'
        },
        emphasis: {
          itemStyle: {
            borderColor: '#66b1ff',
            borderWidth: 2
          }
        }
      }]
    };

    myChart.setOption(option);
    
    // 监听窗口大小变化
    window.addEventListener('resize', () => {
      myChart.resize();
    });
  });
};

// 确保nextTick可用
const nextTick = Promise.resolve().then.bind(Promise.resolve());
</script>

<style scoped>
.health-dist-container {
  padding: 24px;
  background: linear-gradient(135deg, #f5f7fa 0%, #e4edf5 100%);
  min-height: 100vh;
}

.header {
  text-align: center;
  margin-bottom: 32px;
}

.header h1 {
  font-size: 28px;
  font-weight: 700;
  color: #2c3e50;
  margin-bottom: 12px;
  background: linear-gradient(90deg, #1e5799, #207cca, #2989d8, #1e5799);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-size: 300% 300%;
  animation: gradientShift 3s ease infinite;
}

@keyframes gradientShift {
  0% { background-position: 0% 50%; }
  50% { background-position: 100% 50%; }
  100% { background-position: 0% 50%; }
}

.header p {
  font-size: 16px;
  color: #666;
  max-width: 600px;
  margin: 0 auto;
  line-height: 1.6;
}

.charts-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(320px, 1fr));
  gap: 24px;
  max-width: 1400px;
  margin: 0 auto;
}

.chart-card {
  background: white;
  border-radius: 16px;
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.08);
  overflow: hidden;
  transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.chart-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 12px 32px rgba(0, 0, 0, 0.12);
}

.chart-card h3 {
  font-size: 18px;
  font-weight: 600;
  color: #2c3e50;
  padding: 20px 24px 12px;
  margin: 0;
}

.chart-wrapper {
  padding: 0 24px 16px;
  height: 200px;
}

.chart {
  width: 100%;
  height: 100%;
}

.reference-line {
  padding: 12px 24px;
  background: #f8f9fa;
  border-top: 1px solid #eee;
  font-size: 13px;
  color: #666;
  line-height: 1.5;
}

@media (max-width: 768px) {
  .health-dist-container {
    padding: 16px;
  }
  
  .charts-grid {
    grid-template-columns: 1fr;
    gap: 16px;
  }
  
  .header h1 {
    font-size: 24px;
  }
  
  .chart-wrapper {
    height: 180px;
  }
}
</style>