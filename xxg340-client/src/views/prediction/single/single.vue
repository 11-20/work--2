<template>
  <div class="single-prediction-page">
    <div class="container">
      <div class="form-section">
        <h2>心血管疾病风险预测</h2>
        <el-form
          ref="predictionFormRef"
          :model="formData"
          label-position="top"
          class="prediction-form"
        >
          <!-- 模型选择 -->
          <el-form-item label="预测模型" prop="pm_id" required>
            <el-select
              v-model="formData.pm_id"
              placeholder="请选择预测模型"
              class="model-select"
            >
              <el-option
                v-for="model in predictionModels"
                :key="model.id"
                :label="`${model.wywpm_name} (v${model.nubpm_version})`"
                :value="model.id"
              />
            </el-select>
          </el-form-item>

          <!-- 基础信息 -->
          <div class="form-row">
            <el-form-item label="年龄" prop="pr_age" required>
              <el-input
                v-model="formData.pr_age"
                type="number"
                placeholder="请输入年龄"
              />
            </el-form-item>
            <el-form-item label="性别" prop="pr_sex" required>
              <el-select
                v-model="formData.pr_sex"
                placeholder="请选择性别"
                class="gender-select"
              >
                <el-option :label="'男'" :value="2" />
                <el-option :label="'女'" :value="3" />
              </el-select>
            </el-form-item>
          </div>

          <!-- 医疗指标 -->
          <div class="form-grid">
            <el-form-item label="胸痛类型" prop="pr_cp" required>
              <el-input v-model="formData.pr_cp" placeholder="例如：典型心绞痛" />
            </el-form-item>
            <el-form-item label="静息血压 (mm Hg)" prop="pr_trestbps" required>
              <el-input v-model="formData.pr_trestbps" placeholder="例如：120" />
            </el-form-item>
            <el-form-item label="血清胆固醇 (mg/dl)" prop="pr_chol" required>
              <el-input v-model="formData.pr_chol" placeholder="例如：240" />
            </el-form-item>
            <el-form-item label="空腹血糖 (>120 mg/dl)" prop="pr_fbs" required>
              <el-input v-model="formData.pr_fbs" placeholder="1=是, 0=否" />
            </el-form-item>
            <el-form-item label="静息心电图结果" prop="pr_restecg" required>
              <el-input v-model="formData.pr_restecg" placeholder="例如：正常" />
            </el-form-item>
            <el-form-item label="最大心率" prop="pr_thalach" required>
              <el-input v-model="formData.pr_thalach" placeholder="例如：150" />
            </el-form-item>
            <el-form-item label="运动诱发心绞痛" prop="pr_exang" required>
              <el-input v-model="formData.pr_exang" placeholder="1=是, 0=否" />
            </el-form-item>
            <el-form-item label="ST段压低" prop="pr_oldpeak" required>
              <el-input v-model="formData.pr_oldpeak" placeholder="例如：2.3" />
            </el-form-item>
            <el-form-item label="ST段峰值运动斜率" prop="pr_slope" required>
              <el-input v-model="formData.pr_slope" placeholder="例如：上斜" />
            </el-form-item>
            <el-form-item label="主要血管数量" prop="pr_ca" required>
              <el-input v-model="formData.pr_ca" placeholder="例如：0" />
            </el-form-item>
            <el-form-item label="地中海贫血" prop="pr_thal" required>
              <el-input v-model="formData.pr_thal" placeholder="例如：正常" />
            </el-form-item>
          </div>

          <!-- 提交按钮 -->
          <div class="submit-section">
            <el-button
              type="primary"
              size="large"
              @click="submitPrediction"
              :loading="submitting"
            >
              {{ submitting ? '预测中...' : '开始预测' }}
            </el-button>
          </div>
        </el-form>
      </div>

      <!-- 结果展示区 -->
      <div v-if="showResult" class="result-section">
        <div class="result-card">
          <h3>预测结果</h3>
          <div class="risk-level">
            <span class="risk-label">风险等级:</span>
            <span
              class="risk-value"
              :class="getRiskClass(formData.pr_risklevel)"
            >
              {{ formData.pr_risklevel }}
            </span>
          </div>
          <div class="probability">
            <span class="prob-label">预测概率:</span>
            <span class="prob-value">{{ formData.pr_probability }}%</span>
          </div>
          <div class="prediction-time">
            <span class="time-label">预测时间:</span>
            <span class="time-value">{{ formData.pr_predictiontime }}</span>
          </div>
          <div class="model-info">
            <span class="model-label">使用模型:</span>
            <span class="model-value">
              {{ selectedModelName }} (v{{ selectedModelVersion }})
            </span>
          </div>
          <div class="chart-container" ref="chartRef"></div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import {
  ref,
  reactive,
  onMounted,
  nextTick
} from 'vue';

