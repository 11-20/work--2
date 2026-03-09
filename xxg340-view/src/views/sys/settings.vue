<template>
  <div class="config-container">
    <!-- 顶部操作栏 -->
    <div class="config-header">
      <div class="header-content">
        <h1 class="page-title">
          <el-icon class="title-icon"><Setting /></el-icon>
          系统参数配置
        </h1>
        <p class="page-desc">管理系统运行参数，配置键值对信息</p>
      </div>
      <div class="header-actions">
        <el-button 
          @click="handleRefreshCache" 
          :loading="cacheLoading"
          class="action-btn secondary-btn"
        >
          <el-icon><Refresh /></el-icon>
          刷新缓存
        </el-button>
        <el-button 
          type="primary" 
          @click="handleAdd"
          class="action-btn primary-btn"
        >
          <el-icon><Plus /></el-icon>
          新增参数
        </el-button>
      </div>
    </div>

    <!-- 主要内容区 -->
    <div class="config-content">
      <!-- 筛选卡片 -->
      <el-card class="search-card" shadow="never">
        <template #header>
          <div class="search-header">
            <el-icon><Search /></el-icon>
            <span>筛选条件</span>
          </div>
        </template>
        
        <el-form :model="searchForm" label-width="100px">
          <el-row :gutter="20">
            <el-col :xs="24" :sm="12" :md="8" :lg="6">
              <el-form-item label="配置键名">
                <el-input 
                  v-model="searchForm.confkey" 
                  placeholder="请输入配置键名" 
                  clearable
                  suffix-icon="Search"
                />
              </el-form-item>
            </el-col>
            <el-col :xs="24" :sm="12" :md="8" :lg="6">
              <el-form-item label="配置名称">
                <el-input 
                  v-model="searchForm.confname" 
                  placeholder="请输入配置名称" 
                  clearable
                  suffix-icon="Document"
                />
              </el-form-item>
            </el-col>
            <el-col :xs="24" :sm="12" :md="8" :lg="6">
              <el-form-item label="配置类型">
                <el-select 
                  v-model="searchForm.conftype" 
                  placeholder="请选择配置类型" 
                  clearable 
                  style="width: 100%"
                >
                  <el-option label="字符串" value="string" />
                  <el-option label="数字" value="number" />
                  <el-option label="布尔值" value="boolean" />
                  <el-option label="JSON数据" value="json" />
                </el-select>
              </el-form-item>
            </el-col>
            <el-col :xs="24" :sm="12" :md="8" :lg="6" class="search-buttons">
              <el-button type="primary" @click="handleSearch" class="search-btn">
                <el-icon><Search /></el-icon>
                查询
              </el-button>
              <el-button @click="resetSearch" class="reset-btn">
                <el-icon><RefreshRight /></el-icon>
                重置
              </el-button>
            </el-col>
          </el-row>
        </el-form>
      </el-card>

      <!-- 数据表格区域 -->
      <el-card class="table-card" shadow="never">
        <template #header>
          <div class="table-header">
            <span class="table-title">参数配置列表</span>
            <div class="table-stats">
              <span class="stat-text">共 {{ pagination.total }} 项配置</span>
            </div>
          </div>
        </template>

        <el-table
          :data="tableData"
          v-loading="loading"
          style="width: 100%"
          class="config-table"
          :header-cell-style="{ background: '#f8f9fa', color: '#2c3e50' }"
        >
          <el-table-column prop="id" label="ID" width="80" align="center">
            <template #header>
              <span class="table-header-text">ID</span>
            </template>
          </el-table-column>
          
          <el-table-column prop="confkey" label="配置键名" min-width="150">
            <template #header>
              <span class="table-header-text">配置键名</span>
            </template>
            <template #default="{ row }">
              <div class="key-cell">
                <el-icon class="key-icon"><Key /></el-icon>
                <span class="key-text">{{ row.confkey }}</span>
              </div>
            </template>
          </el-table-column>
          
          <el-table-column prop="confname" label="配置名称" min-width="150">
            <template #header>
              <span class="table-header-text">配置名称</span>
            </template>
          </el-table-column>
          
          <el-table-column prop="confvalue" label="配置值" min-width="200" show-overflow-tooltip>
            <template #header>
              <span class="table-header-text">配置值</span>
            </template>
            <template #default="{ row }">
              <div class="value-cell">
                <span v-if="row.conftype === 'boolean'" class="boolean-value">
                  <el-tag :type="row.confvalue === 'true' ? 'success' : 'info'" effect="plain" size="small">
                    {{ row.confvalue === 'true' ? '是' : '否' }}
                  </el-tag>
                </span>
                <span v-else-if="row.conftype === 'json'" class="json-value">
                  {{ formatJsonValue(row.confvalue) }}
                </span>
                <span v-else class="text-value">{{ row.confvalue }}</span>
              </div>
            </template>
          </el-table-column>
          
          <el-table-column prop="conftype" label="配置类型" width="120" align="center">
            <template #header>
              <span class="table-header-text">配置类型</span>
            </template>
            <template #default="{ row }">
              <el-tag :type="getTypeTagType(row.conftype)" effect="light" class="type-tag">
                {{ getTypeText(row.conftype) }}
              </el-tag>
            </template>
          </el-table-column>
          
          <el-table-column prop="confdesc" label="配置描述" min-width="200" show-overflow-tooltip>
            <template #header>
              <span class="table-header-text">配置描述</span>
            </template>
            <template #default="{ row }">
              <span class="desc-text">{{ row.confdesc || '无描述' }}</span>
            </template>
          </el-table-column>
          
          <el-table-column label="操作" width="220" align="center" fixed="right">
            <template #header>
              <span class="table-header-text">操作</span>
            </template>
            <template #default="{ row }">
              <div class="action-buttons">
                <el-button 
                  size="small" 
                  @click="handleView(row)"
                  class="view-btn"
                >
                  <el-icon><View /></el-icon>
                  查看
                </el-button>
                <el-button 
                  size="small" 
                  type="primary" 
                  @click="handleEdit(row)"
                  class="edit-btn"
                >
                  <el-icon><Edit /></el-icon>
                  编辑
                </el-button>
                <el-button 
                  size="small" 
                  type="danger" 
                  @click="handleDelete(row)"
                  class="delete-btn"
                >
                  <el-icon><Delete /></el-icon>
                  删除
                </el-button>
              </div>
            </template>
          </el-table-column>
        </el-table>

        <!-- 分页 -->
        <div class="pagination-container">
          <el-pagination
            v-model:current-page="pagination.current"
            v-model:page-size="pagination.size"
            :total="pagination.total"
            :page-sizes="[10, 20, 50, 100]"
            layout="total, sizes, prev, pager, next, jumper"
            background
            @size-change="handleSizeChange"
            @current-change="handleCurrentChange"
          />
        </div>
      </el-card>
    </div>

    <!-- 参数查看/编辑/新增 Dialog -->
    <el-dialog
      :title="dialogTitle"
      v-model="dialogVisible"
      width="600px"
      class="config-dialog"
      @close="handleDialogClose"
    >
      <div class="dialog-content">
        <el-form
          ref="paramFormRef"
          :model="paramForm"
          :rules="paramFormRules"
          label-width="100px"
          class="param-form"
        >
          <el-form-item label="配置键名" prop="confkey">
            <el-input 
              v-model="paramForm.confkey" 
              placeholder="请输入配置键名，如：system_name"
              :disabled="!isAddMode"
              suffix-icon="Key"
            />
            <div class="form-tip" v-if="isAddMode">
              键名只能包含字母、数字和下划线，且不能以数字开头
            </div>
          </el-form-item>
          
          <el-form-item label="配置名称" prop="confname">
            <el-input 
              v-model="paramForm.confname" 
              placeholder="请输入配置名称"
              suffix-icon="Document"
            />
          </el-form-item>
          
          <el-form-item label="配置类型" prop="conftype">
            <el-select 
              v-model="paramForm.conftype" 
              placeholder="请选择配置类型" 
              style="width: 100%"
              @change="handleTypeChange"
            >
              <el-option label="字符串" value="string" />
              <el-option label="数字" value="number" />
              <el-option label="布尔值" value="boolean" />
              <el-option label="JSON数据" value="json" />
            </el-select>
          </el-form-item>
          
          <el-form-item label="配置值" prop="confvalue">
            <el-input 
              v-if="paramForm.conftype === 'string' || paramForm.conftype === 'number'"
              v-model="paramForm.confvalue" 
              :placeholder="getValuePlaceholder()"
              :type="paramForm.conftype === 'number' ? 'number' : 'text'"
            />
            <el-select 
              v-else-if="paramForm.conftype === 'boolean'"
              v-model="paramForm.confvalue" 
              placeholder="请选择"
              style="width: 100%"
            >
              <el-option label="是" value="true" />
              <el-option label="否" value="false" />
            </el-select>
            <el-input
              v-else-if="paramForm.conftype === 'json'"
              v-model="paramForm.confvalue"
              type="textarea"
              :rows="4"
              placeholder='请输入JSON格式数据，如：{"key": "value"}'
              class="json-textarea"
            />
          </el-form-item>
          
          <el-form-item label="配置描述" prop="confdesc">
            <el-input 
              v-model="paramForm.confdesc" 
              type="textarea" 
              :rows="3" 
              placeholder="请输入配置描述信息"
              maxlength="200"
              show-word-limit
            />
          </el-form-item>
        </el-form>
      </div>
      
      <template #footer>
        <div class="dialog-footer">
          <el-button @click="dialogVisible = false" class="cancel-btn">取消</el-button>
          <el-button 
            type="primary" 
            @click="submitParamForm" 
            class="confirm-btn"
            :loading="loading"
          >
            <el-icon><Check /></el-icon>
            {{ isAddMode ? '新增' : '更新' }}
          </el-button>
        </div>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted, computed, nextTick } from 'vue';
