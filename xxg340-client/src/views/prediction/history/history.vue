<template>
  <div class="prediction-history-container">
    <div class="header">
      <h1>预测历史记录</h1>
      <div class="actions">
        <button class="btn-primary" @click="goToVisualization">
          <img src="https://cdn-icons-png.flaticon.com/512/2972/2972408.png" alt="可视化" class="icon" />
          可视化分析
        </button>
      </div>
    </div>

    <div class="records-list">
      <div 
        v-for="record in predictionRecords" 
        :key="record.id" 
        class="record-card"
        @click="goToReport(record.id)"
      >
        <div class="record-header">
          <div class="time">{{ record.pr_predictiontime }}</div>
          <span 
            class="risk-tag" 
            :class="getRiskClass(record.pr_risklevel)"
          >
            {{ getRiskText(record.pr_risklevel) }}
          </span>
        </div>
        <div class="model-info">
          <div class="model-name">{{ record.wywpm_name }}</div>
          <div class="model-version">v{{ record.nubpm_version }}</div>
        </div>
        <div class="prediction-details">
          <div class="detail-item">
            <span class="label">年龄:</span>
            <span>{{ record.pr_age }}</span>
          </div>
          <div class="detail-item">
            <span class="label">性别:</span>
            <span>{{ record.pr_sex == 2 ? '男' : '女' }}</span>
          </div>
          <div class="detail-item">
            <span class="label">预测概率:</span>
            <span>{{ record.pr_probability }}%</span>
          </div>
          <div class="detail-item">
            <span class="label">类型:</span>
            <span>{{ record.pr_isbatch == 1 ? '单次预测' : '批量预测' }}</span>
          </div>
        </div>
        <div class="action-area">
          <span class="view-report">查看报告 →</span>
        </div>
      </div>
    </div>

    <div v-if="predictionRecords.length == 0" class="empty-state">
      <img src="https://cdn-icons-png.flaticon.com/512/2296/2296318.png" alt="无记录" class="empty-icon" />
      <p>暂无预测记录</p>
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

const router = useRouter();
const route = useRoute();
const globalStore = GlobalStore();

const userInfo = globalStore.userInfo;
const predictionRecords = ref([]);

const goToReport = (id) => {
  router.push({ path: '/prediction/report', query: { id } });
};

const goToVisualization = () => {
  router.push({ path: '/visualization/risktrend' });
};

const getRiskClass = (riskLevel) => {
  if (riskLevel.includes('高')) return 'high-risk';
  if (riskLevel.includes('中')) return 'medium-risk';
  return 'low-risk';
};

const getRiskText = (riskLevel) => {
  if (riskLevel.includes('高')) return '高风险';
  if (riskLevel.includes('中')) return '中风险';
  return '低风险';
};

onMounted(async () => {
  const res = await request('/predictionrecord/index', {
    userid: userInfo.id,
    limit: 999
  }, 'get');
  predictionRecords.value = res.data;
});
</script>

<style scoped>
.prediction-history-container {
  padding: 24px;
  background: #f8f9fa;
  min-height: 100vh;
}

.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 32px;
  padding-bottom: 16px;
  border-bottom: 1px solid #e0e0e0;
}

.header h1 {
  font-size: 28px;
  font-weight: 700;
  color: #1a202c;
  margin: 0;
}

.actions .btn-primary {
  display: flex;
  align-items: center;
  gap: 8px;
  background: #4361ee;
  color: white;
  border: none;
  padding: 10px 20px;
  border-radius: 8px;
  font-size: 16px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  box-shadow: 0 4px 6px rgba(67, 97, 238, 0.2);
}

.actions .btn-primary:hover {
  background: #3a56d4;
  transform: translateY(-2px);
  box-shadow: 0 6px 8px rgba(67, 97, 238, 0.3);
}

.icon {
  width: 20px;
  height: 20px;
}

.records-list {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(350px, 1fr));
  gap: 24px;
}

.record-card {
  background: white;
  border-radius: 12px;
  padding: 20px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
  transition: all 0.3s ease;
  cursor: pointer;
  position: relative;
  overflow: hidden;
}

.record-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 8px 20px rgba(0, 0, 0, 0.12);
}

.record-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 16px;
}

.time {
  font-size: 14px;
  color: #64748b;
  font-weight: 500;
}

.risk-tag {
  padding: 4px 12px;
  border-radius: 20px;
  font-size: 12px;
  font-weight: 600;
  text-transform: uppercase;
}

.low-risk {
  background: #e8f5e9;
  color: #2e7d32;
}

.medium-risk {
  background: #fff8e1;
  color: #f57f17;
}

.high-risk {
  background: #ffebee;
  color: #c62828;
}

.model-info {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-bottom: 16px;
}

.model-name {
  font-size: 18px;
  font-weight: 700;
  color: #1e293b;
}

.model-version {
  background: #f1f5f9;
  color: #475569;
  padding: 2px 8px;
  border-radius: 4px;
  font-size: 12px;
  font-weight: 600;
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

.label {
  font-size: 12px;
  color: #64748b;
  margin-bottom: 4px;
}

.detail-item span:last-child {
  font-size: 14px;
  font-weight: 600;
  color: #1e293b;
}

.action-area {
  text-align: right;
  padding-top: 12px;
  border-top: 1px dashed #e2e8f0;
}

.view-report {
  color: #4361ee;
  font-weight: 600;
  font-size: 14px;
  transition: color 0.2s;
}

.record-card:hover .view-report {
  color: #3a56d4;
}

.empty-state {
  text-align: center;
  padding: 60px 20px;
}

.empty-icon {
  width: 80px;
  height: 80px;
  opacity: 0.6;
  margin-bottom: 20px;
}

.empty-state p {
  font-size: 18px;
  color: #64748b;
  font-weight: 500;
}

/* 斑马纹和悬停效果通过卡片布局实现，无需额外处理 */
</style>