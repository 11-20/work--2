<template>
  <div class="page-container">
    <!-- 筛选区 -->
    <div class="search-area">
      <el-form :model="searchForm" label-width="80px" class="custom-form">
        <el-row :gutter="24">
          <el-col :span="6">
            <el-form-item label="用户名">
              <el-input v-model="searchForm.username" placeholder="请输入用户名" clearable />
            </el-form-item>
          </el-col>
          <el-col :span="6">
            <el-form-item label="真实姓名">
              <el-input v-model="searchForm.realName" placeholder="请输入真实姓名" clearable />
            </el-form-item>
          </el-col>
          <el-col :span="6">
            <el-form-item label="邮箱">
              <el-input v-model="searchForm.email" placeholder="请输入邮箱" clearable />
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
      <el-button type="primary" class="add-btn" @click="handleAdd">新增用户</el-button>
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
        <el-table-column prop="id" label="ID" width="80" align="center" />
        <el-table-column prop="username" label="用户名" min-width="120" />
        <el-table-column prop="realName" label="真实姓名" min-width="120" />
        <el-table-column prop="email" label="邮箱" min-width="180" />
        <el-table-column prop="role" label="角色" min-width="100">
          <template #default="{ row }">
            <el-tag :type="row.role == 'admin' ? 'danger' : 'success'" size="small">
              {{ row.role == 'admin' ? '管理员' : '普通用户' }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="createTime" label="创建时间" min-width="160" />
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

    <!-- 用户表单 Dialog -->
    <el-dialog
      :title="dialogTitle"
      v-model="dialogVisible"
      width="500px"
      class="user-dialog"
      @close="resetForm"
    >
      <el-form :model="userForm" :rules="rules" ref="userFormRef" label-width="80px" class="dialog-form">
        <el-form-item label="用户名" prop="username">
          <el-input v-model="userForm.username" placeholder="请输入用户名" :disabled="isViewMode" />
        </el-form-item>
        <el-form-item label="真实姓名" prop="realName">
          <el-input v-model="userForm.realName" placeholder="请输入真实姓名" :disabled="isViewMode" />
        </el-form-item>
        <el-form-item label="邮箱" prop="email">
          <el-input v-model="userForm.email" placeholder="请输入邮箱" :disabled="isViewMode" />
        </el-form-item>
        <el-form-item label="角色" prop="role" v-if="!isViewMode">
          <el-select v-model="userForm.role" placeholder="请选择角色" style="width: 100%">
            <el-option label="管理员" value="admin" />
            <el-option label="普通用户" value="user" />
          </el-select>
        </el-form-item>
        <el-form-item label="密码" prop="password" v-if="!isViewMode && userForm.id == undefined">
          <el-input v-model="userForm.password" type="password" placeholder="请输入密码" />
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
import { ref, reactive, computed, watch, onMounted, onUnmounted } from 'vue'
import { request } from "@/http/index";
import { GlobalStore } from "@/stores";
import { useRoute, useRouter } from "vue-router";
import { ElMessage, ElMessageBox } from 'element-plus'

const router = useRouter();
const route = useRoute();
const globalStore = GlobalStore();

// 表单引用
const userFormRef = ref()

// 搜索表单
const searchForm = reactive({
  username: '',
  realName: '',
  email: ''
})

// 分页配置
const pagination = reactive({
  current: 1,
  size: 10,
  total: 0
})

// 表格数据
const tableData = ref([])

// Dialog 相关
const dialogVisible = ref(false)
const isViewMode = ref(false)
const dialogTitle = ref('')

// 用户表单
const userForm = reactive({
  id: undefined,
  username: '',
  realName: '',
  email: '',
  role: 'user',
  password: ''
})

// 表单验证规则
const rules = {
  username: [
    { required: true, message: '请输入用户名', trigger: 'blur' },
    { min: 3, max: 20, message: '长度在 3 到 20 个字符', trigger: 'blur' }
  ],
  realName: [
    { required: true, message: '请输入真实姓名', trigger: 'blur' }
  ],
  email: [
    { required: true, message: '请输入邮箱', trigger: 'blur' },
    { type: 'email', message: '请输入正确的邮箱格式', trigger: 'blur' }
  ],
  password: [
    { required: true, message: '请输入密码', trigger: 'blur' },
    { min: 6, message: '密码长度至少6位', trigger: 'blur' }
  ]
}

// 获取数据
const fetchData = async () => {
  try {
    const params = {
      page: pagination.current,
      size: pagination.size,
      ...searchForm
    }
    // 模拟API调用
    // const res = await request('/users/list', params, 'get')
    // tableData.value = res.data.list
    // pagination.total = res.data.total
    
    // 模拟数据
    const mockData = Array.from({ length: 5 }, (_, index) => ({
      id: (pagination.current - 1) * pagination.size + index + 1,
      username: `user${(pagination.current - 1) * pagination.size + index + 1}`,
      realName: `用户${(pagination.current - 1) * pagination.size + index + 1}`,
      email: `user${(pagination.current - 1) * pagination.size + index + 1}@example.com`,
      role: index % 3 == 0 ? 'admin' : 'user',
      createTime: new Date().toLocaleString()
    }))
    tableData.value = mockData
    pagination.total = 100
  } catch (error) {
    ElMessage.error('获取数据失败')
  }
}

// 查询
const handleSearch = () => {
  pagination.current = 1
  fetchData()
}

// 重置搜索
const resetSearch = () => {
  Object.keys(searchForm).forEach(key => {
    searchForm[key] = ''
  })
  pagination.current = 1
  fetchData()
}

// 查看
const handleView = (row) => {
  Object.assign(userForm, { ...row })
  dialogTitle.value = '查看用户'
  isViewMode.value = true
  dialogVisible.value = true
}

// 编辑
const handleEdit = (row) => {
  Object.assign(userForm, { ...row })
  dialogTitle.value = '编辑用户'
  isViewMode.value = false
  dialogVisible.value = true
}

// 新增
const handleAdd = () => {
  resetForm()
  dialogTitle.value = '新增用户'
  isViewMode.value = false
  dialogVisible.value = true
}

// 重置表单
const resetForm = () => {
  userForm.id = undefined
  userForm.username = ''
  userForm.realName = ''
  userForm.email = ''
  userForm.role = 'user'
  userForm.password = ''
  if (userFormRef.value) {
    userFormRef.value.clearValidate()
  }
}

// 提交表单
const submitForm = async () => {
  if (!userFormRef.value) return
  
  try {
    await userFormRef.value.validate()
    // 模拟API调用
    // if (userForm.id) {
    //   await request('/users/update', userForm, 'put')
    // } else {
    //   await request('/users/create', userForm, 'post')
    // }
    ElMessage.success('操作成功')
    dialogVisible.value = false
    fetchData()
  } catch (error) {
    ElMessage.error('操作失败')
  }
}

// 删除
const handleDelete = (row) => {
  ElMessageBox.confirm('确定要删除该用户吗?', '提示', {
    confirmButtonText: '确定',
    cancelButtonText: '取消',
    type: 'warning'
  }).then(() => {
    // 模拟API调用
    // await request('/users/destroy', { id: row.id }, 'delete')
    ElMessage.success('删除成功')
    fetchData()
  }).catch(() => {
    ElMessage.info('已取消删除')
  })
}

// 分页事件
const handleSizeChange = (val) => {
  pagination.size = val
  fetchData()
}

const handleCurrentChange = (val) => {
  pagination.current = val
  fetchData()
}

onMounted(async () => {
  fetchData()
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
:deep(.user-dialog .el-dialog__header) {
  padding: 24px 24px 0;
}

:deep(.user-dialog .el-dialog__body) {
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