import { ElMessage, ElMessageBox } from 'element-plus'
import { 
  Setting, 
  Refresh, 
  Plus, 
  Search, 
  Document, 
  RefreshRight, 
  Key, 
  View, 
  Edit, 
  Delete, 
  Check 
} from '@element-plus/icons-vue'
import { request } from '@/http/index';

// 表格数据
const tableData = ref([]);
const loading = ref(false);
const cacheLoading = ref(false);

// 分页配置
const pagination = reactive({
  current: 1,
  size: 10,
  total: 0
});

// 搜索表单
const searchForm = reactive({
  confkey: '',
  confname: '',
  conftype: ''
});

// 参数表单引用
const paramFormRef = ref(null);

// 参数表单数据
const paramForm = reactive({
  id: '',
  confkey: '',
  confname: '',
  confvalue: '',
  conftype: 'string',
  confdesc: ''
});

// 表单验证规则
const paramFormRules = {
  confkey: [
    { required: true, message: '请输入配置键名', trigger: 'blur' },
    { pattern: /^[a-zA-Z_][a-zA-Z0-9_]*$/, message: '键名只能包含字母、数字和下划线，且不能以数字开头', trigger: 'blur' }
  ],
  confname: [
    { required: true, message: '请输入配置名称', trigger: 'blur' }
  ],
  conftype: [
    { required: true, message: '请选择配置类型', trigger: 'change' }
  ],
  confvalue: [
    { required: true, message: '请输入配置值', trigger: 'blur' },
    { validator: validateValue, trigger: 'blur' }
  ]
};

