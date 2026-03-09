<template>
  <div class="user-management-container">
    <!-- 筛选查询区 -->
    <div class="search-area">
      <el-form :model="searchForm" label-width="100px">
        <el-row :gutter="20">
          <el-col :xs="24" :sm="12" :md="8" :lg="6">
            <el-form-item label="用户ID">
              <el-input v-model="searchForm.id" placeholder="请输入用户ID" clearable />
            </el-form-item>
          </el-col>
          <el-col :xs="24" :sm="12" :md="8" :lg="6">
            <el-form-item label="用户名">
              <el-input v-model="searchForm.user_name" placeholder="请输入用户名" clearable />
            </el-form-item>
          </el-col>
        </el-row>
        <el-row>
          <el-col :span="24" style="text-align: right; padding-right: 20px;">
            <div class="form-buttons">
              <button class="custom-btn reset-btn" @click="resetSearch">重置</button>
              <button class="custom-btn search-btn" @click="fetchData">查询</button>
            </div>
          </el-col>
        </el-row>
      </el-form>
    </div>

    <!-- 数据表格区 -->
    <div class="table-area">
      <el-table :data="tableData" stripe style="width: 100%" v-loading="loading">
        <el-table-column prop="id" label="用户ID" width="100" />
        <el-table-column prop="user_name" label="用户名" width="120" />
        <el-table-column prop="avatar" label="头像" width="100">
          <template #default="scope">
            <el-avatar :size="40" :src="scope.row.avatar" v-if="scope.row.avatar" />
            <el-avatar :size="40" v-else>{{ scope.row.user_name?.charAt(0) }}</el-avatar>
          </template>
        </el-table-column>
        <el-table-column prop="createTime" label="创建时间" width="180" />
        <el-table-column label="操作" width="220" fixed="right">
          <template #default="scope">
            <div class="action-buttons">
              <button class="action-btn edit-btn" @click="handleEdit(scope.row)">编辑</button>
              <button class="action-btn delete-btn" @click="handleDelete(scope.row)">删除</button>
            </div>
          </template>
        </el-table-column>
      </el-table>
    </div>

    <!-- 分页区 -->
    <div class="pagination-area">
      <el-pagination
        v-model:current-page="pagination.currentPage"
        v-model:page-size="pagination.pageSize"
        :page-sizes="[10, 20, 50, 100]"
        :small="true"
        :background="true"
        layout="total, sizes, prev, pager, next, jumper"
        :total="pagination.total"
        @size-change="handleSizeChange"
        @current-change="handleCurrentChange"
      />
    </div>

    <!-- 编辑用户对话框 -->
    <el-dialog
      v-model="dialogVisible"
      title="编辑用户"
      width="500px"
      :close-on-click-modal="false"
    >
      <el-form :model="userForm" :rules="rules" ref="userFormRef" label-width="100px">
        <el-form-item label="用户名" prop="user_name">
          <el-input v-model="userForm.user_name" placeholder="请输入用户名" />
        </el-form-item>
        <el-form-item label="头像">
          <UploadImg v-model="userForm.avatar" />
        </el-form-item>
      </el-form>
      <template #footer>
        <span class="dialog-footer">
          <button class="custom-btn cancel-btn" @click="dialogVisible = false">取消</button>
          <button class="custom-btn confirm-btn" @click="submitForm">确定</button>
        </span>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import UploadImg from "@/components/UploadImg/index.vue";
import { GlobalStore } from '@/stores';
const globalStore = GlobalStore();

// 搜索表单
const searchForm = reactive({
  id: '',
  user_name: ''
})

// 表格数据
const tableData = ref([])
const loading = ref(false)

// 分页配置
const pagination = reactive({
  currentPage: 1,
  pageSize: 10,
  total: 0
})

// 对话框控制
const dialogVisible = ref(false)
const userFormRef = ref()
const userForm = reactive({
  id: '',
  user_name: '',
  avatar: ''
})

// 表单验证规则
const rules = reactive({
  user_name: [
    { required: true, message: '请输入用户名', trigger: 'blur' }
  ]
})

// 获取用户列表
const fetchData = async () => {
  loading.value = true
  try {
    const params = {
      limit: pagination.pageSize,
      pg: pagination.currentPage,
      ...searchForm
    }
    
    const res = await request('/user/index', params, 'get')
    tableData.value = res.data.list || []
    pagination.total = res.data.total || 0
  } catch (error) {
    console.error('获取用户列表失败:', error)
  } finally {
    loading.value = false
  }
}

