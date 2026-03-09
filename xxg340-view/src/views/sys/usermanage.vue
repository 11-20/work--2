<template>
  <div class="page-container">
    <!-- 筛选区 -->
    <div class="search-area">
      <el-form :model="searchForm" label-width="80px" class="custom-form">
        <el-row :gutter="24">
          <el-col :span="6">
            <el-form-item label="用户名">
              <el-input v-model="searchForm.user_name" placeholder="请输入用户名" clearable />
            </el-form-item>
          </el-col>
          <el-col :span="6">
            <el-form-item label="手机号">
              <el-input v-model="searchForm.phone" placeholder="请输入手机号" clearable />
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
        <el-table-column prop="user_name" label="用户名" min-width="120" />
        <el-table-column prop="phone" label="手机号码" min-width="140" />
        <el-table-column prop="email" label="邮箱" min-width="180" />
        <el-table-column prop="sex" label="性别" min-width="100">
          <template #default="{ row }">
            <el-tag :type="row.sex == 1 ? 'primary' : 'danger'" size="small">
              {{ row.sex == 1 ? '男' : '女' }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column label="头像" width="100" align="center">
          <template #default="{ row }">
            <el-avatar :src="row.avatar || defaultAvatar" size="small" />
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

    <!-- 用户表单 Dialog -->
    <el-dialog
      :title="dialogTitle"
      v-model="dialogVisible"
      width="500px"
      class="user-dialog"
      @close="resetForm"
    >
      <el-form :model="formData" :rules="formRules" ref="userFormRef" label-width="80px" class="dialog-form">
        <el-form-item label="用户名" prop="user_name">
          <el-input v-model="formData.user_name" placeholder="请输入用户名" :disabled="isViewMode" />
        </el-form-item>
        <el-form-item label="手机号码" prop="phone">
          <el-input v-model="formData.phone" placeholder="请输入手机号码" :disabled="isViewMode" />
        </el-form-item>
        <el-form-item label="邮箱" prop="email">
          <el-input v-model="formData.email" placeholder="请输入邮箱" :disabled="isViewMode" />
        </el-form-item>
        <el-form-item label="性别" prop="sex" v-if="!isViewMode">
          <el-select v-model="formData.sex" placeholder="请选择性别" style="width: 100%">
            <el-option label="男" :value="1" />
            <el-option label="女" :value="2" />
          </el-select>
        </el-form-item>
        <el-form-item label="头像" prop="avatar" v-if="!isViewMode">
          <UploadImg v-model:imageUrl="formData.avatar" />
        </el-form-item>
        <el-form-item label="密码" prop="password" v-if="!isViewMode && formData.id == undefined">
          <el-input v-model="formData.password" type="password" placeholder="请输入密码" />
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

const userInfo = globalStore.userInfo

// 默认头像
const defaultAvatar = 'https://cube.elemecdn.com/3/7c/3ea6beec64369c2642b92c6726f1epng.png';

// 表格数据
const tableData = ref([]);

// 搜索表单
const searchForm = reactive({
  user_name: '',
  phone: '',
  email: ''
});

// 分页配置
const pagination = reactive({
  current: 1,
  size: 10,
  total: 0
});

// 对话框相关
const dialogVisible = ref(false);
const dialogTitle = ref('');
const isViewMode = ref(false);

// 表单引用
const userFormRef = ref();

// 表单数据
const formData = reactive({
  id: undefined,
  user_name: '',
  phone: '',
  email: '',
  sex: 1,
  avatar: '',
  password: '' // 只在新增时使用
});

// 表单验证规则
const formRules = {
  user_name: [
    { required: true, message: '请输入用户名', trigger: 'blur' },
    { min: 2, max: 20, message: '长度在 2 到 20 个字符', trigger: 'blur' }
  ],
  phone: [
    { required: true, message: '请输入手机号', trigger: 'blur' },
    { pattern: /^1[3-9]\d{9}$/, message: '请输入正确的手机号', trigger: 'blur' }
  ],
  email: [
    { required: true, message: '请输入邮箱地址', trigger: 'blur' },
    { type: 'email', message: '请输入正确的邮箱地址', trigger: 'blur' }
  ],
  sex: [
    { required: true, message: '请选择性别', trigger: 'change' }
  ],
  password: [
    { required: true, message: '请输入密码', trigger: 'blur' },
    { min: 6, max: 20, message: '密码长度应在 6 到 20 位之间', trigger: 'blur' }
  ]
};

// 获取用户列表
const getUserList = async () => {
  try {
    const params = {
      pg: pagination.current,
      limit: pagination.size,
      role_id: 3,
      ...searchForm
    };

    const res = await request('/user/index', params, 'get');
    
    if (res && res.data) {
      tableData.value = res.data;
      pagination.total = res.total || 0;
    } else {
      tableData.value = [];
      pagination.total = 0;
    }
  } catch (error) {
    console.error('获取用户列表失败:', error);
    ElMessage.error('获取用户列表失败');
  }
};

// 处理搜索
const handleSearch = () => {
  pagination.current = 1;
  getUserList();
};

// 重置搜索
const resetSearch = () => {
  searchForm.user_name = '';
  searchForm.phone = '';
  searchForm.email = '';
  pagination.current = 1;
  getUserList();
};

// 处理添加
const handleAdd = () => {
  isViewMode.value = false;
  dialogTitle.value = '添加用户';
  dialogVisible.value = true;
  
  // 重置表单
  Object.assign(formData, {
    id: undefined,
    user_name: '',
    phone: '',
    email: '',
    sex: 1,
    avatar: '',
    password: '',
    role_id: 3,
  });
};

// 处理编辑
const handleEdit = (row) => {
  isViewMode.value = false;
  dialogTitle.value = '编辑用户';
  dialogVisible.value = true;
  
  // 填充表单数据
  Object.assign(formData, {
    id: row.id,
    user_name: row.user_name,
    phone: row.phone,
    email: row.email,
    sex: row.sex,
    avatar: row.avatar
  });
};

// 处理查看
const handleView = (row) => {
  isViewMode.value = true;
  dialogTitle.value = '查看用户';
  dialogVisible.value = true;
  
  // 填充表单数据
  Object.assign(formData, {
    id: row.id,
    user_name: row.user_name,
    phone: row.phone,
    email: row.email,
    sex: row.sex,
    avatar: row.avatar
  });
};

// 处理删除
const handleDelete = (row) => {
  ElMessageBox.confirm(
    `确定要删除用户 "${row.user_name}" 吗？此操作不可恢复！`,
    '警告',
    {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning'
    }
  ).then(async () => {
    try {
      const res = await request('/user/destroy', { id: row.id }, 'delete');
      
      if (res) {
        ElMessage.success('删除成功');
        // 如果当前页只剩一条数据且不是第一页，则回到上一页
        if (tableData.value.length == 1 && pagination.current > 1) {
          pagination.current--;
        }
        getUserList();
      } else {
        ElMessage.error('删除失败');
      }
    } catch (error) {
      console.error('删除失败:', error);
      ElMessage.error('删除失败');
    }
  }).catch(() => {
    // 用户取消删除
  });
};

// 提交表单
const submitForm = async () => {
  if (!userFormRef.value) return;

  await userFormRef.value.validate(async (valid) => {
    if (!valid) return;

    try {
      let res;
      
      if (!formData.id) {
        // 新增用户
        res = await request('/user/store', formData, 'post');
      } else {
        // 更新用户
        res = await request('/user/update', formData, 'put');
      }

      if (res) {
        ElMessage.success(!formData.id ? '添加成功' : '更新成功');
        dialogVisible.value = false;
        getUserList();
      } else {
        ElMessage.error(!formData.id ? '添加失败' : '更新失败');
      }
    } catch (error) {
      console.error('操作失败:', error);
      ElMessage.error(!formData.id ? '添加失败' : '更新失败');
    }
  });
};

// 重置表单
const resetForm = () => {
  if (userFormRef.value) {
    userFormRef.value.clearValidate();
  }
};

// 处理分页大小变化
const handleSizeChange = (val) => {
  pagination.size = val;
  pagination.current = 1;
  getUserList();
};

// 处理当前页变化
const handleCurrentChange = (val) => {
  pagination.current = val;
  getUserList();
};

// 组件挂载时获取数据
onMounted(() => {
  getUserList();
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