// 自定义验证规则
function validateValue(rule, value, callback) {
  if (!value) {
    callback(new Error('配置值不能为空'));
    return;
  }

  const type = paramForm.conftype;
  
  if (type === 'number') {
    if (isNaN(value)) {
      callback(new Error('请输入有效的数字'));
    } else {
      callback();
    }
  } else if (type === 'boolean') {
    if (value !== 'true' && value !== 'false') {
      callback(new Error('请选择是或否'));
    } else {
      callback();
    }
  } else if (type === 'json') {
    try {
      JSON.parse(value);
      callback();
    } catch (e) {
      callback(new Error('请输入有效的JSON格式'));
    }
  } else {
    callback();
  }
}

// 对话框相关
const dialogVisible = ref(false);
const dialogTitle = ref('');
const isAddMode = ref(true);

// 获取参数列表
const getParamList = async () => {
  loading.value = true;
  try {
    const res = await request('/sysarg/index', {
      pg: pagination.current,
      limit: pagination.size,
      ...searchForm
    }, 'get');
    
    tableData.value = res.data;
    pagination.total = res.total;
  } catch (error) {
    ElMessage.error('获取参数列表失败');
  } finally {
    loading.value = false;
  }
};

// 处理搜索
const handleSearch = () => {
  pagination.current = 1;
  getParamList();
};

// 重置搜索
const resetSearch = () => {
  searchForm.confkey = '';
  searchForm.confname = '';
  searchForm.conftype = '';
  pagination.current = 1;
  getParamList();
};

// 处理分页大小变化
const handleSizeChange = (val) => {
  pagination.size = val;
  pagination.current = 1;
  getParamList();
};

// 处理当前页变化
const handleCurrentChange = (val) => {
  pagination.current = val;
  getParamList();
};

