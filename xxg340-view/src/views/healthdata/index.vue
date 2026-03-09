<template>
  <div class="page-container">
    <!-- 筛选区 -->
    <div class="search-area">
      <el-form :model="searchForm" label-width="100px" class="custom-form">
        <el-row :gutter="24">
          <el-col :span="6">
            <el-form-item label="记录日期">
              <el-date-picker
                v-model="searchForm.hd_date"
                type="date"
                placeholder="请选择记录日期"
                format="YYYY-MM-DD"
                value-format="YYYY-MM-DD"
                clearable
                style="width: 100%"
              />
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
      <el-button type="primary" class="add-btn" @click="handleAdd">新增健康数据</el-button>
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
        <el-table-column prop="hd_date" label="记录日期" min-width="120" />
        <el-table-column prop="hd_weight" label="体重(kg)" min-width="100" />
        <el-table-column prop="hd_height" label="身高(cm)" min-width="100" />
        <el-table-column prop="hd_bmi" label="BMI指数" min-width="100" />
        <el-table-column prop="hd_sbp" label="收缩压" min-width="100" />
        <el-table-column prop="hd_dbp" label="舒张压" min-width="100" />
        <el-table-column prop="hd_glucose" label="血糖水平" min-width="100" />
        <el-table-column prop="hd_cholesterol" label="总胆固醇" min-width="100" />
        <el-table-column prop="hd_hdl" label="高密度脂蛋白" min-width="120" />
        <el-table-column prop="hd_ldl" label="低密度脂蛋白" min-width="120" />
        <el-table-column prop="hd_triglycerides" label="甘油三酯" min-width="120" />
        <el-table-column prop="hd_smoking" label="是否吸烟" min-width="100">
          <template #default="{ row }">
            <el-tag :type="row.hd_smoking == 1 ? 'success' : 'danger'" size="small">
              {{ row.hd_smoking == 1 ? '否' : '是' }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="hd_exercise" label="每周运动时长(小时)" min-width="140" />
        <el-table-column prop="hd_alcohol" label="是否饮酒" min-width="100">
          <template #default="{ row }">
            <el-tag :type="row.hd_alcohol == 1 ? 'success' : 'danger'" size="small">
              {{ row.hd_alcohol == 1 ? '否' : '是' }}
            </el-tag>
          </template>
        </el-table-column>
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

    <!-- 健康数据表单 Dialog -->
    <el-dialog
      :title="dialogTitle"
      v-model="dialogVisible"
      width="600px"
      class="health-data-dialog"
      @close="resetForm"
    >
      <el-form :model="healthDataForm" :rules="rules" ref="healthDataFormRef" label-width="140px" class="dialog-form">
        <el-form-item label="记录日期" prop="hd_date">
          <el-date-picker
            v-model="healthDataForm.hd_date"
            type="date"
            placeholder="请选择记录日期"
            format="YYYY-MM-DD"
            value-format="YYYY-MM-DD"
            style="width: 100%"
            :disabled="isViewMode"
          />
        </el-form-item>
        <el-form-item label="体重(kg)" prop="hd_weight">
          <el-input v-model="healthDataForm.hd_weight" placeholder="请输入体重(kg)" :disabled="isViewMode" />
        </el-form-item>
        <el-form-item label="身高(cm)" prop="hd_height">
          <el-input v-model="healthDataForm.hd_height" placeholder="请输入身高(cm)" :disabled="isViewMode" />
        </el-form-item>
        <el-form-item label="BMI指数" prop="hd_bmi">
          <el-input v-model="healthDataForm.hd_bmi" placeholder="请输入BMI指数" :disabled="isViewMode" />
        </el-form-item>
        <el-form-item label="收缩压" prop="hd_sbp">
          <el-input v-model="healthDataForm.hd_sbp" placeholder="请输入收缩压" :disabled="isViewMode" />
        </el-form-item>
        <el-form-item label="舒张压" prop="hd_dbp">
          <el-input v-model="healthDataForm.hd_dbp" placeholder="请输入舒张压" :disabled="isViewMode" />
        </el-form-item>
        <el-form-item label="血糖水平" prop="hd_glucose">
          <el-input v-model="healthDataForm.hd_glucose" placeholder="请输入血糖水平" :disabled="isViewMode" />
        </el-form-item>
        <el-form-item label="总胆固醇" prop="hd_cholesterol">
          <el-input v-model="healthDataForm.hd_cholesterol" placeholder="请输入总胆固醇" :disabled="isViewMode" />
        </el-form-item>
        <el-form-item label="高密度脂蛋白" prop="hd_hdl">
          <el-input v-model="healthDataForm.hd_hdl" placeholder="请输入高密度脂蛋白" :disabled="isViewMode" />
        </el-form-item>
        <el-form-item label="低密度脂蛋白" prop="hd_ldl">
          <el-input v-model="healthDataForm.hd_ldl" placeholder="请输入低密度脂蛋白" :disabled="isViewMode" />
        </el-form-item>
        <el-form-item label="甘油三酯" prop="hd_triglycerides">
          <el-input v-model="healthDataForm.hd_triglycerides" placeholder="请输入甘油三酯" :disabled="isViewMode" />
        </el-form-item>
        <el-form-item label="是否吸烟" prop="hd_smoking" v-if="!isViewMode">
          <el-select v-model="healthDataForm.hd_smoking" placeholder="请选择是否吸烟" style="width: 100%">
            <el-option label="否" :value="1" />
            <el-option label="是" :value="2" />
          </el-select>
        </el-form-item>
        <el-form-item label="是否吸烟" v-else>
          <el-input :value="healthDataForm.hd_smoking == 1 ? '否' : '是'" disabled />
        </el-form-item>
        <el-form-item label="每周运动时长(小时)" prop="hd_exercise">
          <el-input v-model="healthDataForm.hd_exercise" placeholder="请输入每周运动时长(小时)" :disabled="isViewMode" />
        </el-form-item>
        <el-form-item label="是否饮酒" prop="hd_alcohol" v-if="!isViewMode">
          <el-select v-model="healthDataForm.hd_alcohol" placeholder="请选择是否饮酒" style="width: 100%">
            <el-option label="否" :value="1" />
            <el-option label="是" :value="2" />
          </el-select>
        </el-form-item>
        <el-form-item label="是否饮酒" v-else>
          <el-input :value="healthDataForm.hd_alcohol == 1 ? '否' : '是'" disabled />
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
const tableData = ref([])
const searchForm = reactive({
  hd_date: ''
})
const pagination = reactive({
  current: 1,
  size: 10,
  total: 0
})

// 表单相关
const dialogVisible = ref(false)
const healthDataFormRef = ref()
const healthDataForm = reactive({
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
  hd_smoking: 1,
  hd_exercise: '',
  hd_alcohol: 1
})

const dialogTitle = ref('')
const isViewMode = ref(false)

// 表单验证规则
const rules = {
  hd_date: [
    { required: true, message: '请输入记录日期', trigger: 'blur' }
  ],
  hd_weight: [
    { required: true, message: '请输入体重(kg)', trigger: 'blur' }
  ],
  hd_height: [
    { required: true, message: '请输入身高(cm)', trigger: 'blur' }
  ],
  hd_bmi: [
    { required: true, message: '请输入BMI指数', trigger: 'blur' }
  ],
  hd_sbp: [
    { required: true, message: '请输入收缩压', trigger: 'blur' }
  ],
  hd_dbp: [
    { required: true, message: '请输入舒张压', trigger: 'blur' }
  ],
  hd_glucose: [
    { required: true, message: '请输入血糖水平', trigger: 'blur' }
  ],
  hd_cholesterol: [
    { required: true, message: '请输入总胆固醇', trigger: 'blur' }
  ],
  hd_hdl: [
    { required: true, message: '请输入高密度脂蛋白', trigger: 'blur' }
  ],
  hd_ldl: [
    { required: true, message: '请输入低密度脂蛋白', trigger: 'blur' }
  ],
  hd_triglycerides: [
    { required: true, message: '请输入甘油三酯', trigger: 'blur' }
  ],
  hd_smoking: [
    { required: true, message: '请选择是否吸烟', trigger: 'change' }
  ],
  hd_exercise: [
    { required: true, message: '请输入每周运动时长(小时)', trigger: 'blur' }
  ],
  hd_alcohol: [
    { required: true, message: '请选择是否饮酒', trigger: 'change' }
  ]
}

// 初始化数据
onMounted(() => {
  fetchHealthDataList()
})

// 获取健康数据列表
const fetchHealthDataList = async () => {
  const params = {
    limit: pagination.size,
    pg: pagination.current,
    hd_date: searchForm.hd_date || ''
  }
  const res = await request('/healthdata/index', params, 'get')
  tableData.value = res.data
  pagination.total = res.total
}

// 搜索
const handleSearch = () => {
  pagination.current = 1
  fetchHealthDataList()
}

// 重置搜索
const resetSearch = () => {
  searchForm.hd_date = ''
  pagination.current = 1
  fetchHealthDataList()
}

// 分页大小改变
const handleSizeChange = (val) => {
  pagination.size = val
  pagination.current = 1
  fetchHealthDataList()
}

// 当前页改变
const handleCurrentChange = (val) => {
  pagination.current = val
  fetchHealthDataList()
}

// 新增
const handleAdd = () => {
  resetForm()
  dialogTitle.value = '新增健康数据'
  isViewMode.value = false
  dialogVisible.value = true
}

// 编辑
const handleEdit = (row) => {
  resetForm()
  Object.assign(healthDataForm, row)
  dialogTitle.value = '编辑健康数据'
  isViewMode.value = false
  dialogVisible.value = true
}

// 查看
const handleView = (row) => {
  resetForm()
  Object.assign(healthDataForm, row)
  dialogTitle.value = '查看健康数据'
  isViewMode.value = true
  dialogVisible.value = true
}

// 删除
const handleDelete = async (row) => {
  try {
    await ElMessageBox.confirm(`确定要删除这条健康数据吗？`, '确认删除', {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning'
    })
    
    await request(`/healthdata/destroy?id=${row.id}`, {}, 'delete')
    ElMessage.success('删除成功')
    fetchHealthDataList()
  } catch (error) {
    console.log('取消删除')
  }
}

// 提交表单
const submitForm = async () => {
  try {
    await healthDataFormRef.value.validate()
    
    if (healthDataForm.id) {
      // 更新
      await request(`/healthdata/update?id=${healthDataForm.id}`, healthDataForm, 'put')
      ElMessage.success('更新成功')
    } else {
      // 新增
      await request('/healthdata/store', healthDataForm, 'post')
      ElMessage.success('新增成功')
    }
    
    dialogVisible.value = false
    fetchHealthDataList()
  } catch (error) {
    console.log('表单验证失败', error)
  }
}

// 重置表单
const resetForm = () => {
  healthDataFormRef.value.clearValidate()
  Object.keys(healthDataForm).forEach(key => {
    if (key == 'hd_smoking' || key == 'hd_alcohol') {
      healthDataForm[key] = 1
    } else {
      healthDataForm[key] = ''
    }
  })
}

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
:deep(.health-data-dialog .el-dialog__header) {
  padding: 24px 24px 0;
}

:deep(.health-data-dialog .el-dialog__body) {
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