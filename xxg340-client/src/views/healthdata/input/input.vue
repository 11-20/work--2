<template>
  <div class="health-data-input-container">
    <div class="header">
      <h1>健康数据录入</h1>
      <p>请准确填写您的心血管健康相关指标，系统将为您生成个性化风险评估报告</p>
    </div>

    <el-form 
      ref="healthDataForm" 
      :model="formData" 
      :rules="rules" 
      label-position="top"
      class="health-form"
    >
      <!-- 基础信息 -->
      <div class="form-section">
        <h2>基础生理指标</h2>
        <div class="form-row">
          <el-form-item label="记录日期" prop="hd_date">
            <el-date-picker
              v-model="formData.hd_date"
              type="date"
              placeholder="选择日期"
              format="YYYY-MM-DD"
              value-format="YYYY-MM-DD"
              style="width: 100%"
            />
          </el-form-item>
          
          <el-form-item label="身高 (cm)" prop="hd_height">
            <el-input-number
              v-model="formData.hd_height"
              :min="100"
              :max="250"
              controls-position="right"
              style="width: 100%"
            />
          </el-form-item>
          
          <el-form-item label="体重 (kg)" prop="hd_weight">
            <el-slider
              v-model="formData.hd_weight"
              :min="30"
              :max="200"
              show-input
              show-input-controls
              input-size="small"
              style="width: 100%"
            />
          </el-form-item>
        </div>
      </div>

      <!-- 血压指标 -->
      <div class="form-section">
        <h2>血压指标</h2>
        <div class="form-row">
          <el-form-item label="收缩压 (mmHg)" prop="hd_sbp">
            <el-input-number
              v-model="formData.hd_sbp"
              :min="70"
              :max="250"
              controls-position="right"
              style="width: 100%"
            />
          </el-form-item>
          
          <el-form-item label="舒张压 (mmHg)" prop="hd_dbp">
            <el-input-number
              v-model="formData.hd_dbp"
              :min="40"
              :max="150"
              controls-position="right"
              style="width: 100%"
            />
          </el-form-item>
        </div>
      </div>

      <!-- 血液指标 -->
      <div class="form-section">
        <h2>血液生化指标</h2>
        <div class="form-row">
          <el-form-item label="血糖水平 (mmol/L)" prop="hd_glucose">
            <el-input-number
              v-model="formData.hd_glucose"
              :min="2.0"
              :max="30.0"
              :step="0.1"
              controls-position="right"
              style="width: 100%"
            />
          </el-form-item>
          
          <el-form-item label="总胆固醇 (mmol/L)" prop="hd_cholesterol">
            <el-input-number
              v-model="formData.hd_cholesterol"
              :min="2.0"
              :max="10.0"
              :step="0.1"
              controls-position="right"
              style="width: 100%"
            />
          </el-form-item>
          
          <el-form-item label="高密度脂蛋白 (mmol/L)" prop="hd_hdl">
            <el-input-number
              v-model="formData.hd_hdl"
              :min="0.5"
              :max="3.0"
              :step="0.1"
              controls-position="right"
              style="width: 100%"
            />
          </el-form-item>
          
          <el-form-item label="低密度脂蛋白 (mmol/L)" prop="hd_ldl">
            <el-input-number
              v-model="formData.hd_ldl"
              :min="0.5"
              :max="6.0"
              :step="0.1"
              controls-position="right"
              style="width: 100%"
            />
          </el-form-item>
          
          <el-form-item label="甘油三酯 (mmol/L)" prop="hd_triglycerides">
            <el-input-number
              v-model="formData.hd_triglycerides"
              :min="0.2"
              :max="10.0"
              :step="0.1"
              controls-position="right"
              style="width: 100%"
            />
          </el-form-item>
        </div>
      </div>

      <!-- 生活习惯 -->
      <div class="form-section">
        <h2>生活习惯</h2>
        <div class="form-row">
          <el-form-item label="是否吸烟" prop="hd_smoking">
            <el-select v-model="formData.hd_smoking" placeholder="请选择" style="width: 100%">
              <el-option :value="1" label="否" />
              <el-option :value="2" label="是" />
            </el-select>
          </el-form-item>
          
          <el-form-item label="是否饮酒" prop="hd_alcohol">
            <el-select v-model="formData.hd_alcohol" placeholder="请选择" style="width: 100%">
              <el-option :value="1" label="否" />
              <el-option :value="2" label="是" />
            </el-select>
          </el-form-item>
          
          <el-form-item label="每周运动时长 (小时)" prop="hd_exercise">
            <el-slider
              v-model="formData.hd_exercise"
              :min="0"
              :max="20"
              :step="0.5"
              show-input
              show-input-controls
              input-size="small"
              style="width: 100%"
            />
          </el-form-item>
        </div>
      </div>

      <!-- BMI计算显示 -->
      <div class="bmi-display" v-if="computedBMI > 0">
        <div class="bmi-value">{{ computedBMI.toFixed(1) }}</div>
        <div class="bmi-label">BMI指数</div>
        <div class="bmi-category" :class="bmiCategoryClass">
          {{ bmiCategory }}
        </div>
      </div>

      <div class="form-actions">
        <el-button type="primary" @click="submitForm" :loading="submitting">
          提交健康数据
        </el-button>
        <el-button @click="resetForm">重置表单</el-button>
      </div>
    </el-form>
  </div>
