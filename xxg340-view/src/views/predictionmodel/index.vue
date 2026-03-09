<template>
  <div class="page-container">
    <!-- 筛选区 -->
    <div class="search-area">
      <el-form :model="searchForm" label-width="80px" class="custom-form">
        <el-row :gutter="24">
          <el-col :span="6">
            <el-form-item label="模型名称">
              <el-input v-model="searchForm.wywpm_name" placeholder="请输入模型名称" clearable />
            </el-form-item>
          </el-col>
          <el-col :span="6">
            <el-form-item label="模型状态">
              <el-select v-model="searchForm.pm_status" placeholder="请选择模型状态" clearable>
                <el-option label="启用" :value="2" />
                <el-option label="禁用" :value="1" />
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
      <el-button type="primary" class="add-btn" @click="handleAdd">新增模型</el-button>
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
        <el-table-column prop="wywpm_name" label="模型名称" min-width="150" />
        <el-table-column prop="nubpm_version" label="模型版本" min-width="120" />
        <el-table-column prop="pm_status" label="模型状态" min-width="100">
          <template #default="{ row }">
            <el-tag :type="row.pm_status == 2 ? 'success' : 'danger'" size="small">
              {{ row.pm_status == 2 ? '启用' : '禁用' }}
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

    <!-- 预测模型表单 Dialog -->
    <el-dialog
      :title="dialogTitle"
      v-model="dialogVisible"
      width="600px"
      class="model-dialog"
      @close="resetForm"
    >
      <el-form :model="modelForm" :rules="rules" ref="modelFormRef" label-width="100px" class="dialog-form">
        <el-form-item label="模型名称" prop="wywpm_name">
          <el-input v-model="modelForm.wywpm_name" placeholder="请输入模型名称" :disabled="isViewMode" />
        </el-form-item>
        <el-form-item label="模型版本" prop="nubpm_version">
          <el-input v-model="modelForm.nubpm_version" placeholder="请输入模型版本" :disabled="isViewMode" />
        </el-form-item>
        <el-form-item label="模型状态" prop="pm_status" v-if="!isViewMode">
          <el-select v-model="modelForm.pm_status" placeholder="请选择模型状态" style="width: 100%">
            <el-option label="启用" :value="2" />
            <el-option label="禁用" :value="1" />
          </el-select>
        </el-form-item>
        <el-form-item label="模型状态" v-else>
          <el-tag :type="modelForm.pm_status == 2 ? 'success' : 'danger'" size="small">
            {{ modelForm.pm_status == 2 ? '启用' : '禁用' }}
          </el-tag>
        </el-form-item>
        <el-form-item label="训练数据集描述" prop="pm_dataset">
          <el-input 
            v-model="modelForm.pm_dataset" 
            type="textarea" 
            :rows="3" 
            placeholder="请输入训练数据集描述" 
            :disabled="isViewMode" 
          />
        </el-form-item>
        <el-form-item label="模型描述" prop="pm_description">
          <el-input 
            v-model="modelForm.pm_description" 
            type="textarea" 
            :rows="3" 
            placeholder="请输入模型描述" 
            :disabled="isViewMode" 
          />
        </el-form-item>
        <el-form-item label="模型文件" prop="pm_filepath" v-if="!isViewMode">
          <UploadFile v-model:fileUrl="modelForm.pm_filepath" />
        </el-form-item>
        <el-form-item label="模型文件" v-else>
          <div v-for="(file, index) in modelForm.pm_filepath" :key="index" class="file-item">
            <el-link :href="file.url" target="_blank" type="primary">{{ file.name }}</el-link>
          </div>
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

// 搜索表单
const searchForm = reactive({
  wywpm_name: '',
  pm_status: ''
})

// 分页信息
const pagination = reactive({
  current: 1,
  size: 10,
  total: 0
})

// 表格数据
const tableData = ref([])

// 弹窗相关
const dialogVisible = ref(false)
const dialogTitle = ref('')
const isViewMode = ref(false)
const modelFormRef = ref(null)