// 处理添加参数
const handleAdd = () => {
  isAddMode.value = true;
  dialogTitle.value = '新增参数';
  resetParamForm();
  dialogVisible.value = true;
};

// 处理编辑参数
const handleEdit = (row) => {
  isAddMode.value = false;
  dialogTitle.value = '编辑参数';
  Object.assign(paramForm, row);
  dialogVisible.value = true;
};

// 处理查看参数
const handleView = (row) => {
  isAddMode.value = false;
  dialogTitle.value = '查看参数';
  Object.assign(paramForm, row);
  dialogVisible.value = true;
};

// 处理删除参数
const handleDelete = (row) => {
  ElMessageBox.confirm('确定要删除该参数吗？', '提示', {
    confirmButtonText: '确定',
    cancelButtonText: '取消',
    type: 'warning'
  }).then(async () => {
    try {
      await request('/sysarg/destory', { id: row.id }, 'delete');
      ElMessage.success('删除成功');
      getParamList();
    } catch (error) {
      ElMessage.error('删除失败');
    }
  }).catch(() => {
    // 取消删除
  });
};

// 处理刷新缓存
const handleRefreshCache = async () => {
  cacheLoading.value = true;
  try {
    await request('/sysarg/refreshCache', {}, 'post');
    ElMessage.success('缓存刷新成功');
  } catch (error) {
    ElMessage.error('缓存刷新失败');
  } finally {
    cacheLoading.value = false;
  }
};

// 重置参数表单
const resetParamForm = () => {
  Object.assign(paramForm, {
    id: '',
    confkey: '',
    confname: '',
    confvalue: '',
    conftype: 'string',
    confdesc: ''
  });
};

// 处理对话框关闭
const handleDialogClose = () => {
  paramFormRef.value?.resetFields();
  resetParamForm();
};

// 处理类型变化
const handleTypeChange = (type) => {
  // 根据类型重置值
  if (type === 'boolean') {
    paramForm.confvalue = 'true';
  } else if (type === 'number') {
    paramForm.confvalue = '0';
  } else {
    paramForm.confvalue = '';
  }
};

// 提交参数表单
const submitParamForm = () => {
  paramFormRef.value?.validate(async (valid) => {
    if (!valid) return;
    
    try {
      if (isAddMode.value) {
        // 新增参数
        await request('/sysarg/store', paramForm, 'post');
        ElMessage.success('新增成功');
      } else {
        // 编辑参数
        await request('/sysarg/update', paramForm, 'put');
        ElMessage.success('更新成功');
      }
      
      dialogVisible.value = false;
      getParamList();
    } catch (error) {
      ElMessage.error(isAddMode.value ? '新增失败' : '更新失败');
    }
  });
};

// 获取类型标签样式
const getTypeTagType = (type) => {
  const typeMap = {
    string: '',
    number: 'success',
    boolean: 'warning',
    json: 'danger'
  };
  return typeMap[type] || '';
};

// 获取类型显示文本
const getTypeText = (type) => {
  const typeMap = {
    string: '字符串',
    number: '数字',
    boolean: '布尔值',
    json: 'JSON'
  };
  return typeMap[type] || type;
};

// 格式化JSON值显示
const formatJsonValue = (value) => {
  try {
    const obj = JSON.parse(value);
    return JSON.stringify(obj, null, 2);
  } catch (e) {
    return value;
  }
};

// 获取值输入框的placeholder
const getValuePlaceholder = () => {
  const type = paramForm.conftype;
  if (type === 'number') {
    return '请输入数字';
  }
  return '请输入配置值';
};

// 组件挂载时获取数据
onMounted(() => {
  getParamList();
});
</script>