</template>

<script setup lang="ts">
import { 
  ref, 
  reactive, 
  onMounted, 
  computed,
  watch
} from 'vue';

import { request } from "@/http/index";
import { GlobalStore } from "@/stores";
import { useRoute, useRouter } from "vue-router";
import { ElMessage, ElMessageBox } from 'element-plus'

const router = useRouter();
const route = useRoute();
const globalStore = GlobalStore();

const userInfo = globalStore.userInfo;

// 表单数据
const formData = reactive({
  hd_date: '',
  hd_weight: 70,
  hd_height: 170,
  hd_bmi: '',
  hd_sbp: 120,
  hd_dbp: 80,
  hd_glucose: 5.0,
  hd_cholesterol: 4.5,
  hd_hdl: 1.2,
  hd_ldl: 2.8,
  hd_triglycerides: 1.5,
  hd_smoking: 1,
  hd_exercise: 3.0,
  hd_alcohol: 1
});

// 计算BMI
const computedBMI = computed(() => {
  if (formData.hd_height && formData.hd_weight) {
    const heightInMeters = formData.hd_height / 100;
    return formData.hd_weight / (heightInMeters * heightInMeters);
  }
  return 0;
});

// BMI分类
const bmiCategory = computed(() => {
  const bmi = computedBMI.value;
  if (bmi < 18.5) return '体重过轻';
  if (bmi < 24) return '正常范围';
  if (bmi < 28) return '超重';
  return '肥胖';
});

const bmiCategoryClass = computed(() => {
  const bmi = computedBMI.value;
  if (bmi < 18.5) return 'underweight';
  if (bmi < 24) return 'normal';
  if (bmi < 28) return 'overweight';
  return 'obese';
});

// 表单验证规则
const rules = {
  hd_date: [{ required: true, message: '请选择记录日期', trigger: 'change' }],
  hd_weight: [{ required: true, message: '请输入体重', trigger: 'blur' }],
  hd_height: [{ required: true, message: '请输入身高', trigger: 'blur' }],
  hd_sbp: [{ required: true, message: '请输入收缩压', trigger: 'blur' }],
  hd_dbp: [{ required: true, message: '请输入舒张压', trigger: 'blur' }],
  hd_glucose: [{ required: true, message: '请输入血糖水平', trigger: 'blur' }],
  hd_cholesterol: [{ required: true, message: '请输入总胆固醇', trigger: 'blur' }],
  hd_hdl: [{ required: true, message: '请输入高密度脂蛋白', trigger: 'blur' }],
  hd_ldl: [{ required: true, message: '请输入低密度脂蛋白', trigger: 'blur' }],
  hd_triglycerides: [{ required: true, message: '请输入甘油三酯', trigger: 'blur' }],
  hd_smoking: [{ required: true, message: '请选择是否吸烟', trigger: 'change' }],
  hd_exercise: [{ required: true, message: '请输入每周运动时长', trigger: 'blur' }],
  hd_alcohol: [{ required: true, message: '请选择是否饮酒', trigger: 'change' }]
};

const healthDataForm = ref(null);
const submitting = ref(false);

// 监听BMI变化并更新表单
watch(computedBMI, (newBMI) => {
  formData.hd_bmi = newBMI.toString();
});

// 重置表单
const resetForm = () => {
  healthDataForm.value.resetFields();
  Object.assign(formData, {
    hd_date: '',
    hd_weight: 70,
    hd_height: 170,
    hd_bmi: '',
    hd_sbp: 120,
    hd_dbp: 80,
    hd_glucose: 5.0,
    hd_cholesterol: 4.5,
    hd_hdl: 1.2,
    hd_ldl: 2.8,
    hd_triglycerides: 1.5,
    hd_smoking: 1,
    hd_exercise: 3.0,
    hd_alcohol: 1
  });
};

