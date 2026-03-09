<template>
  <div class="page-container">
    <!-- 筛选区 -->
    <div class="search-area">
      <el-form :model="searchForm" label-width="100px" class="custom-form">
        <el-row :gutter="24">
          <el-col :span="6">
            <el-form-item label="模板名称">
              <el-input v-model="searchForm.rt_name" placeholder="请输入模板名称" clearable />
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
      <el-button type="primary" class="add-btn" @click="handleAdd">新增模板</el-button>
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
        <el-table-column prop="rt_name" label="模板名称" min-width="180" />
        <el-table-column prop="rt_risklevel" label="适用风险等级" min-width="150" />
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

    <!-- 报告模板表单 Dialog -->
    <el-dialog
      :title="dialogTitle"
      v-model="dialogVisible"
      width="800px"
      class="report-template-dialog"
      @close="resetForm"
    >
      <el-form :model="form" :rules="rules" ref="formRef" label-width="100px" class="dialog-form">
        <el-form-item label="模板名称" prop="rt_name">
          <el-input v-model="form.rt_name" placeholder="请输入模板名称" :disabled="isViewMode" />
        </el-form-item>
        <el-form-item label="适用风险等级" prop="rt_risklevel">
          <el-input v-model="form.rt_risklevel" placeholder="请输入适用风险等级" :disabled="isViewMode" />
        </el-form-item>
        <el-form-item label="风险解释" prop="rt_explanation" v-if="!isViewMode">
          <WangEditor height="300px" v-model:value="form.rt_explanation" />
        </el-form-item>
        <el-form-item label="风险解释" v-else>
          <div v-html="form.rt_explanation" class="rich-text-display"></div>
        </el-form-item>
        <el-form-item label="建议措施" prop="rt_suggestions" v-if="!isViewMode">
          <WangEditor height="300px" v-model:value="form.rt_suggestions" />
        </el-form-item>
        <el-form-item label="建议措施" v-else>
          <div v-html="form.rt_suggestions" class="rich-text-display"></div>
        </el-form-item>
        <el-form-item label="正常范围说明" prop="rt_normalscope" v-if="!isViewMode">
          <WangEditor height="300px" v-model:value="form.rt_normalscope" />
        </el-form-item>
        <el-form-item label="正常范围说明" v-else>
          <div v-html="form.rt_normalscope" class="rich-text-display"></div>
        </el-form-item>
        <el-form-item label="模板内容" prop="rt_templatecontent" v-if="!isViewMode">
          <WangEditor height="300px" v-model:value="form.rt_templatecontent" />
        </el-form-item>
        <el-form-item label="模板内容" v-else>
          <div v-html="form.rt_templatecontent" class="rich-text-display"></div>
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
  rt_name: ''
})

// 表格数据
const tableData = ref([])
const pagination = reactive({
  current: 1,
  size: 10,
  total: 0
})

// 弹窗控制
const dialogVisible = ref(false)
const dialogTitle = ref('')
const isViewMode = ref(false)

// 表单数据
const form = reactive({
  id: undefined,
  rt_name: '',
  rt_risklevel: '',
  rt_explanation: '',
  rt_suggestions: '',
  rt_normalscope: '',
  rt_templatecontent: ''
})

// 表单引用
const formRef = ref()

// 表单验证规则
const rules = {
  rt_name: [
    { required: true, message: '请输入模板名称', trigger: 'blur' }
  ],
  rt_risklevel: [
    { required: true, message: '请输入适用风险等级', trigger: 'blur' }
  ],
  rt_explanation: [
    { required: true, message: '请输入风险解释', trigger: 'blur' }
  ],
  rt_suggestions: [
    { required: true, message: '请输入建议措施', trigger: 'blur' }
  ],
  rt_normalscope: [
    { required: true, message: '请输入正常范围说明', trigger: 'blur' }
  ],
  rt_templatecontent: [
    { required: true, message: '请输入模板内容', trigger: 'blur' }
  ]
}

// 获取列表数据
const getList = async () => {
  const res = await request('/reporttemplate/index', {
    limit: pagination.size,
    pg: pagination.current,
    rt_name: searchForm.rt_name
  }, 'get')
  tableData.value = res.data
  pagination.total = res.total
}

// 搜索
const handleSearch = () => {
  pagination.current = 1
  getList()
}

// 重置搜索
const resetSearch = () => {
  searchForm.rt_name = ''
  pagination.current = 1
  getList()
}

// 分页大小改变
const handleSizeChange = (val) => {
  pagination.size = val
  getList()
}

// 当前页改变
const handleCurrentChange = (val) => {
  pagination.current = val
  getList()
}

// 新增
const handleAdd = () => {
  dialogTitle.value = '新增报告模板'
  isViewMode.value = false
  Object.assign(form, {
    id: undefined,
    rt_name: '',
    rt_risklevel: '',
    rt_explanation: '',
    rt_suggestions: '',
    rt_normalscope: '',
    rt_templatecontent: ''
  })
  dialogVisible.value = true
}

// 编辑
const handleEdit = (row) => {
  dialogTitle.value = '编辑报告模板'
  isViewMode.value = false
  Object.assign(form, { ...row })
  dialogVisible.value = true
}

// 查看
const handleView = (row) => {
  dialogTitle.value = '查看报告模板'
  isViewMode.value = true
  Object.assign(form, { ...row })
  dialogVisible.value = true
}

// 删除
const handleDelete = async (row) => {
  try {
    await ElMessageBox.confirm(`确定要删除报告模板 "${row.rt_name}" 吗？`, '确认删除', {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning'
    })
    
    await request('/reporttemplate/destroy', { id: row.id }, 'delete')
    ElMessage.success('删除成功')
    getList()
  } catch (error) {
    // 用户取消删除
  }
}

// 提交表单
const submitForm = async () => {
  try {
    await formRef.value.validate()
    
    if (form.id) {
      // 更新
      await request('/reporttemplate/update', { ...form }, 'put')
      ElMessage.success('更新成功')
    } else {
      // 新增
      await request('/reporttemplate/store', { ...form }, 'post')
      ElMessage.success('新增成功')
    }
    
    dialogVisible.value = false
    getList()
  } catch (error) {
    console.error('表单验证失败:', error)
  }
}

// 重置表单
const resetForm = () => {
  if (formRef.value) {
    formRef.value.clearValidate()
  }
}

onMounted(() => {
  getList()
})
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
:deep(.report-template-dialog .el-dialog__header) {
  padding: 24px 24px 0;
}

:deep(.report-template-dialog .el-dialog__body) {
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

.rich-text-display {
  padding: 12px;
  border: 1px solid #dcdfe6;
  border-radius: 4px;
  min-height: 100px;
  background: #f8fafc;
}
</style>