// 重置搜索
const resetSearch = () => {
  searchForm.id = ''
  searchForm.user_name = ''
  pagination.currentPage = 1
  fetchData()
}

// 分页大小改变
const handleSizeChange = (size) => {
  pagination.pageSize = size
  pagination.currentPage = 1
  fetchData()
}

// 当前页改变
const handleCurrentChange = (page) => {
  pagination.currentPage = page
  fetchData()
}

// 编辑用户
const handleEdit = (row) => {
  Object.assign(userForm, row)
  dialogVisible.value = true
}

// 删除用户
const handleDelete = (row) => {
  ElMessageBox.confirm('确定要删除该用户吗？', '提示', {
    confirmButtonText: '确定',
    cancelButtonText: '取消',
    type: 'warning'
  }).then(async () => {
    try {
      await request('/user/destory', { id: row.id }, 'delete')
      ElMessage.success('删除成功')
      fetchData()
    } catch (error) {
      console.error('删除用户失败:', error)
    }
  }).catch(() => {})
}

// 提交表单
const submitForm = async () => {
  if (!userFormRef.value) return
  
  try {
    await userFormRef.value.validate()
    
    await request('/user/update', userForm, 'put')
    ElMessage.success('更新成功')
    dialogVisible.value = false
    fetchData()
  } catch (error) {
    console.error('表单验证或提交失败:', error)
  }
}

// 初始化加载数据
onMounted(() => {
  fetchData()
})
</script>

<style scoped>
.user-management-container {
  padding: 20px;
  background-color: #f5f7fa;
  min-height: 100%
}

.search-area {
  background: #fff;
  padding: 20px;
  border-radius: 10px;
  box-shadow: 0 2px 12px 0 rgba(0,0,0,0.1);
  margin-bottom: 20px
}

.table-area {
  background: #fff;
  padding: 20px;
  border-radius: 10px;
  box-shadow: 0 2px 12px 0 rgba(0,0,0,0.1);
  margin-bottom: 20px
}

.pagination-area {
  background: #fff;
  padding: 15px 20px;
  border-radius: 10px;
  box-shadow: 0 2px 12px 0 rgba(0,0,0,0.1);
  display: flex;
  justify-content: flex-end
}

.form-buttons {
  display: flex;
  gap: 12px;
  justify-content: flex-end
}

.action-buttons {
  display: flex;
  gap: 10px
}

.custom-btn {
  padding: 10px 20px;
  border: none;
  border-radius: 6px;
  font-size: 14px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.3s ease;
  outline: none
}

.reset-btn {
  background-color: #f4f4f5;
  color: #909399
}

.reset-btn:hover {
  background-color: #e9e9eb;
  color: #82848a
}

.search-btn {
  background-color: #409EFF;
  color: white
}

.search-btn:hover {
  background-color: #66b1ff
}

.action-btn {
  padding: 6px 12px;
  border: none;
  border-radius: 4px;
  font-size: 12px;
  cursor: pointer;
  transition: all 0.2s ease
}

.edit-btn {
  background-color: #f0f9eb;
  color: #67C23A
}

.edit-btn:hover {
  background-color: #67C23A;
  color: white
}

.delete-btn {
  background-color: #fef0f0;
  color: #F56C6C
}

.delete-btn:hover {
  background-color: #F56C6C;
  color: white
}

.cancel-btn {
  background-color: #f4f4f5;
  color: #909399
}

.cancel-btn:hover {
  background-color: #e9e9eb
}

.confirm-btn {
  background: linear-gradient(135deg, #ff7c7c 0%, #ff5e5e 100%);
  color: white
}

.confirm-btn:hover {
  background: linear-gradient(135deg, #ff5e5e 0%, #ff4040 100%)
}

.dialog-footer {
  display: flex;
  gap: 10px;
  justify-content: flex-end
}

:deep(.el-form-item__label) {
  font-weight: 500
}

:deep(.el-table th) {
  background-color: #f5f7fa;
  color: #606266;
  font-weight: 600
}

:deep(.el-table .cell) {
  padding: 8px 12px
}
</style>