// 提交表单
const submitForm = async () => {
  if (!healthDataForm.value) return;
  
  await healthDataForm.value.validate(async (valid) => {
    if (valid) {
      submitting.value = true;
      
      try {
        // 确保BMI已计算
        formData.hd_bmi = computedBMI.value.toString();
        
        const res = await request('/healthdata/store', {
          hd_date: formData.hd_date,
          hd_weight: formData.hd_weight.toString(),
          hd_height: formData.hd_height.toString(),
          hd_bmi: formData.hd_bmi,
          hd_sbp: formData.hd_sbp.toString(),
          hd_dbp: formData.hd_dbp.toString(),
          hd_glucose: formData.hd_glucose.toString(),
          hd_cholesterol: formData.hd_cholesterol.toString(),
          hd_hdl: formData.hd_hdl.toString(),
          hd_ldl: formData.hd_ldl.toString(),
          hd_triglycerides: formData.hd_triglycerides.toString(),
          hd_smoking: formData.hd_smoking,
          hd_exercise: formData.hd_exercise.toString(),
          hd_alcohol: formData.hd_alcohol
        }, 'post');
        
        ElMessage.success('健康数据提交成功！');
        router.push({ path: '/healthdata/list', query: undefined });
      } catch (error) {
        ElMessage.error('提交失败，请重试');
        console.error(error);
      } finally {
        submitting.value = false;
      }
    }
  });
};

onMounted(() => {
  // 设置默认日期为今天
  const today = new Date();
  formData.hd_date = today.toISOString().split('T')[0];
});
</script>

<style scoped>
.health-data-input-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 2rem;
  background: linear-gradient(135deg, #f8f9fa 0%, #e9f7ef 100%);
  min-height: 100vh;
}

.header {
  text-align: center;
  margin-bottom: 2.5rem;
}

.header h1 {
  color: #2e7d32;
  font-size: 2.5rem;
  margin-bottom: 1rem;
  font-weight: 600;
}

.header p {
  color: #555;
  font-size: 1.1rem;
  max-width: 600px;
  margin: 0 auto;
  line-height: 1.6;
}

.health-form {
  background: white;
  border-radius: 16px;
  padding: 2.5rem;
  box-shadow: 0 10px 30px rgba(46, 125, 50, 0.15);
}

.form-section {
  margin-bottom: 2.5rem;
}

.form-section h2 {
  color: #2e7d32;
  margin-bottom: 1.5rem;
  padding-bottom: 0.8rem;
  border-bottom: 2px solid #e8f5e9;
  font-size: 1.4rem;
  font-weight: 600;
}

.form-row {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: 1.5rem;
}

.bmi-display {
  background: linear-gradient(135deg, #4caf50 0%, #2e7d32 100%);
  color: white;
  border-radius: 16px;
  padding: 2rem;
  text-align: center;
  margin: 2rem 0;
  box-shadow: 0 8px 20px rgba(76, 175, 80, 0.3);
}

.bmi-value {
  font-size: 3.5rem;
  font-weight: 700;
  margin-bottom: 0.5rem;
  text-shadow: 0 2px 4px rgba(0,0,0,0.2);
}

.bmi-label {
  font-size: 1.2rem;
  opacity: 0.9;
  margin-bottom: 1rem;
}

.bmi-category {
  font-size: 1.3rem;
  font-weight: 600;
  padding: 0.5rem 1rem;
  border-radius: 20px;
  display: inline-block;
  background: rgba(255, 255, 255, 0.2);
}

.bmi-category.underweight {
  background: rgba(255, 193, 7, 0.3);
}

.bmi-category.normal {
  background: rgba(76, 175, 80, 0.3);
}

.bmi-category.overweight {
  background: rgba(255, 152, 0, 0.3);
}

.bmi-category.obese {
  background: rgba(244, 67, 54, 0.3);
}

.form-actions {
  display: flex;
  justify-content: center;
  gap: 1.5rem;
  margin-top: 2rem;
  padding-top: 2rem;
  border-top: 1px solid #eee;
}

.el-button {
  padding: 12px 32px;
  font-size: 1.1rem;
  border-radius: 8px;
  font-weight: 600;
}

.el-button--primary {
  background: #2e7d32;
  border-color: #2e7d32;
}

.el-button--primary:hover {
  background: #1b5e20;
  border-color: #1b5e20;
}

/* Element Plus 样式覆盖 */
.el-form-item__label {
  color: #2e7d32 !important;
  font-weight: 600 !important;
  font-size: 1rem !important;
}

.el-input-number, .el-slider {
  margin-top: 0.5rem;
}

.el-slider__input {
  width: 100px !important;
}

@media (max-width: 768px) {
  .health-data-input-container {
    padding: 1.5rem;
  }
  
  .health-form {
    padding: 1.5rem;
  }
  
  .form-row {
    grid-template-columns: 1fr;
  }
  
  .header h1 {
    font-size: 2rem;
  }
  
  .bmi-value {
    font-size: 2.5rem;
  }
}
</style>