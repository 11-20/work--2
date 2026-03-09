<template>
  <div class="report-detail-container">
    <!-- 报告头部 -->
    <div class="report-header">
      <h1 class="report-title">心血管疾病风险预测报告</h1>
      <div class="report-meta">
        <span>预测时间：{{ reportData.pr_predictiontime }}</span>
        <span>用户：{{ reportData.username }}</span>
        <span>模型：{{ reportData.wywpm_name }} (v{{ reportData.nubpm_version }})</span>
      </div>
    </div>

    <!-- 用户基本信息卡片 -->
    <div class="card">
      <h2 class="section-title">
        <img src="https://cdn-icons-png.flaticon.com/512/2972/2972185.png" alt="user" class="icon" />
        基本信息
      </h2>
      <div class="info-grid">
        <div class="info-item">
          <label>年龄</label>
          <span>{{ reportData.pr_age }} 岁</span>
        </div>
        <div class="info-item">
          <label>性别</label>
          <span>{{ reportData.pr_sex == 2 ? '男' : '女' }}</span>
        </div>
        <div class="info-item">
          <label>预测类型</label>
          <span>{{ reportData.pr_isbatch == 1 ? '单次预测' : '批量预测' }}</span>
        </div>
        <div class="info-item">
          <label>风险等级</label>
          <span :class="`risk-level risk-${reportData.pr_risklevel.toLowerCase() || 'unknown'}`">
            {{ reportData.pr_risklevel }}
          </span>
        </div>
      </div>
    </div>

    <!-- 输入指标卡片 -->
    <div class="card">
      <h2 class="section-title">
        <img src="https://cdn-icons-png.flaticon.com/512/3003/3003842.png" alt="metrics" class="icon" />
        输入指标
      </h2>
      <div class="metrics-grid">
        <div class="metric-item">
          <label>胸痛类型</label>
          <span>{{ reportData.pr_cp }}</span>
        </div>
        <div class="metric-item">
          <label>静息血压 (mmHg)</label>
          <span>{{ reportData.pr_trestbps }}</span>
        </div>
        <div class="metric-item">
          <label>血清胆固醇 (mg/dl)</label>
          <span>{{ reportData.pr_chol }}</span>
        </div>
        <div class="metric-item">
          <label>空腹血糖 >120 mg/dl</label>
          <span>{{ reportData.pr_fbs }}</span>
        </div>
        <div class="metric-item">
          <label>静息心电图结果</label>
          <span>{{ reportData.pr_restecg }}</span>
        </div>
        <div class="metric-item">
          <label>最大心率</label>
          <span>{{ reportData.pr_thalach }}</span>
        </div>
        <div class="metric-item">
          <label>运动诱发心绞痛</label>
          <span>{{ reportData.pr_exang }}</span>
        </div>
        <div class="metric-item">
          <label>ST段压低</label>
          <span>{{ reportData.pr_oldpeak }}</span>
        </div>
        <div class="metric-item">
          <label>ST段峰值运动斜率</label>
          <span>{{ reportData.pr_slope }}</span>
        </div>
        <div class="metric-item">
          <label>主要血管数量</label>
          <span>{{ reportData.pr_ca }}</span>
        </div>
        <div class="metric-item">
          <label>地中海贫血</label>
          <span>{{ reportData.pr_thal }}</span>
        </div>
      </div>
    </div>

    <!-- 风险评分与概率 -->
    <div class="card">
      <h2 class="section-title">
        <img src="https://cdn-icons-png.flaticon.com/512/2972/2972201.png" alt="score" class="icon" />
        风险评估
      </h2>
      <div class="score-section">
        <div class="probability-display">
          <div class="probability-value">{{ parseFloat(reportData.pr_probability).toFixed(2) }}%</div>
          <div class="probability-label">患病概率</div>
        </div>
        <div class="risk-chart" ref="riskChartRef"></div>
      </div>
    </div>

    <!-- 模板内容展示 -->
    <div v-if="matchedTemplate" class="card template-content">
      <h2 class="section-title">
        <img src="https://cdn-icons-png.flaticon.com/512/2972/2972136.png" alt="template" class="icon" />
        个性化建议
      </h2>
      
      <div class="template-section">
        <h3>风险解释</h3>
        <div v-html="matchedTemplate.rt_explanation"></div>
      </div>
      
      <div class="template-section">
        <h3>建议措施</h3>
        <div v-html="matchedTemplate.rt_suggestions"></div>
      </div>
      
      <div class="template-section">
        <h3>正常范围说明</h3>
        <div v-html="matchedTemplate.rt_normalscope"></div>
      </div>
      
      <div class="template-section">
        <h3>模板内容</h3>
        <div v-html="matchedTemplate.rt_templatecontent"></div>
      </div>
    </div>

    <!-- 文件区域 -->
    <div v-if="reportData.pr_batchfile && reportData.pr_batchfile.length > 0" class="card">
      <h2 class="section-title">
        <img src="https://cdn-icons-png.flaticon.com/512/2972/2972124.png" alt="files" class="icon" />
        批量预测文件
      </h2>
      <div class="file-list">
        <div v-for="(file, index) in reportData.pr_batchfile" :key="index" class="file-item">
          <a :href="file.url" target="_blank" class="file-link">
            {{ file.name }}
          </a>
        </div>
      </div>
    </div>

    <div v-if="reportData.pr_resultfile && reportData.pr_resultfile.length > 0" class="card">
      <h2 class="section-title">
        <img src="https://cdn-icons-png.flaticon.com/512/2972/2972124.png" alt="files" class="icon" />
        预测结果文件
      </h2>
      <div class="file-list">
        <div v-for="(file, index) in reportData.pr_resultfile" :key="index" class="file-item">
          <a :href="file.url" target="_blank" class="file-link">
            {{ file.name }}
          </a>
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

