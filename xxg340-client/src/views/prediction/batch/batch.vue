<template>
  <div class="batch-prediction-container">
    <div class="header">
      <h1>心血管疾病风险批量预测</h1>
      <p>上传CSV文件进行批量预测分析，系统将自动生成风险评估结果</p>
    </div>

    <div class="upload-section">
      <div 
        class="upload-area"
        :class="{ 'drag-over': isDragging }"
        @dragover.prevent="handleDragOver"
        @dragleave.prevent="handleDragLeave"
        @drop.prevent="handleDrop"
        @click="triggerFileInput"
      >
        <img 
          src="https://cdn-icons-png.flaticon.com/512/2962/2962408.png" 
          alt="Upload Icon"
          class="upload-icon"
        />
        <h3>拖拽CSV文件到此处或点击选择文件</h3>
        <p class="file-type">支持格式：.csv</p>
        <input 
          type="file" 
          ref="fileInput" 
          accept=".csv" 
          @change="handleFileSelect" 
          style="display: none;"
        />
      </div>

      <div v-if="uploadProgress > 0" class="progress-container">
        <div class="progress-bar">
          <div 
            class="progress-fill" 
            :style="{ width: uploadProgress + '%' }"
          ></div>
        </div>
        <span class="progress-text">{{ uploadProgress }}%</span>
      </div>

      <div v-if="predictionResult" class="result-section">
        <div class="result-summary">
          <h2>预测结果摘要</h2>
          <div class="summary-stats">
            <div class="stat-card">
              <div class="stat-value">{{ predictionResult.total_records || 0 }}</div>
              <div class="stat-label">总记录数</div>
            </div>
            <div class="stat-card">
              <div class="stat-value">{{ predictionResult.high_risk_count || 0 }}</div>
              <div class="stat-label">高风险数量</div>
            </div>
            <div class="stat-card">
              <div class="stat-value">{{ predictionResult.medium_risk_count || 0 }}</div>
              <div class="stat-label">中风险数量</div>
            </div>
            <div class="stat-card">
              <div class="stat-value">{{ predictionResult.low_risk_count || 0 }}</div>
              <div class="stat-label">低风险数量</div>
            </div>
          </div>
        </div>

        <div class="result-actions">
          <el-button 
            type="primary" 
            @click="downloadResultFile"
            :disabled="!hasResultFile"
          >
            下载结果文件
          </el-button>
          <el-button 
            type="success" 
            @click="viewHistory"
          >
            查看历史记录
          </el-button>
        </div>

        <div v-if="hasResultFile" class="result-file-info">
          <p><strong>结果文件：</strong>{{ resultFileName }}</p>
          <a 
            :href="resultFileUrl" 
            target="_blank" 
            class="file-link"
          >
            {{ resultFileName }}
          </a>
        </div>
      </div>
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
import { ElMessage, ElMessageBox } from 'element-plus'

const router = useRouter();
const route = useRoute();
const globalStore = GlobalStore();

const userInfo = globalStore.userInfo;

// 文件上传相关
const fileInput = ref(null);
const isDragging = ref(false);
const uploadProgress = ref(0);
const predictionResult = ref(null);
const resultFileUrl = ref('');
const resultFileName = ref('');

const hasResultFile = computed(() => {
  return predictionResult.value && predictionResult.value.pr_resultfile && 
         predictionResult.value.pr_resultfile.length > 0;
});

// 获取预测模型列表（用于获取pm_id）
const predictionModels = ref([]);

const fetchPredictionModels = async () => {
  try {
    const res = await request('/predictionmodel/index', {}, 'get');
    predictionModels.value = res;
  } catch (error) {
    ElMessage.error('获取预测模型失败');
  }
};

// 触发文件选择
const triggerFileInput = () => {
  fileInput.value.click();
};

// 处理文件选择
const handleFileSelect = async (event) => {
  const file = event.target.files[0];
  if (!file) return;
  
  if (!file.name.endsWith('.csv')) {
    ElMessage.error('请上传CSV格式文件');
    return;
  }
  
  await uploadFile(file);
};

// 拖拽事件处理
const handleDragOver = () => {
  isDragging.value = true;
};

const handleDragLeave = () => {
  isDragging.value = false;
};

const handleDrop = (event) => {
  isDragging.value = false;
  const files = event.dataTransfer.files;
  if (files.length == 0) return;
  
  const file = files[0];
  if (!file.name.endsWith('.csv')) {
    ElMessage.error('请上传CSV格式文件');
    return;
  }
  
  uploadFile(file);
};

