<template>
  <div class="healthdata-edit-container">
    <div class="header">
      <h1>编辑健康数据</h1>
      <p>请更新您的心血管健康相关指标</p>
    </div>

    <div class="form-card">
      <el-form :model="formData" label-position="top" ref="formRef" :rules="rules">
        <el-row :gutter="24">
          <el-col :span="12">
            <el-form-item label="记录日期" prop="hd_date">
              <el-input v-model="formData.hd_date" placeholder="YYYY-MM-DD" />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="体重 (kg)" prop="hd_weight">
              <el-input v-model="formData.hd_weight" placeholder="请输入体重" />
            </el-form-item>
          </el-col>
        </el-row>

        <el-row :gutter="24">
          <el-col :span="12">
            <el-form-item label="身高 (cm)" prop="hd_height">
              <el-input v-model="formData.hd_height" placeholder="请输入身高" />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="BMI指数" prop="hd_bmi">
              <el-input v-model="formData.hd_bmi" placeholder="自动计算或手动输入" readonly />
            </el-form-item>
          </el-col>
        </el-row>

        <el-row :gutter="24">
          <el-col :span="12">
            <el-form-item label="收缩压 (mmHg)" prop="hd_sbp">
              <el-input v-model="formData.hd_sbp" placeholder="请输入收缩压" />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="舒张压 (mmHg)" prop="hd_dbp">
              <el-input v-model="formData.hd_dbp" placeholder="请输入舒张压" />
            </el-form-item>
          </el-col>
        </el-row>

        <el-row :gutter="24">
          <el-col :span="12">
            <el-form-item label="血糖水平 (mmol/L)" prop="hd_glucose">
              <el-input v-model="formData.hd_glucose" placeholder="请输入血糖值" />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="总胆固醇 (mmol/L)" prop="hd_cholesterol">
              <el-input v-model="formData.hd_cholesterol" placeholder="请输入总胆固醇" />
            </el-form-item>
          </el-col>
        </el-row>

        <el-row :gutter="24">
          <el-col :span="8">
            <el-form-item label="高密度脂蛋白 (mmol/L)" prop="hd_hdl">
              <el-input v-model="formData.hd_hdl" placeholder="HDL" />
            </el-form-item>
          </el-col>
          <el-col :span="8">
            <el-form-item label="低密度脂蛋白 (mmol/L)" prop="hd_ldl">
              <el-input v-model="formData.hd_ldl" placeholder="LDL" />
            </el-form-item>
          </el-col>
          <el-col :span="8">
            <el-form-item label="甘油三酯 (mmol/L)" prop="hd_triglycerides">
              <el-input v-model="formData.hd_triglycerides" placeholder="甘油三酯" />
            </el-form-item>
          </el-col>
        </el-row>

        <el-row :gutter="24">
          <el-col :span="12">
            <el-form-item label="是否吸烟" prop="hd_smoking">
              <el-select v-model="formData.hd_smoking" placeholder="请选择">
                <el-option :value="1" label="否" />
                <el-option :value="2" label="是" />
              </el-select>
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="每周运动时长 (小时)" prop="hd_exercise">
              <el-input v-model="formData.hd_exercise" placeholder="请输入运动时长" />
            </el-form-item>
          </el-col>
        </el-row>

        <el-row :gutter="24">
          <el-col :span="12">
            <el-form-item label="是否饮酒" prop="hd_alcohol">
              <el-select v-model="formData.hd_alcohol" placeholder="请选择">
                <el-option :value="1" label="否" />
                <el-option :value="2" label="是" />
              </el-select>
            </el-form-item>
          </el-col>
        </el-row>
      </el-form>

      <div class="action-buttons">
        <el-button @click="goBack">取消</el-button>
        <el-button type="primary" @click="submitForm">保存更新</el-button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { 
  ref, 
  reactive, 
  onMounted, 
  watch
} from 'vue';

import { request } from "@/http/index";
import { GlobalStore } from "@/stores";
import { useRoute, useRouter } from "vue-router";
import { ElMessage, ElMessageBox } from 'element-plus'

const router = useRouter();
const route = useRoute();
const globalStore = GlobalStore();

const userInfo = globalStore.userInfo

const formData = reactive({
  hd_date: '',
  hd_weight: '',
  hd_height: '',
  hd_bmi: '',
  hd_sbp: '',
  hd_dbp: '',
  hd_glucose: '',
  hd_cholesterol: '',
  hd_hdl: '',
  hd_ldl: '',
  hd_triglycerides: '',
  hd_smoking: null,
  hd_exercise: '',
  hd_alcohol: null
});

const formRef = ref(null);

const rules = {
  hd_date: [{ required: true, message: '请输入记录日期', trigger: 'blur' }],
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

// 自动计算 BMI
watch(
  () => [formData.hd_weight, formData.hd_height],
  () => {
    const weight = parseFloat(formData.hd_weight);
    const height = parseFloat(formData.hd_height);
    if (!isNaN(weight) && !isNaN(height) && height > 0) {
      const bmi = (weight / ((height / 100) ** 2)).toFixed(2);
      formData.hd_bmi = bmi;
    } else {
      formData.hd_bmi = '';
    }
  },
  { immediate: true }
);

const goBack = () => {
  router.push({ path: '/healthdata/list', query: undefined });
};

const submitForm = async () => {
  if (!formRef.value) return;
  
  try {
    await formRef.value.validate();
    
    const id = route.query.id;
    if (!id) {
      ElMessage.error('缺少健康数据ID');
      return;
    }

    const res = await request('/healthdata/update', {
      ...formData
    }, 'put');
    
    ElMessage.success('健康数据更新成功！');
    goBack();
  } catch (error) {
    ElMessage.error('更新失败，请重试');
  }
};

onMounted(async () => {
  const id = route.query.id;
  if (!id) {
    ElMessage.error('无效的健康数据ID');
    goBack();
    return;
  }

  const res = await request('/healthdata/show', {
    id: id
  }, 'get');

  // 直接赋值，无需判断
  Object.assign(formData, res);
});
</script>

<style scoped>
.healthdata-edit-container {
  padding: 30px;
  background: linear-gradient(135deg, #f5f7fa 0%, #e4edf9 100%);
  min-height: 100vh;
}

.header {
  text-align: center;
  margin-bottom: 30px;
}

.header h1 {
  font-size: 28px;
  color: #1a5fb4;
  margin-bottom: 10px;
  font-weight: 600;
}

.header p {
  color: #666;
  font-size: 16px;
}

.form-card {
  background: white;
  border-radius: 16px;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.08);
  padding: 30px;
  max-width: 900px;
  margin: 0 auto;
}

.el-form {
  margin-bottom: 30px;
}

.el-form-item {
  margin-bottom: 20px;
}

.el-form-item__label {
  font-weight: 600;
  color: #333;
  font-size: 14px;
  margin-bottom: 6px;
}

.el-input,
.el-select {
  width: 100%;
}

.action-buttons {
  display: flex;
  justify-content: flex-end;
  gap: 16px;
  margin-top: 20px;
}

.action-buttons .el-button {
  padding: 10px 24px;
  font-size: 16px;
  border-radius: 8px;
}

.action-buttons .el-button:first-child {
  background: #f0f2f5;
  border-color: #dcdfe6;
  color: #606266;
}

.action-buttons .el-button:first-child:hover {
  background: #e6e8eb;
}

.action-buttons .el-button--primary {
  background: #1a5fb4;
  border-color: #1a5fb4;
}

.action-buttons .el-button--primary:hover {
  background: #164e9c;
  border-color: #164e9c;
}
</style>