<style scoped lang="scss">
.config-container {
  padding: 24px;
  background: linear-gradient(135deg, #f5f7fa 0%, #e4efe9 100%);
  min-height: 100vh;
}

.config-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 24px;
  
  .header-content {
    .page-title {
      display: flex;
      align-items: center;
      font-size: 28px;
      font-weight: 600;
      color: #2c3e50;
      margin: 0 0 8px 0;
      
      .title-icon {
        margin-right: 12px;
        color: #409eff;
      }
    }
    
    .page-desc {
      font-size: 14px;
      color: #7f8c8d;
      margin: 0;
    }
  }
  
  .header-actions {
    display: flex;
    gap: 12px;
    
    .action-btn {
      border-radius: 8px;
      padding: 10px 20px;
      font-weight: 500;
      
      &.primary-btn {
        background: linear-gradient(135deg, #409eff, #337ecc);
        border: none;
        
        &:hover {
          background: linear-gradient(135deg, #337ecc, #2667b3);
        }
      }
      
      &.secondary-btn {
        border-color: #dcdfe6;
        
        &:hover {
          border-color: #409eff;
          color: #409eff;
        }
      }
    }
  }
}

.config-content {
  .search-card {
    border-radius: 12px;
    border: 1px solid #e4e7ed;
    margin-bottom: 24px;
    
    :deep(.el-card__header) {
      padding: 16px 20px;
      border-bottom: 1px solid #f0f0f0;
      background: #fafbfc;
    }
    
    .search-header {
      display: flex;
      align-items: center;
      gap: 8px;
      font-weight: 600;
      color: #2c3e50;
    }
    
    .search-buttons {
      display: flex;
      align-items: flex-end;
      gap: 12px;
      
      .search-btn,
      .reset-btn {
        border-radius: 6px;
        padding: 10px 20px;
      }
    }
  }
  
  .table-card {
    border-radius: 12px;
    border: 1px solid #e4e7ed;
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
    
    :deep(.el-card__header) {
      padding: 20px 24px;
      border-bottom: 1px solid #f0f0f0;
      background: #fafbfc;
    }
    
    .table-header {
      display: flex;
      justify-content: space-between;
      align-items: center;
      
      .table-title {
        font-size: 18px;
        font-weight: 600;
        color: #2c3e50;
      }
      
      .table-stats {
        .stat-text {
          font-size: 14px;
          color: #7f8c8d;
        }
      }
    }
    
    .config-table {
      :deep(.el-table__header) {
        .table-header-text {
          font-weight: 600;
          color: #2c3e50;
        }
      }
      
      :deep(.el-table__body) {
        .key-cell {
          display: flex;
          align-items: center;
          gap: 8px;
          
          .key-icon {
            color: #409eff;
          }
          
          .key-text {
            font-family: 'Monaco', 'Menlo', 'Ubuntu Mono', monospace;
            font-size: 13px;
            color: #409eff;
          }
        }
        
        .value-cell {
          .boolean-value,
          .json-value,
          .text-value {
            font-size: 13px;
          }
          
          .json-value {
            font-family: 'Monaco', 'Menlo', 'Ubuntu Mono', monospace;
            color: #606266;
          }
        }
        
        .type-tag {
          font-weight: 500;
        }
        
        .desc-text {
          color: #7f8c8d;
          font-size: 13px;
        }
        
        .action-buttons {
          display: flex;
          gap: 8px;
          justify-content: center;
          
          .view-btn,
          .edit-btn,
          .delete-btn {
            border-radius: 6px;
            padding: 6px 12px;
          }
        }
      }
    }
    
    .pagination-container {
      display: flex;
      justify-content: center;
      padding: 20px 0 0 0;
    }
  }
}

// 对话框样式
.config-dialog {
  :deep(.el-dialog) {
    border-radius: 12px;
    
    .el-dialog__header {
      padding: 20px 24px;
      border-bottom: 1px solid #f0f0f0;
      margin: 0;
      
      .el-dialog__title {
        font-weight: 600;
        color: #2c3e50;
      }
    }
    
    .el-dialog__body {
      padding: 24px;
    }
  }
  
  .dialog-content {
    .param-form {
      .form-tip {
        font-size: 12px;
        color: #909399;
        margin-top: 4px;
      }
      
      .json-textarea {
        :deep(.el-textarea__inner) {
          font-family: 'Monaco', 'Menlo', 'Ubuntu Mono', monospace;
          font-size: 13px;
        }
      }
    }
  }
  
  .dialog-footer {
    display: flex;
    justify-content: flex-end;
    gap: 12px;
    
    .cancel-btn,
    .confirm-btn {
      border-radius: 8px;
      padding: 10px 20px;
    }
  }
}

// 响应式设计
@media (max-width: 768px) {
  .config-container {
    padding: 16px;
  }
  
  .config-header {
    flex-direction: column;
    gap: 16px;
    
    .header-actions {
      width: 100%;
      
      .action-btn {
        flex: 1;
      }
    }
  }
  
  .search-buttons {
    justify-content: flex-start !important;
    margin-top: 16px;
  }
  
  .table-header {
    flex-direction: column;
    gap: 12px;
    align-items: flex-start !important;
  }
  
  .action-buttons {
    flex-direction: column;
    gap: 4px !important;
  }
}
</style>