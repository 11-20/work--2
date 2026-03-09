<template>
  <div class="page-container">
    <!-- 筛选区 -->
    <div class="search-area">
      <el-form :model="searchForm" label-width="100px" class="custom-form">
        <el-row :gutter="24">
          <el-col :span="6">
            <el-form-item label="统计日期">
              <el-date-picker
                v-model="searchForm.hs_date"
                type="date"
                placeholder="请选择统计日期"
                format="YYYY-MM-DD"
                value-format="YYYY-MM-DD"
                clearable
              />
            </el-form-item>
          </el-col>
          <el-col :span="6">
            <el-form-item label="统计类型">
              <el-input v-model="searchForm.hs_type" placeholder="请输入统计类型" clearable />
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
      <el-button type="primary" class="add-btn" @click="handleAdd">新增统计</el-button>
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
        <el-table-column prop="hs_date" label="统计日期" width="120" align="center" />
        <el-table-column prop="hs_type" label="统计类型" min-width="120" />
        <el-table-column prop="hs_avgbmi" label="平均BMI" width="100" align="center" />
        <el-table-column prop="hs_avgsbp" label="平均收缩压" width="120" align="center" />
        <el-table-column prop="hs_avgdbp" label="平均舒张压" width="120" align="center" />
        <el-table-column prop="hs_avgchol" label="平均总胆固醇" width="130" align="center" />
        <el-table-column prop="hs_highriskrate" label="高风险比例" width="120" align="center" />
        <el-table-column prop="hs_normalrate" label="正常指标比例" width="120" align="center" />
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

    <!-- 健康统计汇总表单 Dialog -->
    <el-dialog
      :title="dialogTitle"
      v-model="dialogVisible"
      width="600px"
      class="health-summary-dialog"
      @close="resetForm"
    >
      <el-form :model="healthSummaryForm" :rules="rules" ref="healthSummaryFormRef" label-width="120px" class="dialog-form">
        <el-form-item label="统计日期" prop="hs_date">
          <el-date-picker
            v-model="healthSummaryForm.hs_date"
            type="date"
            placeholder="请选择统计日期"
            format="YYYY-MM-DD"
            value-format="YYYY-MM-DD"
            style="width: 100%"
            :disabled="isViewMode"
          />
        </el-form-item>
        <el-form-item label="统计类型" prop="hs_type">
          <el-input v-model="healthSummaryForm.hs_type" placeholder="请输入统计类型" :disabled="isViewMode" />
        </el-form-item>
        <el-form-item label="平均BMI" prop="hs_avgbmi">
          <el-input v-model="healthSummaryForm.hs_avgbmi" placeholder="请输入平均BMI" :disabled="isViewMode" />
        </el-form-item>
        <el-form-item label="平均收缩压" prop="hs_avgsbp">
          <el-input v-model="healthSummaryForm.hs_avgsbp" placeholder="请输入平均收缩压" :disabled="isViewMode" />
        </el-form-item>
        <el-form-item label="平均舒张压" prop="hs_avgdbp">
          <el-input v-model="healthSummaryForm.hs_avgdbp" placeholder="请输入平均舒张压" :disabled="isViewMode" />
        </el-form-item>
        <el-form-item label="平均总胆固醇" prop="hs_avgchol">
          <el-input v-model="healthSummaryForm.hs_avgchol" placeholder="请输入平均总胆固醇" :disabled="isViewMode" />
        </el-form-item>
        <el-form-item label="高风险比例" prop="hs_highriskrate">
          <el-input v-model="healthSummaryForm.hs_highriskrate" placeholder="请输入高风险比例" :disabled="isViewMode" />
        </el-form-item>
        <el-form-item label="正常指标比例" prop="hs_normalrate">
          <el-input v-model="healthSummaryForm.hs_normalrate" placeholder="请输入正常指标比例" :disabled="isViewMode" />
        </el-form-item>
        <el-form-item label="汇总数据JSON" prop="hs_summarydata" v-if="!isViewMode">
          <el-input
            v-model="healthSummaryForm.hs_summarydata"
            type="textarea"
            :rows="4"
            placeholder="请输入汇总数据JSON"
          />
        </el-form-item>
        <el-form-item label="汇总数据JSON" v-else>
          <el-input
            v-model="healthSummaryForm.hs_summarydata"
            type="textarea"
            :rows="4"
            readonly
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

// 页面数据
const tableData = ref([]);
const pagination = reactive({
  current: 1,
  size: 10,
  total: 0
});

// 搜索表单
const searchForm = reactive({
  hs_date: '',
  hs_type: ''
});

// 弹窗相关
const dialogVisible = ref(false);
const dialogTitle = ref('');
const isViewMode = ref(false);

// 健康统计汇总表单
const healthSummaryForm = reactive({
  id: undefined,
  hs_date: '',
  hs_type: '',
  hs_avgbmi: '',
  hs_avgsbp: '',
  hs_avgdbp: '',
  hs_avgchol: '',
  hs_highriskrate: '',
  hs_normalrate: '',
  hs_summarydata: ''
});

