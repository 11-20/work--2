<template>
  <div class="page-container">
    <!-- 筛选区 -->
    <div class="search-area">
      <el-form :model="searchForm" label-width="100px" class="custom-form">
        <el-row :gutter="24">
          <el-col :span="6">
            <el-form-item label="分析类型">
              <el-input v-model="searchForm.ar_type" placeholder="请输入分析类型" clearable />
            </el-form-item>
          </el-col>
          <el-col :span="6">
            <el-form-item label="统计周期">
              <el-input v-model="searchForm.ar_period" placeholder="请输入统计周期" clearable />
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
      <el-button type="primary" class="add-btn" @click="handleAdd">新增分析结果</el-button>
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
        <el-table-column prop="ar_type" label="分析类型" min-width="120" />
        <el-table-column prop="ar_summary" label="分析摘要" min-width="200" show-overflow-tooltip />
        <el-table-column prop="ar_period" label="统计周期" min-width="120" />
        <el-table-column prop="ar_generatedate" label="生成日期" min-width="160" />
        <el-table-column prop="username" label="用户名" min-width="120" />
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

    <!-- 分析结果表单 Dialog -->
    <el-dialog
      :title="dialogTitle"
      v-model="dialogVisible"
      width="700px"
      class="analysis-result-dialog"
      @close="resetForm"
    >
      <el-form :model="analysisResultForm" :rules="rules" ref="analysisResultFormRef" label-width="100px" class="dialog-form">
        <el-form-item label="分析类型" prop="ar_type">
          <el-input v-model="analysisResultForm.ar_type" placeholder="请输入分析类型" :disabled="isViewMode" />
        </el-form-item>
        <el-form-item label="分析摘要" prop="ar_summary">
          <el-input 
            v-model="analysisResultForm.ar_summary" 
            type="textarea" 
            :rows="4" 
            placeholder="请输入分析摘要" 
            :disabled="isViewMode"
          />
        </el-form-item>
        <el-form-item label="统计周期" prop="ar_period">
          <el-input v-model="analysisResultForm.ar_period" placeholder="请输入统计周期" :disabled="isViewMode" />
        </el-form-item>
        <el-form-item label="详细结果数据" prop="ar_resultdata" v-if="!isViewMode">
          <el-input 
            v-model="analysisResultForm.ar_resultdata" 
            type="textarea" 
            :rows="6" 
            placeholder="请输入详细结果数据(JSON或文本)" 
          />
        </el-form-item>
        <el-form-item label="详细结果数据" v-else>
          <el-input 
            v-model="analysisResultForm.ar_resultdata" 
            type="textarea" 
            :rows="6" 
            readonly
          />
        </el-form-item>
        <el-form-item label="生成日期" prop="ar_generatedate" v-if="!isViewMode">
          <el-input v-model="analysisResultForm.ar_generatedate" placeholder="请输入生成日期" />
        </el-form-item>
        <el-form-item label="生成日期" v-else>
          <el-input v-model="analysisResultForm.ar_generatedate" readonly />
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
const pagination = reactive({
  current: 1,
  size: 10,
  total: 0
});
const searchForm = reactive({
  ar_type: '',
  ar_period: ''
});

// 表单相关
const analysisResultFormRef = ref();
const dialogVisible = ref(false);
const isViewMode = ref(false);
const dialogType = ref('add'); // add, edit, view

const analysisResultForm = reactive({
  id: undefined,
  ar_type: '',
  ar_resultdata: '',
  ar_summary: '',
  ar_period: '',
  ar_generatedate: ''
});

// 验证规则
const rules = {
  ar_type: [
    { required: true, message: '请输入分析类型', trigger: 'blur' }
  ],
  ar_summary: [
    { required: true, message: '请输入分析摘要', trigger: 'blur' }
  ],
  ar_period: [
    { required: true, message: '请输入统计周期', trigger: 'blur' }
  ]
};

// 计算属性
const dialogTitle = computed(() => {
  return isViewMode.value ? '查看分析结果' : (analysisResultForm.id ? '编辑分析结果' : '新增分析结果');
});

// 方法
const fetchData = async () => {
  const params = {
    limit: pagination.size,
    pg: pagination.current,
    ar_type: searchForm.ar_type,
    ar_period: searchForm.ar_period
  };
  
  const res = await request('/analysisresult/index', params, 'get');
  tableData.value = res.data;
  pagination.total = res.total;
};

const handleSearch = () => {
  pagination.current = 1;
  fetchData();
};

const resetSearch = () => {
  searchForm.ar_type = '';
  searchForm.ar_period = '';
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
  Object.assign(analysisResultForm, {
    id: undefined,
    ar_type: '',
    ar_resultdata: '',
    ar_summary: '',
    ar_period: '',
    ar_generatedate: ''
  });
  dialogType.value = 'add';
  isViewMode.value = false;
  dialogVisible.value = true;
};

const handleEdit = (row) => {
  Object.assign(analysisResultForm, { ...row });
  dialogType.value = 'edit';
  isViewMode.value = false;
  dialogVisible.value = true;
};

const handleView = (row) => {
  Object.assign(analysisResultForm, { ...row });
  dialogType.value = 'view';
  isViewMode.value = true;
  dialogVisible.value = true;
};

const handleDelete = async (row) => {
  try {
    await ElMessageBox.confirm(`确定要删除该分析结果吗？`, '确认删除', {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning'
    });

    await request(`/analysisresult/destroy?id=${row.id}`, {}, 'delete');
    ElMessage.success('删除成功');
    fetchData();
  } catch (error) {
    console.log('取消删除');
  }
};

const submitForm = async () => {
  try {
    await analysisResultFormRef.value.validate();
    
    if (analysisResultForm.id) {
      // 更新
      await request(`/analysisresult/update?id=${analysisResultForm.id}`, analysisResultForm, 'put');
      ElMessage.success('更新成功');
    } else {
      // 新增
      await request('/analysisresult/store', analysisResultForm, 'post');
      ElMessage.success('新增成功');
    }
    
    dialogVisible.value = false;
    fetchData();
  } catch (error) {
    console.error('表单验证失败或提交错误:', error);
  }
};

const resetForm = () => {
  if (analysisResultFormRef.value) {
    analysisResultFormRef.value.clearValidate();
  }
};

// 初始化
onMounted(() => {
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
:deep(.analysis-result-dialog .el-dialog__header) {
  padding: 24px 24px 0;
}

:deep(.analysis-result-dialog .el-dialog__body) {
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