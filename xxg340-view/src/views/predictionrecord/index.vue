<template>
  <div class="page-container">
    <!-- 筛选区 -->
    <div class="search-area">
      <el-form :model="searchForm" label-width="100px" class="custom-form">
        <el-row :gutter="24">
          <el-col :span="6">
            <el-form-item label="模型名称">
              <el-select v-model="searchForm.pm_id" placeholder="请选择预测模型" clearable>
                <el-option 
                  v-for="item in modelOptions" 
                  :key="item.id" 
                  :label="`${item.wywpm_name} (${item.nubpm_version})`" 
                  :value="item.id" 
                />
              </el-select>
            </el-form-item>
          </el-col>
          <el-col :span="6">
            <el-form-item label="风险等级">
              <el-input v-model="searchForm.pr_risklevel" placeholder="请输入风险等级" clearable />
            </el-form-item>
          </el-col>
          <el-col :span="6">
            <el-form-item label="预测时间">
              <el-input v-model="searchForm.pr_predictiontime" placeholder="请输入预测时间" clearable />
            </el-form-item>
          </el-col>
          <el-col :span="6">
            <el-form-item label="是否批量">
              <el-select v-model="searchForm.pr_isbatch" placeholder="请选择是否批量预测" clearable>
                <el-option label="单次预测" :value="1" />
                <el-option label="批量预测" :value="2" />
              </el-select>
            </el-form-item>
          </el-col>
          <el-col :span="6">
            <el-form-item label="年龄">
              <el-input v-model="searchForm.pr_age" placeholder="请输入年龄" clearable />
            </el-form-item>
          </el-col>
          <el-col :span="6">
            <el-form-item label="性别">
              <el-select v-model="searchForm.pr_sex" placeholder="请选择性别" clearable>
                <el-option label="男" :value="2" />
                <el-option label="女" :value="3" />
              </el-select>
            </el-form-item>
          </el-col>
          <el-col :span="6" class="search-buttons">
            <el-button type="primary" @click="handleSearch">查询</el-button>
            <el-button @click="resetSearch">重置</el-button>
          </el-col>
        </el-row>
      </el-form>
    </div>

    <!-- 操作按钮区 -->
    <div class="action-area">
      <el-button type="primary" class="add-btn" @click="handleAdd">新增预测记录</el-button>
    </div>

    <!-- 数据表格区 -->
    <div class="table-area">
      <el-table
        :data="tableData"
        border
        stripe
        style="width: 100%"
        class="custom-table"
      >
        <el-table-column prop="wywpm_name" label="模型名称" min-width="120" />
        <el-table-column prop="nubpm_version" label="模型版本" min-width="100" />
        <el-table-column prop="pr_age" label="年龄" min-width="80" />
        <el-table-column prop="pr_sex" label="性别" min-width="80">
          <template #default="{ row }">
            <el-tag :type="row.pr_sex == 2 ? 'primary' : 'warning'" size="small">
              {{ row.pr_sex == 2 ? '男' : '女' }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="pr_risklevel" label="风险等级" min-width="100" />
        <el-table-column prop="pr_probability" label="预测概率" min-width="100" />
        <el-table-column prop="pr_predictiontime" label="预测时间" min-width="160" />
        <el-table-column prop="pr_isbatch" label="是否批量" min-width="100">
          <template #default="{ row }">
            <el-tag :type="row.pr_isbatch == 1 ? 'info' : 'success'" size="small">
              {{ row.pr_isbatch == 1 ? '单次预测' : '批量预测' }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="cd" label="创建时间" min-width="160" />
        <el-table-column label="操作" width="220" fixed="right" align="center">
          <template #default="{ row }">
            <div class="action-buttons">
              <el-button size="small" class="view-btn" @click="handleView(row)">查看</el-button>
              <el-button size="small" type="primary" class="edit-btn" @click="handleEdit(row)">编辑</el-button>
              <el-button size="small" type="danger" class="delete-btn" @click="handleDelete(row)">删除</el-button>
            </div>
          </template>
        </el-table-column>
      </el-table>
      
      <!-- 分页 -->
      <div class="pagination-area">
        <el-pagination
          v-model:current-page="pagination.current"
          v-model:page-size="pagination.size"
          :total="pagination.total"
          layout="total, sizes, prev, pager, next, jumper"
          :page-sizes="[10, 20, 30, 50]"
          @size-change="handleSizeChange"
          @current-change="handleCurrentChange"
          class="custom-pagination"
        />
      </div>
    </div>

    <!-- 预测记录表单 Dialog -->
    <el-dialog
      :title="dialogTitle"
      v-model="dialogVisible"
      width="600px"
      class="prediction-record-dialog"
      @close="resetForm"
    >
      <el-form :model="form" :rules="rules" ref="formRef" label-width="120px" class="dialog-form">
        <el-form-item label="预测模型" prop="pm_id">
          <el-select v-model="form.pm_id" placeholder="请选择预测模型" style="width: 100%" :disabled="isViewMode">
            <el-option 
              v-for="item in modelOptions" 
              :key="item.id" 
              :label="`${item.wywpm_name} (${item.nubpm_version})`" 
              :value="item.id" 
            />
          </el-select>
        </el-form-item>
        <el-form-item label="年龄" prop="pr_age">
          <el-input v-model="form.pr_age" placeholder="请输入年龄" :disabled="isViewMode" />
        </el-form-item>
        <el-form-item label="性别" prop="pr_sex">
          <el-select v-model="form.pr_sex" placeholder="请选择性别" style="width: 100%" :disabled="isViewMode">
            <el-option label="男" :value="2" />
            <el-option label="女" :value="3" />
          </el-select>
        </el-form-item>
        <el-form-item label="胸痛类型" prop="pr_cp">
          <el-input v-model="form.pr_cp" placeholder="请输入胸痛类型" :disabled="isViewMode" />
        </el-form-item>
        <el-form-item label="静息血压" prop="pr_trestbps">
          <el-input v-model="form.pr_trestbps" placeholder="请输入静息血压" :disabled="isViewMode" />
        </el-form-item>
        <el-form-item label="血清胆固醇" prop="pr_chol">
          <el-input v-model="form.pr_chol" placeholder="请输入血清胆固醇" :disabled="isViewMode" />
        </el-form-item>
        <el-form-item label="空腹血糖" prop="pr_fbs">
          <el-input v-model="form.pr_fbs" placeholder="请输入空腹血糖" :disabled="isViewMode" />
        </el-form-item>
        <el-form-item label="静息心电图结果" prop="pr_restecg">
          <el-input v-model="form.pr_restecg" placeholder="请输入静息心电图结果" :disabled="isViewMode" />
        </el-form-item>
        <el-form-item label="最大心率" prop="pr_thalach">
          <el-input v-model="form.pr_thalach" placeholder="请输入最大心率" :disabled="isViewMode" />
        </el-form-item>
        <el-form-item label="运动诱发心绞痛" prop="pr_exang">
          <el-input v-model="form.pr_exang" placeholder="请输入运动诱发心绞痛" :disabled="isViewMode" />
        </el-form-item>
        <el-form-item label="ST段压低" prop="pr_oldpeak">
          <el-input v-model="form.pr_oldpeak" placeholder="请输入ST段压低" :disabled="isViewMode" />
        </el-form-item>
        <el-form-item label="ST段峰值运动斜率" prop="pr_slope">
          <el-input v-model="form.pr_slope" placeholder="请输入ST段峰值运动斜率" :disabled="isViewMode" />
        </el-form-item>
        <el-form-item label="主要血管数量" prop="pr_ca">
          <el-input v-model="form.pr_ca" placeholder="请输入主要血管数量" :disabled="isViewMode" />
        </el-form-item>
        <el-form-item label="地中海贫血" prop="pr_thal">
          <el-input v-model="form.pr_thal" placeholder="请输入地中海贫血" :disabled="isViewMode" />
        </el-form-item>
        <el-form-item label="风险等级" prop="pr_risklevel">
          <el-input v-model="form.pr_risklevel" placeholder="请输入风险等级" :disabled="isViewMode" />
        </el-form-item>
        <el-form-item label="预测概率" prop="pr_probability">
          <el-input v-model="form.pr_probability" placeholder="请输入预测概率" :disabled="isViewMode" />
        </el-form-item>
        <el-form-item label="预测时间" prop="pr_predictiontime">
          <el-input v-model="form.pr_predictiontime" placeholder="请输入预测时间" :disabled="isViewMode" />
        </el-form-item>
        <el-form-item label="批量预测文件" prop="pr_batchfile">
          <UploadFile v-model:fileUrl="form.pr_batchfile" :disabled="isViewMode" />
        </el-form-item>
        <el-form-item label="预测结果文件" prop="pr_resultfile">
          <UploadFile v-model:fileUrl="form.pr_resultfile" :disabled="isViewMode" />
        </el-form-item>
        <el-form-item label="是否批量预测" prop="pr_isbatch">
          <el-select v-model="form.pr_isbatch" placeholder="请选择是否批量预测" style="width: 100%" :disabled="isViewMode">
            <el-option label="单次预测" :value="1" />
            <el-option label="批量预测" :value="2" />
          </el-select>
        </el-form-item>
      </el-form>
      <template #footer v-if="!isViewMode">
        <div class="dialog-footer">
          <el-button @click="dialogVisible = false">取消</el-button>
          <el-button type="primary" @click="submitForm">保存</el-button>
        </div>
      </template>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
// 固定代码只能新增不能修改
import { 
  ref, 
  reactive, 
  onMounted, 
  onUpdated, 
  onBeforeUnmount, 
  computed, 
  watch, 
  watchEffect, 
  provide, 
  inject, 
  nextTick 
} from 'vue';

import { ElMessage, ElMessageBox } from 'element-plus'
import { request } from '@/http/index'; // 请求数据直接用这个
import { GlobalStore } from '@/stores';
const globalStore = GlobalStore();
import * as echarts from "echarts"; // echarts图表 需要时直接使用


/**
* 当前登录用户信息数据，包含用户的角色数据比如教练、商家等
* 使用方法：
- 获取用户基本信息 
const userInfo = globalStore.userInfo
返回值：{
    id:'用户id',
    user_name:'用户名称',
    avatar:'头像',
    role_id:'角色id',
}

*/

const userInfo = globalStore.userInfo

/**
以下属于全局组件可直接使用不要引入：
富文本编辑：<WangEditor height="400px" v-model:value="字段名称" />
单图上传：<UploadImg  v-model:imageUrl="字段名称" />
多图上传：<UploadManyImg  v-model:imageUrl="字段名称" />
文件上传： <UploadFile  v-model:fileUrl="字段名称" />
*/
// 固定代码只能新增不能修改

// 响应式数据
const tableData = ref([]);
const modelOptions = ref([]);
const pagination = reactive({
  current: 1,
  size: 10,
  total: 0
});
const searchForm = reactive({
  pm_id: '',
  pr_risklevel: '',
  pr_predictiontime: '',
  pr_isbatch: '',
  pr_age: '',
  pr_sex: ''
});

// 表单相关
const dialogVisible = ref(false);
const isViewMode = ref(false);
const formRef = ref();
const form = reactive({
  id: undefined,
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
  pr_isbatch: null,
  wywpm_name: '',
  nubpm_version: ''
});

// 表单验证规则
const rules = {
  pm_id: [{ required: true, message: '请选择预测模型', trigger: 'change' }],
  pr_age: [{ required: true, message: '请输入年龄', trigger: 'blur' }],
  pr_sex: [{ required: true, message: '请选择性别', trigger: 'change' }],
  pr_cp: [{ required: true, message: '请输入胸痛类型', trigger: 'blur' }],
  pr_trestbps: [{ required: true, message: '请输入静息血压', trigger: 'blur' }],
  pr_chol: [{ required: true, message: '请输入血清胆固醇', trigger: 'blur' }],
  pr_fbs: [{ required: true, message: '请输入空腹血糖', trigger: 'blur' }],
  pr_restecg: [{ required: true, message: '请输入静息心电图结果', trigger: 'blur' }],
  pr_thalach: [{ required: true, message: '请输入最大心率', trigger: 'blur' }],
  pr_exang: [{ required: true, message: '请输入运动诱发心绞痛', trigger: 'blur' }],
  pr_oldpeak: [{ required: true, message: '请输入ST段压低', trigger: 'blur' }],
  pr_slope: [{ required: true, message: '请输入ST段峰值运动斜率', trigger: 'blur' }],
  pr_ca: [{ required: true, message: '请输入主要血管数量', trigger: 'blur' }],
  pr_thal: [{ required: true, message: '请输入地中海贫血', trigger: 'blur' }],
  pr_risklevel: [{ required: true, message: '请输入风险等级', trigger: 'blur' }],
  pr_probability: [{ required: true, message: '请输入预测概率', trigger: 'blur' }],
  pr_predictiontime: [{ required: true, message: '请输入预测时间', trigger: 'blur' }],
  pr_isbatch: [{ required: true, message: '请选择是否批量预测', trigger: 'change' }]
};

// 计算属性
const dialogTitle = computed(() => {
  if (isViewMode.value) return '查看预测记录';
  return form.id ? '编辑预测记录' : '新增预测记录';
});

// 方法
const fetchData = async () => {
  const params = {
    limit: pagination.size,
    pg: pagination.current,
    pm_id: searchForm.pm_id,
    pr_risklevel: searchForm.pr_risklevel,
    pr_predictiontime: searchForm.pr_predictiontime,
    pr_isbatch: searchForm.pr_isbatch,
    pr_age: searchForm.pr_age,
    pr_sex: searchForm.pr_sex
  };
  
  const res = await request('/predictionrecord/index', params, 'get');
  tableData.value = res.data;
  pagination.total = res.total;
};

const fetchModelOptions = async () => {
  const res = await request('/predictionmodel/index', { limit: 999 }, 'get');
  modelOptions.value = res.data;
};

const handleSearch = () => {
  pagination.current = 1;
  fetchData();
};

const resetSearch = () => {
  Object.keys(searchForm).forEach(key => {
    searchForm[key] = '';
  });
  pagination.current = 1;
  fetchData();
};

const handleSizeChange = (val) => {
  pagination.size = val;
  fetchData();
};

const handleCurrentChange = (val) => {
  pagination.current = val;
  fetchData();
};

const handleAdd = () => {
  resetForm();
  isViewMode.value = false;
  dialogVisible.value = true;
};

const handleView = (row) => {
  Object.assign(form, row);
  isViewMode.value = true;
  dialogVisible.value = true;
};

const handleEdit = (row) => {
  Object.assign(form, row);
  isViewMode.value = false;
  dialogVisible.value = true;
};

const handleDelete = async (row) => {
  try {
    await ElMessageBox.confirm(`确定要删除这条预测记录吗？`, '确认删除', {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning'
    });
    
    await request('/predictionrecord/destroy', { id: row.id }, 'delete');
    ElMessage.success('删除成功');
    fetchData();
  } catch (error) {
    console.error('删除失败:', error);
  }
};

const submitForm = async () => {
  try {
    await formRef.value.validate();
    
    if (form.id) {
      await request('/predictionrecord/update', form, 'put');
      ElMessage.success('更新成功');
    } else {
      await request('/predictionrecord/store', form, 'post');
      ElMessage.success('新增成功');
    }
    
    dialogVisible.value = false;
    fetchData();
  } catch (error) {
    console.error('提交失败:', error);
    ElMessage.error('提交失败');
  }
};

const resetForm = () => {
  Object.keys(form).forEach(key => {
    if (key == 'pr_sex' || key == 'pr_isbatch') {
      form[key] = null;
    } else if (key == 'pr_batchfile' || key == 'pr_resultfile') {
      form[key] = [];
    } else {
      form[key] = '';
    }
  });
  form.id = undefined;
  if (formRef.value) {
    formRef.value.clearValidate();
  }
};

// 初始化
onMounted(() => {
  fetchModelOptions();
  fetchData();
});
</script>

<style scoped>
.page-container {
  padding: 24px;
  background: #f8fafc;
  min-height: 100vh;
}

/* 搜索区域样式 */
.search-area {
  background: white;
  padding: 24px;
  border-radius: 12px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
  margin-bottom: 20px;
}

.custom-form :deep(.el-form-item__label) {
  font-weight: 600;
  color: #475569;
}

.search-buttons {
  display: flex;
  justify-content: flex-end;
  align-items: center;
  gap: 12px;
}

/* 操作按钮区域 */
.action-area {
  margin-bottom: 20px;
  display: flex;
  justify-content: flex-end;
}

.add-btn {
  background: linear-gradient(135deg, #4f46e5 0%, #7c3aed 100%);
  border: none;
  border-radius: 8px;
  padding: 10px 24px;
  font-weight: 600;
  transition: all 0.3s ease;
}

.add-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(79, 70, 229, 0.3);
}

/* 表格区域样式 */
.table-area {
  background: white;
  border-radius: 12px;
  overflow: hidden;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
}

.custom-table :deep(.el-table__header th) {
  background: #f1f5f9;
  font-weight: 600;
  color: #334155;
}

.custom-table :deep(.el-table__row) {
  transition: background-color 0.2s ease;
}

.custom-table :deep(.el-table__row:hover) {
  background-color: #f8fafc !important;
}

/* 操作按钮样式 */
.action-buttons {
  display: flex;
  gap: 8px;
  justify-content: center;
}

.view-btn {
  background: #e2e8f0;
  color: #475569;
  border: 1px solid #cbd5e1;
  border-radius: 6px;
  padding: 6px 12px;
  font-size: 12px;
  transition: all 0.2s ease;
}

.view-btn:hover {
  background: #cbd5e1;
  color: #334155;
}

.edit-btn {
  background: linear-gradient(135deg, #0ea5e9 0%, #0284c7 100%);
  border: none;
  border-radius: 6px;
  padding: 6px 12px;
  font-size: 12px;
  transition: all 0.2s ease;
}

.edit-btn:hover {
  transform: translateY(-1px);
  box-shadow: 0 2px 6px rgba(14, 165, 233, 0.3);
}

.delete-btn {
  background: linear-gradient(135deg, #ef4444 0%, #dc2626 100%);
  border: none;
  border-radius: 6px;
  padding: 6px 12px;
  font-size: 12px;
  transition: all 0.2s ease;
}

.delete-btn:hover {
  transform: translateY(-1px);
  box-shadow: 0 2px 6px rgba(239, 68, 68, 0.3);
}

/* 分页区域 */
.pagination-area {
  padding: 20px;
  display: flex;
  justify-content: flex-end;
}

.custom-pagination :deep(.el-pagination__total) {
  margin-right: 20px;
  color: #64748b;
}

.custom-pagination :deep(.el-pagination .el-input__inner) {
  height: 32px;
  padding: 0 8px;
}

/* Dialog 样式 */
:deep(.prediction-record-dialog .el-dialog__header) {
  padding: 24px 24px 0;
}

:deep(.prediction-record-dialog .el-dialog__body) {
  padding: 0 24px 24px;
}

.dialog-form :deep(.el-form-item__label) {
  font-weight: 600;
  color: #475569;
}

.dialog-footer {
  display: flex;
  justify-content: flex-end;
  gap: 12px;
  padding-top: 16px;
}
</style>