// 表单验证规则
const rules = {
  hs_date: [
    { required: true, message: '请输入统计日期', trigger: 'blur' }
  ],
  hs_type: [
    { required: true, message: '请输入统计类型', trigger: 'blur' }
  ],
  hs_avgbmi: [
    { required: true, message: '请输入平均BMI', trigger: 'blur' }
  ],
  hs_avgsbp: [
    { required: true, message: '请输入平均收缩压', trigger: 'blur' }
  ],
  hs_avgdbp: [
    { required: true, message: '请输入平均舒张压', trigger: 'blur' }
  ],
  hs_avgchol: [
    { required: true, message: '请输入平均总胆固醇', trigger: 'blur' }
  ],
  hs_highriskrate: [
    { required: true, message: '请输入高风险比例', trigger: 'blur' }
  ],
  hs_normalrate: [
    { required: true, message: '请输入正常指标比例', trigger: 'blur' }
  ]
};

// 初始化数据
onMounted(() => {
  fetchHealthSummaryList();
});

// 获取健康统计汇总列表
const fetchHealthSummaryList = async () => {
  try {
    const params = {
      limit: pagination.size,
      pg: pagination.current,
      hs_date: searchForm.hs_date || '',
      hs_type: searchForm.hs_type || ''
    };
    
    const res = await request('/healthsummary/index', params, 'get');
    tableData.value = res.data;
    pagination.total = res.total;
  } catch (error) {
    console.error('获取健康统计汇总列表失败:', error);
  }
};

// 搜索
const handleSearch = () => {
  pagination.current = 1;
  fetchHealthSummaryList();
};

// 重置搜索
const resetSearch = () => {
  searchForm.hs_date = '';
  searchForm.hs_type = '';
  pagination.current = 1;
  fetchHealthSummaryList();
};

// 分页大小改变
const handleSizeChange = (size) => {
  pagination.size = size;
  pagination.current = 1;
  fetchHealthSummaryList();
};

// 当前页改变
const handleCurrentChange = (page) => {
  pagination.current = page;
  fetchHealthSummaryList();
};

// 新增
const handleAdd = () => {
  dialogTitle.value = '新增健康统计汇总';
  isViewMode.value = false;
  Object.assign(healthSummaryForm, {
    id: undefined,
    hs_date: '',
    hs_type: '',
    hs_avgbmi: '',
    hs_avgsbp: '',
    hs_avgdbp: '',
    hs_avgchol: '',
    hs_highriskrate: '',
    hs_normalrate: '',
    hs_summarydata: ''
  });
  dialogVisible.value = true;
};

// 查看
const handleView = (row) => {
  dialogTitle.value = '查看健康统计汇总';
  isViewMode.value = true;
  Object.assign(healthSummaryForm, { ...row });
  dialogVisible.value = true;
};

// 编辑
const handleEdit = (row) => {
  dialogTitle.value = '编辑健康统计汇总';
  isViewMode.value = false;
  Object.assign(healthSummaryForm, { ...row });
  dialogVisible.value = true;
};

// 删除
const handleDelete = async (row) => {
  try {
    await ElMessageBox.confirm(`确定要删除这条健康统计汇总吗？`, '确认删除', {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning'
    });
    
    await request(`/healthsummary/destroy?id=${row.id}`, {}, 'delete');
    ElMessage.success('删除成功');
    fetchHealthSummaryList();
  } catch (error) {
    console.error('删除失败:', error);
  }
};

// 提交表单
const submitForm = async () => {
  try {
    if (!healthSummaryForm.hs_date) {
      ElMessage.error('请输入统计日期');
      return;
    }
    if (!healthSummaryForm.hs_type) {
      ElMessage.error('请输入统计类型');
      return;
    }
    if (!healthSummaryForm.hs_avgbmi) {
      ElMessage.error('请输入平均BMI');
      return;
    }
    if (!healthSummaryForm.hs_avgsbp) {
      ElMessage.error('请输入平均收缩压');
      return;
    }
    if (!healthSummaryForm.hs_avgdbp) {
      ElMessage.error('请输入平均舒张压');
      return;
    }
    if (!healthSummaryForm.hs_avgchol) {
      ElMessage.error('请输入平均总胆固醇');
      return;
    }
    if (!healthSummaryForm.hs_highriskrate) {
      ElMessage.error('请输入高风险比例');
      return;
    }
    if (!healthSummaryForm.hs_normalrate) {
      ElMessage.error('请输入正常指标比例');
      return;
    }

    if (healthSummaryForm.id == undefined) {
      // 新增
      await request('/healthsummary/store', healthSummaryForm, 'post');
      ElMessage.success('新增成功');
    } else {
      // 更新
      await request(`/healthsummary/update?id=${healthSummaryForm.id}`, healthSummaryForm, 'put');
      ElMessage.success('更新成功');
    }
    
    dialogVisible.value = false;
    fetchHealthSummaryList();
  } catch (error) {
    console.error('保存失败:', error);
  }
};

// 重置表单
const resetForm = () => {
  Object.assign(healthSummaryForm, {
    id: undefined,
    hs_date: '',
    hs_type: '',
    hs_avgbmi: '',
    hs_avgsbp: '',
    hs_avgdbp: '',
    hs_avgchol: '',
    hs_highriskrate: '',
    hs_normalrate: '',
    hs_summarydata: ''
  });
};
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
:deep(.health-summary-dialog .el-dialog__header) {
  padding: 24px 24px 0;
}

:deep(.health-summary-dialog .el-dialog__body) {
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