import { request } from "@/http/index";
import { GlobalStore } from "@/stores";
import { useRoute, useRouter } from "vue-router";
import { ElMessage, ElMessageBox } from 'element-plus'
import * as echarts from "echarts";

const router = useRouter();
const route = useRoute();
const globalStore = GlobalStore();

const userInfo = globalStore.userInfo;

// 表单数据
const formData = reactive({
  pm_id: null,
  pr_age: '',
  pr_sex: null,
  pr_cp: '',
  pr_trestbps: '',
  pr_chol: '',
  pr_fbs: '',
  pr_restecg: '',
  pr_thalach: '',
  pr_exang: '',
  pr_oldpeak: '',
  pr_slope: '',
  pr_ca: '',
  pr_thal: '',
  pr_risklevel: '',
  pr_probability: '',
  pr_predictiontime: '',
  pr_batchfile: [],
  pr_resultfile: [],
  pr_isbatch: 1, // 单次预测
});

// 状态管理
const predictionModels = ref([]);
const submitting = ref(false);
const showResult = ref(false);
const chartRef = ref(null);

// 模型信息缓存
const selectedModelName = ref('');
const selectedModelVersion = ref('');

// 获取预测模型列表
const fetchPredictionModels = async () => {
  const res = await request('/predictionmodel/index', {
    limit: 999,
    pm_status: 2 // 只获取启用的模型
  }, 'get');
  predictionModels.value = res.data;
};

// 监听模型选择变化
watch(() => formData.pm_id, (newId) => {
  if (newId) {
    const model = predictionModels.value.find(m => m.id == newId);
    if (model) {
      selectedModelName.value = model.wywpm_name;
      selectedModelVersion.value = model.nubpm_version;
    }
  }
});

// 提交预测
const submitPrediction = async () => {
  // 基础验证
  if (!formData.pm_id) {
    ElMessage.warning('请选择预测模型');
    return;
  }
  if (!formData.pr_age || !formData.pr_sex) {
    ElMessage.warning('请填写必填字段');
    return;
  }

  submitting.value = true;
  
  try {
    // 添加用户ID和批量标志
    const submitData = {
      ...formData,
      userid: userInfo.id,
      pr_isbatch: 1
    };
    
    const res = await request('/predictionrecord/store', submitData, 'post');
    
    // 更新表单数据（包含后端返回的结果）
    Object.assign(formData, res);
    
    // 显示结果
    showResult.value = true;
    
    // 显示成功提示
    ElMessage.success('预测成功！结果已生成');
    
    // 初始化图表
    await nextTick();
    initChart();
    
  } catch (error) {
    ElMessage.error('预测失败，请重试');
    console.error(error);
  } finally {
    submitting.value = false;
  }
};

