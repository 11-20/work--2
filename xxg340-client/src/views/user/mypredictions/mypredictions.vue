<template>
  <div class="mypredictions-container">
    <div class="header">
      <h1>我的预测记录</h1>
      <p>查看您过往的心血管疾病风险预测结果</p>
    </div>

    <div class="records-list" v-if="predictionRecords.length > 0">
      <div 
        v-for="record in predictionRecords" 
        :key="record.id" 
        class="record-card"
        @click="goToReport(record.id)"
      >
        <div class="card-header">
          <div class="model-info">
            <span class="model-name">{{ record.wywpm_name || '未知模型' }}</span>
            <span class="model-version">v{{ record.nubpm_version || '1.0' }}</span>
          </div>
          <div class="risk-badge" :class="getRiskClass(record.pr_risklevel)">
            {{ record.pr_risklevel || '未知风险' }}
          </div>
        </div>
        
        <div class="prediction-time">
          预测时间：{{ record.pr_predictiontime }}
        </div>
        
        <div class="prediction-details">
          <div class="detail-item">
            <span class="label">年龄：</span>
            <span>{{ record.pr_age }} 岁</span>
          </div>
          <div class="detail-item">
            <span class="label">性别：</span>
            <span>{{ record.pr_sex == 2 ? '男' : record.pr_sex == 3 ? '女' : '未知' }}</span>
          </div>
          <div class="detail-item">
            <span class="label">预测概率：</span>
            <span>{{ record.pr_probability }}%</span>
          </div>
          <div class="detail-item">
            <span class="label">预测类型：</span>
            <span>{{ record.pr_isbatch == 1 ? '单次预测' : '批量预测' }}</span>
          </div>
        </div>
        
        <div class="prediction-summary">
          <div class="summary-item">
            <strong>胸痛类型：</strong>
            <span>{{ record.pr_cp || '未提供' }}</span>
          </div>
          <div class="summary-item">
            <strong>静息血压：</strong>
            <span>{{ record.pr_trestbps || '未提供' }}</span>
          </div>
          <div class="summary-item">
            <strong>血清胆固醇：</strong>
            <span>{{ record.pr_chol || '未提供' }}</span>
          </div>
        </div>
      </div>
    </div>

    <div class="empty-state" v-else>
      <img src="https://cdn-icons-png.flaticon.com/512/2296/2296837.png" alt="无记录图标" />
      <h3>暂无预测记录</h3>
      <p>您还没有进行过心血管疾病风险预测，点击下方按钮开始您的第一次预测吧！</p>
      <el-button type="primary" @click="goToPredict">立即预测</el-button>
    </div>
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
import { ElMessage } from 'element-plus'

const router = useRouter();
const route = useRoute();
const globalStore = GlobalStore();

const userInfo = globalStore.userInfo

const predictionRecords = ref([]);

const goToReport = (id) => {
  router.push({ path: '/prediction/report', query: { id } })
}

const goToPredict = () => {
  router.push({ path: '/prediction/create' })
}

const getRiskClass = (riskLevel) => {
  if (!riskLevel) return 'unknown';
  const level = riskLevel.toLowerCase();
  if (level.includes('高') || level.includes('high')) return 'high-risk';
  if (level.includes('中') || level.includes('medium')) return 'medium-risk';
  if (level.includes('低') || level.includes('low')) return 'low-risk';
  return 'unknown';
}

onMounted(async () => {
  const res = await request('/predictionrecord/index', {
    userid: userInfo.id,
    limit: 999
  }, 'get');
  predictionRecords.value = res.data;
});
</script>

<style scoped>
.mypredictions-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
  min-height: calc(100vh - 120px);
}

.header {
  text-align: center;
  margin-bottom: 30px;
}

.header h1 {
  font-size: 28px;
  font-weight: 700;
  color: #1a365d;
  margin-bottom: 8px;
}

.header p {
  color: #64748b;
  font-size: 16px;
}

.records-list {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(350px, 1fr));
  gap: 24px;
}

.record-card {
  background: white;
  border-radius: 12px;
  padding: 24px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
  transition: all 0.3s ease;
  cursor: pointer;
  border: 1px solid #e2e8f0;
}

.record-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 6px 16px rgba(0, 0, 0, 0.12);
  border-color: #cbd5e1;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 16px;
  padding-bottom: 12px;
  border-bottom: 1px solid #f1f5f9;
}

.model-info {
  display: flex;
  flex-direction: column;
}

.model-name {
  font-weight: 600;
  font-size: 18px;
  color: #1e40af;
  margin-bottom: 4px;
}

.model-version {
  font-size: 12px;
  color: #64748b;
  background: #dbeafe;
  padding: 2px 8px;
  border-radius: 12px;
  display: inline-block;
}

.risk-badge {
  padding: 4px 12px;
  border-radius: 20px;
  font-size: 12px;
  font-weight: 600;
  text-transform: uppercase;
}

.high-risk {
  background: #fee2e2;
  color: #dc2626;
}

.medium-risk {
  background: #ffedd5;
  color: #ea580c;
}

.low-risk {
  background: #dcfce7;
  color: #16a34a;
}

.unknown {
  background: #e2e8f0;
  color: #475569;
}

.prediction-time {
  color: #64748b;
  font-size: 14px;
  margin-bottom: 16px;
  font-style: italic;
}

.prediction-details {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 12px;
  margin-bottom: 16px;
}

.detail-item {
  display: flex;
  flex-direction: column;
}

.detail-item .label {
  font-size: 12px;
  color: #64748b;
  margin-bottom: 4px;
}

.detail-item span {
  font-weight: 500;
  color: #1e293b;
}

.prediction-summary {
  background: #f8fafc;
  padding: 16px;
  border-radius: 8px;
  margin-top: 16px;
}

.summary-item {
  display: flex;
  margin-bottom: 8px;
  font-size: 14px;
}

.summary-item:last-child {
  margin-bottom: 0;
}

.summary-item strong {
  color: #334155;
  min-width: 100px;
}

.summary-item span {
  color: #475569;
  flex: 1;
  word-break: break-word;
}

.empty-state {
  text-align: center;
  padding: 60px 20px;
}

.empty-state img {
  width: 120px;
  height: 120px;
  margin-bottom: 24px;
  opacity: 0.7;
}

.empty-state h3 {
  font-size: 24px;
  color: #1e293b;
  margin-bottom: 12px;
}

.empty-state p {
  color: #64748b;
  max-width: 500px;
  margin: 0 auto 24px;
  line-height: 1.6;
}

:deep(.el-button) {
  background: #3b82f6;
  border-color: #3b82f6;
  color: white;
  padding: 10px 24px;
  font-size: 16px;
  border-radius: 8px;
}

:deep(.el-button:hover) {
  background: #2563eb;
  border-color: #2563eb;
}
</style>