// 表单数据
const modelForm = reactive({
  wywpm_name: '',
  nubpm_version: '',
  pm_status: null,
  pm_dataset: '',
  pm_description: '',
  pm_filepath: []
})

// 表单验证规则
const rules = {
  wywpm_name: [
    { required: true, message: '请输入模型名称', trigger: 'blur' }
  ],
  nubpm_version: [
    { required: true, message: '请输入模型版本', trigger: 'blur' }
  ],
  pm_status: [
    { required: true, message: '请选择模型状态', trigger: 'change' }
  ],
  pm_dataset: [
    { required: true, message: '请输入训练数据集描述', trigger: 'blur' }
  ],
  pm_description: [
    { required: true, message: '请输入模型描述', trigger: 'blur' }
  ],
  pm_filepath: [
    { required: true, message: '请上传模型文件', trigger: 'change' }
  ]
}

// 初始化数据
onMounted(() => {
  fetchTableData()
})

// 获取表格数据
const fetchTableData = async () => {
  const res = await request('/predictionmodel/index', {
    limit: pagination.size,
    pg: pagination.current,
    wywpm_name: searchForm.wywpm_name,
    pm_status: searchForm.pm_status
  }, 'get')
  
  tableData.value = res.data
  pagination.total = res.total
}

// 搜索
const handleSearch = () => {
  pagination.current = 1
  fetchTableData()
}

// 重置搜索
const resetSearch = () => {
  searchForm.wywpm_name = ''
  searchForm.pm_status = ''
  pagination.current = 1
  fetchTableData()
}

// 分页大小改变
const handleSizeChange = (val) => {
  pagination.size = val
  pagination.current = 1
  fetchTableData()
}

// 当前页改变
const handleCurrentChange = (val) => {
  pagination.current = val
  fetchTableData()
}

// 新增
const handleAdd = () => {
  dialogTitle.value = '新增预测模型'
  isViewMode.value = false
  Object.assign(modelForm, {
    wywpm_name: '',
    nubpm_version: '',
    pm_status: null,
    pm_dataset: '',
    pm_description: '',
    pm_filepath: []
  })
  dialogVisible.value = true
}

// 查看
const handleView = (row) => {
  dialogTitle.value = '查看预测模型'
  isViewMode.value = true
  Object.assign(modelForm, JSON.parse(JSON.stringify(row)))
  dialogVisible.value = true
}

// 编辑
const handleEdit = (row) => {
  dialogTitle.value = '编辑预测模型'
  isViewMode.value = false
  Object.assign(modelForm, JSON.parse(JSON.stringify(row)))
  dialogVisible.value = true
}

// 删除
const handleDelete = async (row) => {
  try {
    await ElMessageBox.confirm(`确定要删除模型 "${row.wywpm_name}" 吗？`, '确认删除', {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning'
    })
    
    await request('/predictionmodel/destroy', { id: row.id }, 'delete')
    ElMessage.success('删除成功')
    fetchTableData()
  } catch (error) {
    console.log('取消删除')
  }
}

// 提交表单
const submitForm = async () => {
  try {
    await modelFormRef.value.validate()
    
    if (modelForm.id) {
      // 更新
      await request('/predictionmodel/update', modelForm, 'put')
      ElMessage.success('更新成功')
    } else {
      // 新增
      await request('/predictionmodel/store', modelForm, 'post')
      ElMessage.success('新增成功')
    }
    
    dialogVisible.value = false
    fetchTableData()
  } catch (error) {
    console.log('表单验证失败', error)
  }
}

// 重置表单
const resetForm = () => {
  if (modelFormRef.value) {
    modelFormRef.value.clearValidate()
  }
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
:deep(.model-dialog .el-dialog__header) {
  padding: 24px 24px 0;
}

:deep(.model-dialog .el-dialog__body) {
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

.file-item {
  margin-bottom: 5px;
}
</style>