// 初始化图表
const initChart = () => {
  if (!chartRef.value) return;
  
  const chart = echarts.init(chartRef.value);
  
  // 根据风险等级设置颜色
  let riskColor = '#67C23A'; // 低风险
  if (formData.pr_risklevel.includes('中')) {
    riskColor = '#E6A23C';
  } else if (formData.pr_risklevel.includes('高')) {
    riskColor = '#F56C6C';
  }
  
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
          fontSize: 24,
          color: riskColor
        },
        data: [
          {
            value: parseFloat(formData.pr_probability) || 0,
            name: '心血管疾病风险'
          }
        ],
        axisLine: {
          lineStyle: {
            width: 15,
            color: [
              [0.3, '#67C23A'],
              [0.7, '#E6A23C'],
              [1, '#F56C6C']
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
};

// 风险等级样式类
const getRiskClass = (riskLevel) => {
  if (!riskLevel) return '';
  if (riskLevel.includes('高')) return 'high-risk';
  if (riskLevel.includes('中')) return 'medium-risk';
  return 'low-risk';
};

onMounted(async () => {
  await fetchPredictionModels();
});
</script>

<style scoped>
.single-prediction-page {
  background: linear-gradient(135deg, #1a2a6c, #2a4d8e, #3a6ea5);
  min-height: 100vh;
  padding: 2rem;
}

.container {
  max-width: 1400px;
  margin: 0 auto;
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 2rem;
}

.form-section {
  background: rgba(255, 255, 255, 0.95);
  border-radius: 20px;
  padding: 2.5rem;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.2);
  backdrop-filter: blur(10px);
}

.form-section h2 {
  color: #1a2a6c;
  margin-bottom: 2rem;
  font-size: 1.8rem;
  text-align: center;
  font-weight: 700;
}

.prediction-form {
  max-width: 100%;
}

.model-select,
.gender-select {
  width: 100%;
}

.form-row {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1.5rem;
  margin-bottom: 1.5rem;
}

.form-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
  gap: 1.2rem;
  margin-bottom: 2rem;
}

.submit-section {
  text-align: center;
  margin-top: 2rem;
}

.submit-section .el-button {
  padding: 12px 40px;
  font-size: 1.1rem;
  border-radius: 50px;
  background: linear-gradient(45deg, #1a2a6c, #3a6ea5);
  border: none;
  transition: all 0.3s ease;
}

.submit-section .el-button:hover {
  transform: translateY(-2px);
  box-shadow: 0 5px 15px rgba(26, 42, 108, 0.4);
}

.result-section {
  display: flex;
  align-items: center;
  justify-content: center;
}

.result-card {
  background: rgba(255, 255, 255, 0.95);
  border-radius: 20px;
  padding: 2.5rem;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.2);
  backdrop-filter: blur(10px);
  width: 100%;
  max-width: 500px;
}

.result-card h3 {
  color: #1a2a6c;
  margin-bottom: 2rem;
  font-size: 1.6rem;
  text-align: center;
  font-weight: 700;
}

.risk-level,
.probability,
.prediction-time,
.model-info {
  display: flex;
  justify-content: space-between;
  margin-bottom: 1.5rem;
  padding-bottom: 1rem;
  border-bottom: 1px solid #eee;
}

.risk-label,
.prob-label,
.time-label,
.model-label {
  font-weight: 600;
  color: #555;
  font-size: 1.1rem;
}

.risk-value,
.prob-value,
.time-value,
.model-value {
  font-weight: 700;
  font-size: 1.2rem;
}

.risk-value.low-risk {
  color: #67C23A;
}

.risk-value.medium-risk {
  color: #E6A23C;
}

.risk-value.high-risk {
  color: #F56C6C;
}

.chart-container {
  height: 300px;
  margin-top: 2rem;
}

/* 输入框聚焦效果 */
.el-input__wrapper,
.el-select__wrapper {
  transition: all 0.3s ease;
  border-radius: 12px !important;
}

.el-input__wrapper:focus-within,
.el-select__wrapper:focus-within {
  box-shadow: 0 0 0 2px #3a6ea5 !important;
  transform: scale(1.02);
}

/* 响应式设计 */
@media (max-width: 1200px) {
  .container {
    grid-template-columns: 1fr;
  }
  
  .form-grid {
    grid-template-columns: repeat(auto-fill, minmax(150px, 1fr));
  }
}

@media (max-width: 768px) {
  .single-prediction-page {
    padding: 1rem;
  }
  
  .container {
    gap: 1.5rem;
  }
  
  .form-section,
  .result-card {
    padding: 1.5rem;
  }
  
  .form-row {
    grid-template-columns: 1fr;
  }
  
  .form-grid {
    grid-template-columns: 1fr;
  }
}
</style>