// 上传文件并进行批量预测
const uploadFile = async (file) => {
  // 重置状态
  uploadProgress.value = 0;
  predictionResult.value = null;
  resultFileUrl.value = '';
  resultFileName.value = '';
  
  // 显示上传进度（模拟）
  const progressInterval = setInterval(() => {
    if (uploadProgress.value < 90) {
      uploadProgress.value += 10;
    }
  }, 200);
  
  try {
    // 确保有预测模型
    if (predictionModels.value.length == 0) {
      await fetchPredictionModels();
    }
    
    if (predictionModels.value.length == 0) {
      ElMessage.error('没有可用的预测模型');
      clearInterval(progressInterval);
      return;
    }
    
    // 使用第一个模型（实际业务中可能需要用户选择）
    const pmId = predictionModels.value[0].id;
    
    // 创建FormData
    const formData = new FormData();
    formData.append('pr_batchfile', file);
    formData.append('pm_id', pmId);
    formData.append('pr_isbatch', 2); // 批量预测
    
    // 调用后端接口
    const res = await request('/predictionrecord/store', formData, 'post');
    
    // 清除进度
    clearInterval(progressInterval);
    uploadProgress.value = 100;
    
    // 设置结果
    predictionResult.value = res;
    
    // 处理结果文件
    if (res.pr_resultfile && res.pr_resultfile.length > 0) {
      resultFileUrl.value = res.pr_resultfile[0].url;
      resultFileName.value = res.pr_resultfile[0].name;
    }
    
    ElMessage.success('批量预测完成！');
  } catch (error) {
    clearInterval(progressInterval);
    uploadProgress.value = 0;
    ElMessage.error('批量预测失败，请重试');
    console.error('Upload error:', error);
  }
};

// 下载结果文件
const downloadResultFile = () => {
  if (!hasResultFile.value) return;
  
  const link = document.createElement('a');
  link.href = resultFileUrl.value;
  link.download = resultFileName.value;
  document.body.appendChild(link);
  link.click();
  document.body.removeChild(link);
};

// 查看历史记录
const viewHistory = () => {
  router.push({ path: '/prediction/history', query: undefined });
};

onMounted(async () => {
  await fetchPredictionModels();
});
</script>

<style scoped>
.batch-prediction-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
}

.header {
  text-align: center;
  margin-bottom: 40px;
}

.header h1 {
  color: #1976d2;
  font-size: 2.5rem;
  margin-bottom: 12px;
  font-weight: 600;
}

.header p {
  color: #666;
  font-size: 1.1rem;
  line-height: 1.6;
}

.upload-section {
  display: flex;
  flex-direction: column;
  gap: 30px;
}

.upload-area {
  border: 2px dashed #1976d2;
  border-radius: 12px;
  padding: 40px 20px;
  text-align: center;
  cursor: pointer;
  transition: all 0.3s ease;
  background-color: #f8fbff;
}

.upload-area:hover,
.upload-area.drag-over {
  background-color: #e3f2fd;
  border-color: #0d47a1;
}

.upload-icon {
  width: 64px;
  height: 64px;
  margin-bottom: 20px;
  opacity: 0.8;
}

.upload-area h3 {
  color: #1976d2;
  margin-bottom: 10px;
  font-size: 1.3rem;
}

.file-type {
  color: #666;
  font-size: 0.9rem;
}

.progress-container {
  display: flex;
  align-items: center;
  gap: 15px;
  margin-top: 20px;
}

.progress-bar {
  flex: 1;
  height: 8px;
  background-color: #e0e0e0;
  border-radius: 4px;
  overflow: hidden;
}

.progress-fill {
  height: 100%;
  background: linear-gradient(90deg, #2196f3, #1976d2);
  border-radius: 4px;
  transition: width 0.3s ease;
}

.progress-text {
  font-weight: 600;
  color: #1976d2;
  min-width: 40px;
}

.result-section {
  background: white;
  border-radius: 12px;
  padding: 30px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
  border: 1px solid #e0e0e0;
}

.result-section h2 {
  color: #1976d2;
  margin-bottom: 25px;
  font-size: 1.8rem;
  text-align: center;
}

.summary-stats {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 20px;
  margin-bottom: 30px;
}

.stat-card {
  background: linear-gradient(135deg, #f5f9ff, #e3f2fd);
  border-radius: 10px;
  padding: 20px;
  text-align: center;
  border: 1px solid #bbdefb;
}

.stat-value {
  font-size: 2.2rem;
  font-weight: 700;
  color: #1976d2;
  margin-bottom: 8px;
}

.stat-label {
  color: #555;
  font-size: 1rem;
}

.result-actions {
  display: flex;
  justify-content: center;
  gap: 20px;
  margin: 30px 0;
}

.result-file-info {
  text-align: center;
  margin-top: 20px;
  padding-top: 20px;
  border-top: 1px solid #eee;
}

.file-link {
  color: #1976d2;
  text-decoration: none;
  font-weight: 600;
  display: inline-block;
  margin-top: 8px;
}

.file-link:hover {
  text-decoration: underline;
}

@media (max-width: 768px) {
  .batch-prediction-container {
    padding: 15px;
  }
  
  .header h1 {
    font-size: 2rem;
  }
  
  .result-actions {
    flex-direction: column;
    align-items: center;
  }
  
  .el-button {
    width: 200px;
  }
}
</style>