const reportData = ref({});
const templates = ref([]);
const matchedTemplate = ref(null);
const riskChartRef = ref(null);

onMounted(async () => {
  const id = route.query.id;
  if (!id) {
    ElMessage.error('缺少报告ID');
    router.push({ path: '/prediction/list' });
    return;
  }

  // 获取预测报告详情
  const res1 = await request('/predictionrecord/show', {
    id: id
  }, 'get');
  reportData.value = res1;

  // 获取所有报告模板
  const res2 = await request('/reporttemplate/index', {
    limit: 999
  }, 'get');
  templates.value = res2.data;

  // 匹配适用模板（根据风险等级）
  const riskLevel = reportData.value.pr_risklevel;
  if (riskLevel) {
    matchedTemplate.value = templates.value.find(t => t.rt_risklevel == riskLevel) || null;
  }

  // 初始化图表
  await nextTick();
  initRiskChart();
});

const initRiskChart = () => {
  if (!riskChartRef.value) return;

  const chart = echarts.init(riskChartRef.value);
  const probability = parseFloat(reportData.value.pr_probability) || 0;
  const option = {
    tooltip: {
      formatter: '{a} <br/>{b} : {c}%'
    },
    series: [
      {
        name: '风险概率',
        type: 'gauge',
        detail: { 
          formatter: '{value}%',
          fontSize: 20,
          color: '#333'
        },
        data: [{ value: probability, name: '患病概率' }],
        axisLine: {
          lineStyle: {
            width: 15,
            color: [
              [0.3, '#67e0e3'],
              [0.7, '#37a2da'],
              [1, '#fd666d']
            ]
          }
        },
        splitLine: {
          length: 15,
          lineStyle: {
            width: 2,
            color: '#999'
          }
        },
        axisTick: {
          length: 10,
          lineStyle: {
            color: '#999'
          }
        },
        axisLabel: {
          color: '#666',
          fontSize: 12
        }
      }
    ]
  };
  chart.setOption(option);
  window.addEventListener('resize', () => chart.resize());
};
</script>

<style scoped>
.report-detail-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
  background: #fff;
  box-shadow: 0 0 20px rgba(0, 0, 0, 0.08);
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
}

.report-header {
  text-align: center;
  margin-bottom: 30px;
  padding-bottom: 20px;
  border-bottom: 2px solid #f0f0f0;
}

.report-title {
  font-size: 28px;
  color: #2c3e50;
  margin-bottom: 12px;
  font-weight: 700;
}

.report-meta {
  display: flex;
  justify-content: center;
  gap: 20px;
  color: #666;
  font-size: 14px;
}

.card {
  background: #fff;
  border-radius: 12px;
  padding: 24px;
  margin-bottom: 24px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
  border: 1px solid #eee;
}

.section-title {
  display: flex;
  align-items: center;
  gap: 10px;
  font-size: 20px;
  color: #2c3e50;
  margin-bottom: 20px;
  padding-bottom: 12px;
  border-bottom: 1px solid #f0f0f0;
}

.icon {
  width: 24px;
  height: 24px;
  opacity: 0.8;
}

.info-grid,
.metrics-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
  gap: 16px;
}

.info-item,
.metric-item {
  display: flex;
  flex-direction: column;
}

.info-item label,
.metric-item label {
  font-weight: 600;
  color: #555;
  margin-bottom: 4px;
  font-size: 14px;
}

.info-item span,
.metric-item span {
  color: #333;
  font-size: 16px;
}

.risk-level {
  padding: 4px 12px;
  border-radius: 20px;
  font-weight: 600;
  display: inline-block;
}

.risk-low {
  background-color: #e6f7ee;
  color: #2e7d32;
}

.risk-medium {
  background-color: #fff8e1;
  color: #ff8f00;
}

.risk-high {
  background-color: #ffebee;
  color: #d32f2f;
}

.score-section {
  display: flex;
  flex-wrap: wrap;
  gap: 30px;
  align-items: center;
}

.probability-display {
  text-align: center;
  flex: 1;
  min-width: 200px;
}

.probability-value {
  font-size: 48px;
  font-weight: 700;
  color: #2c3e50;
  margin-bottom: 8px;
}

.probability-label {
  font-size: 16px;
  color: #666;
}

.risk-chart {
  flex: 2;
  min-width: 280px;
  height: 200px;
}

.template-content h3 {
  margin: 20px 0 12px;
  color: #2c3e50;
  font-size: 18px;
  border-left: 4px solid #3498db;
  padding-left: 12px;
}

.template-content div[style] {
  margin-top: 0 !important;
}

.file-list {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.file-item {
  padding: 8px 12px;
  background: #f8f9fa;
  border-radius: 6px;
  border: 1px solid #e9ecef;
}

.file-link {
  color: #3498db;
  text-decoration: none;
  font-weight: 500;
}

.file-link:hover {
  text-decoration: underline;
}

@media (max-width: 768px) {
  .report-detail-container {
    padding: 15px;
  }
  
  .info-grid,
  .metrics-grid {
    grid-template-columns: 1fr;
  }
  
  .score-section {
    flex-direction: column;
    align-items: stretch;
  }
  
  .risk-chart {
    height: 180px;
  }
}
</style>