<template>
  <div class="page-container">
    <!-- 操作按钮区 -->
    <div class="action-area">
      <el-button type="primary" class="add-btn" @click="handleAdd">新增轮播图</el-button>
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
        <el-table-column prop="ca_title" label="轮播图标题" min-width="200" />
        <el-table-column prop="ca_cover" label="轮播图图片" min-width="150">
          <template #default="{ row }">
            <el-image
              v-if="row.ca_cover"
              :src="row.ca_cover"
              :preview-src-list="[row.ca_cover]"
              fit="cover"
              style="width: 100px; height: 60px;"
              preview-teleported
            />
            <span v-else>暂无图片</span>
          </template>
        </el-table-column>
        <el-table-column prop="ca_excerpt" label="轮播图简介" min-width="250" />
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

    <!-- 轮播图表单 Dialog -->
    <el-dialog
      :title="dialogTitle"
      v-model="dialogVisible"
      width="600px"
      class="carousel-dialog"
      @close="resetForm"
    >
      <el-form :model="carouselForm" :rules="rules" ref="carouselFormRef" label-width="100px" class="dialog-form">
        <el-form-item label="轮播图标题" prop="ca_title">
          <el-input v-model="carouselForm.ca_title" placeholder="请输入轮播图标题" :disabled="isViewMode" />
        </el-form-item>
        <el-form-item label="轮播图图片" prop="ca_cover">
          <UploadImg v-model:imageUrl="carouselForm.ca_cover" v-if="!isViewMode" />
          <div v-else>
            <el-image
              :src="carouselForm.ca_cover"
              :preview-src-list="[carouselForm.ca_cover]"
              fit="cover"
              style="width: 200px; height: 120px;"
              preview-teleported
            />
          </div>
        </el-form-item>
        <el-form-item label="轮播图简介" prop="ca_excerpt">
          <el-input 
            v-model="carouselForm.ca_excerpt" 
            placeholder="请输入轮播图简介" 
            :disabled="isViewMode"
            type="textarea"
            :rows="4"
          />
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
const dialogVisible = ref(false);
const isViewMode = ref(false);
const dialogTitle = ref('');

// 分页数据
const pagination = reactive({
  current: 1,
  size: 10,
  total: 0
});

// 搜索表单
const searchForm = reactive({
  ca_title: ''
});

// 轮播图表单
const carouselForm = reactive({
  id: undefined,
  ca_title: '',
  ca_cover: '',
  ca_excerpt: ''
});

// 表单验证规则
const rules = {
  ca_title: [
    { required: true, message: '请输入轮播图标题', trigger: 'blur' }
  ],
  ca_cover: [
    { required: true, message: '请上传轮播图图片', trigger: 'change' }
  ],
  ca_excerpt: [
    { required: true, message: '请输入轮播图简介', trigger: 'blur' }
  ]
};

// 表单引用
const carouselFormRef = ref();

// 初始化数据
onMounted(() => {
  fetchData();
});

// 获取数据
const fetchData = async () => {
  const params = {
    limit: pagination.size,
    pg: pagination.current,
    ca_title: searchForm.ca_title
  };
  
  const res = await request('/carousel/index', params, 'get');
  tableData.value = res.data;
  pagination.total = res.total;
};

// 处理搜索
const handleSearch = () => {
  pagination.current = 1;
  fetchData();
};

// 重置搜索
const resetSearch = () => {
  searchForm.ca_title = '';
  pagination.current = 1;
  fetchData();
};

// 处理分页大小变化
const handleSizeChange = (val) => {
  pagination.size = val;
  fetchData();
};

// 处理当前页变化
const handleCurrentChange = (val) => {
  pagination.current = val;
  fetchData();
};

// 新增轮播图
const handleAdd = () => {
  dialogTitle.value = '新增轮播图';
  isViewMode.value = false;
  carouselForm.id = undefined;
  resetForm();
  dialogVisible.value = true;
};

// 查看轮播图
const handleView = (row) => {
  dialogTitle.value = '查看轮播图';
  isViewMode.value = true;
  Object.assign(carouselForm, row);
  dialogVisible.value = true;
};

// 编辑轮播图
const handleEdit = (row) => {
  dialogTitle.value = '编辑轮播图';
  isViewMode.value = false;
  Object.assign(carouselForm, row);
  dialogVisible.value = true;
};

// 删除轮播图
const handleDelete = async (row) => {
  try {
    await ElMessageBox.confirm(`确定要删除轮播图 "${row.ca_title}" 吗？`, '确认删除', {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning'
    });
    
    await request(`/carousel/destroy?id=${row.id}`, {}, 'delete');
    ElMessage.success('删除成功');
    fetchData();
  } catch (error) {
    console.log('取消删除');
  }
};

// 提交表单
const submitForm = async () => {
  try {
    await carouselFormRef.value.validate();
    
    if (carouselForm.id) {
      // 更新
      await request(`/carousel/update?id=${carouselForm.id}`, carouselForm, 'put');
      ElMessage.success('更新成功');
    } else {
      // 新增
      await request('/carousel/store', carouselForm, 'post');
      ElMessage.success('新增成功');
    }
    
    dialogVisible.value = false;
    fetchData();
  } catch (error) {
    console.log('表单验证失败', error);
  }
};

// 重置表单
const resetForm = () => {
  carouselForm.id = undefined;
  carouselForm.ca_title = '';
  carouselForm.ca_cover = '';
  carouselForm.ca_excerpt = '';
};
</script>

<style scoped>
.page-container {
  padding: 24px;
  background: #f8fafc;
  min-height: 100vh;
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
:deep(.carousel-dialog .el-dialog__header) {
  padding: 24px 24px 0;
}

:deep(.carousel-dialog .el-dialog__body) {
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