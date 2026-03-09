<template>
  <div class="page-container">
    <!-- 筛选区 -->
    <div class="search-area">
      <el-form :model="searchForm" label-width="80px" class="custom-form">
        <el-row :gutter="24">
          <el-col :span="6">
            <el-form-item label="公告标题">
              <el-input v-model="searchForm.no_title" placeholder="请输入公告标题" clearable />
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
      <el-button type="primary" class="add-btn" @click="handleAdd">新增公告</el-button>
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
        <el-table-column prop="no_title" label="公告标题" min-width="200" />
        <el-table-column prop="no_excerpt" label="公告摘要" min-width="300" show-tooltip-when-overflow />
        <el-table-column prop="cd" label="创建时间" width="160" />
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

    <!-- 公告表单 Dialog -->
    <el-dialog
      :title="dialogTitle"
      v-model="dialogVisible"
      width="800px"
      class="notice-dialog"
      @close="resetForm"
    >
      <el-form :model="noticeForm" :rules="rules" ref="noticeFormRef" label-width="80px" class="dialog-form">
        <el-form-item label="公告标题" prop="no_title">
          <el-input v-model="noticeForm.no_title" placeholder="请输入公告标题" :disabled="isViewMode" />
        </el-form-item>
        <el-form-item label="公告摘要" prop="no_excerpt">
          <el-input 
            v-model="noticeForm.no_excerpt" 
            placeholder="请输入公告摘要" 
            :rows="4"
            type="textarea"
            :disabled="isViewMode"
          />
        </el-form-item>
        <el-form-item label="公告内容" prop="no_content" v-if="!isViewMode">
          <WangEditor height="400px" v-model:value="noticeForm.no_content" />
        </el-form-item>
        <el-form-item label="公告内容" v-else>
          <div class="content-view" v-html="noticeForm.no_content"></div>
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
  no_title: ''
})

// 分页配置
const pagination = reactive({
  current: 1,
  size: 10,
  total: 0
})

// 表格数据
const tableData = ref([])

// 弹窗相关
const dialogVisible = ref(false)
const isViewMode = ref(false)
const dialogTitle = ref('')
const noticeFormRef = ref()

// 公告表单
const noticeForm = reactive({
  id: undefined,
  no_title: '',
  no_excerpt: '',
  no_content: ''
})

// 表单验证规则
const rules = {
  no_title: [
    { required: true, message: '请输入公告标题', trigger: 'blur' }
  ],
  no_excerpt: [
    { required: true, message: '请输入公告摘要', trigger: 'blur' }
  ],
  no_content: [
    { required: true, message: '请输入公告内容', trigger: 'change' }
  ]
}

// 获取数据列表
const getDataList = async () => {
  const params = {
    limit: pagination.size,
    pg: pagination.current,
    ...searchForm
  }
  const res = await request('/notice/index', params, 'get')
  tableData.value = res.data
  pagination.total = res.total
}

// 搜索
const handleSearch = () => {
  pagination.current = 1
  getDataList()
}

// 重置搜索
const resetSearch = () => {
  searchForm.no_title = ''
  pagination.current = 1
  getDataList()
}

// 分页大小改变
const handleSizeChange = (val) => {
  pagination.size = val
  pagination.current = 1
  getDataList()
}

// 当前页改变
const handleCurrentChange = (val) => {
  pagination.current = val
  getDataList()
}

// 新增
const handleAdd = () => {
  resetForm()
  dialogTitle.value = '新增公告'
  dialogVisible.value = true
  isViewMode.value = false
}

// 查看
const handleView = (row) => {
  Object.assign(noticeForm, row)
  dialogTitle.value = '查看公告'
  dialogVisible.value = true
  isViewMode.value = true
}

// 编辑
const handleEdit = (row) => {
  Object.assign(noticeForm, row)
  dialogTitle.value = '编辑公告'
  dialogVisible.value = true
  isViewMode.value = false
}

// 删除
const handleDelete = async (row) => {
  try {
    await ElMessageBox.confirm(`确定要删除公告 "${row.no_title}" 吗？`, '确认删除', {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning'
    })
    
    await request('/notice/destroy', { id: row.id }, 'delete')
    ElMessage.success('删除成功')
    getDataList()
  } catch (error) {
    // 用户取消删除
  }
}

// 提交表单
const submitForm = async () => {
  try {
    await noticeFormRef.value.validate()
    
    if (noticeForm.id) {
      // 更新
      await request('/notice/update', noticeForm, 'put')
      ElMessage.success('更新成功')
    } else {
      // 新增
      await request('/notice/store', noticeForm, 'post')
      ElMessage.success('新增成功')
    }
    
    dialogVisible.value = false
    getDataList()
  } catch (error) {
    console.error('提交失败:', error)
  }
}

// 重置表单
const resetForm = () => {
  noticeForm.id = undefined
  noticeForm.no_title = ''
  noticeForm.no_excerpt = ''
  noticeForm.no_content = ''
}

// 初始化
onMounted(() => {
  getDataList()
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
:deep(.notice-dialog .el-dialog__header) {
  padding: 24px 24px 0;
}

:deep(.notice-dialog .el-dialog__body) {
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

.content-view {
  padding: 16px;
  border: 1px solid #dcdfe6;
  border-radius: 4px;
  background-color: #f8fafc;
  min-height: 200px;
  max-height: 400px;
  overflow-y: auto;
}
</style>