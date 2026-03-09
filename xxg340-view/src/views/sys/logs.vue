<template>
  <div class="log-container">
    <!-- 顶部操作栏 -->
    <div class="log-header">
      <div class="header-content">
        <h1 class="page-title">
          <el-icon class="title-icon"><Document /></el-icon>
          系统日志管理
        </h1>
        <p class="page-desc">查看和管理系统操作日志，监控系统运行状态</p>
      </div>
      <div class="header-actions">
        <el-button 
          @click="doClear" 
          type="danger"
          class="action-btn danger-btn"
        >
          <el-icon><Delete /></el-icon>
          清空日志
        </el-button>
      </div>
    </div>

    <!-- 主要内容区 -->
    <div class="log-content">
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
              <el-form-item label="日志标题">
                <el-input 
                  v-model="searchForm.logstitle" 
                  placeholder="请输入日志标题" 
                  clearable
                  suffix-icon="Document"
                />
              </el-form-item>
            </el-col>
            <el-col :xs="24" :sm="12" :md="8" :lg="6">
              <el-form-item label="日志级别">
                <el-select 
                  v-model="searchForm.loglevel" 
                  placeholder="请选择日志级别" 
                  clearable 
                  style="width: 100%"
                >
                  <el-option label="普通" value="info" />
                  <el-option label="错误" value="error" />
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
            <span class="table-title">日志记录列表</span>
            <div class="table-stats">
              <span class="stat-text">共 {{ pagination.total }} 条记录</span>
            </div>
          </div>
        </template>

        <el-table
          :data="tableData"
          v-loading="loading"
          style="width: 100%"
          class="log-table"
          :header-cell-style="{ background: '#f8f9fa', color: '#2c3e50' }"
        >
          <el-table-column prop="id" label="ID" width="80" align="center">
            <template #header>
              <span class="table-header-text">ID</span>
            </template>
          </el-table-column>
          
          <el-table-column prop="logstitle" label="日志标题" min-width="200">
            <template #header>
              <span class="table-header-text">日志标题</span>
            </template>
            <template #default="{ row }">
              <div class="title-cell">
                <el-icon class="title-icon"><Document /></el-icon>
                <span class="title-text">{{ row.logstitle }}</span>
              </div>
            </template>
          </el-table-column>
          
          <el-table-column prop="loglevel" label="日志级别" width="120" align="center">
            <template #header>
              <span class="table-header-text">日志级别</span>
            </template>
            <template #default="{ row }">
              <el-tag :type="getLevelType(row.loglevel)" effect="light" class="level-tag">
                {{ getLevelLabel(row.loglevel) }}
              </el-tag>
            </template>
          </el-table-column>
          
          <el-table-column prop="logip" label="客户端标识" width="150">
            <template #header>
              <span class="table-header-text">客户端标识</span>
            </template>
            <template #default="{ row }">
              <div class="ip-cell">
                <el-icon class="ip-icon"><Monitor /></el-icon>
                <span class="ip-text">{{ row.logip }}</span>
              </div>
            </template>
          </el-table-column>
          
          <el-table-column prop="cd" label="创建时间" min-width="180">
            <template #header>
              <span class="table-header-text">创建时间</span>
            </template>
            <template #default="{ row }">
              <div class="time-cell">
                <el-icon class="time-icon"><Clock /></el-icon>
                <span class="time-text">{{ row.cd }}</span>
              </div>
            </template>
          </el-table-column>
          
          <el-table-column prop="username" label="操作用户" min-width="150">
            <template #header>
              <span class="table-header-text">操作用户</span>
            </template>
            <template #default="{ row }">
              <div class="user-cell">
                <el-icon class="user-icon"><User /></el-icon>
                <span class="user-text">{{ row.username }}</span>
              </div>
            </template>
          </el-table-column>
          
          <el-table-column label="操作" width="180" align="center" fixed="right">
            <template #header>
              <span class="table-header-text">操作</span>
            </template>
            <template #default="{ row }">
              <div class="action-buttons">
                <el-button 
                  size="small" 
                  type="primary" 
                  @click="handleView(row)"
                  class="view-btn"
                >
                  <el-icon><View /></el-icon>
                  详情
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

    <!-- 日志详情对话框 -->
    <el-dialog
      v-model="detailDialogVisible"
      :title="`日志详情 - ${currentLog?.logstitle || ''}`"
      width="800px"
      class="log-detail-dialog"
    >
      <div v-if="currentLog" class="detail-content">
        <el-descriptions :column="2" border>
          <el-descriptions-item label="日志标题">
            <div class="detail-item">
              <el-icon><Document /></el-icon>
              <span>{{ currentLog.logstitle }}</span>
            </div>
          </el-descriptions-item>
          <el-descriptions-item label="日志级别">
            <el-tag :type="getLevelType(currentLog.loglevel)" effect="light">
              {{ getLevelLabel(currentLog.loglevel) }}
            </el-tag>
          </el-descriptions-item>
          <el-descriptions-item label="客户端标识">
            <div class="detail-item">
              <el-icon><Monitor /></el-icon>
              <span>{{ currentLog.logip }}</span>
            </div>
          </el-descriptions-item>
          <el-descriptions-item label="创建时间">
            <div class="detail-item">
              <el-icon><Clock /></el-icon>
              <span>{{ currentLog.cd }}</span>
            </div>
          </el-descriptions-item>
          <el-descriptions-item label="操作用户">
            <div class="detail-item">
              <el-icon><User /></el-icon>
              <span>{{ currentLog.username }}</span>
            </div>
          </el-descriptions-item>
          <el-descriptions-item label="日志内容" :span="2">
            <div class="log-content-panel">
              <div class="content-header">
                <el-icon><Document /></el-icon>
                <span>详细内容</span>
              </div>
              <div class="content-body">
                <pre>{{ formatLogContent(currentLog.logcontent) }}</pre>
              </div>
            </div>
          </el-descriptions-item>
        </el-descriptions>
      </div>
      
      <template #footer>
        <div class="dialog-footer">
          <el-button @click="detailDialogVisible = false" class="close-btn">关闭</el-button>
        </div>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { 
  ref, 
  reactive, 
  onMounted 
} from 'vue';
import { ElMessage, ElMessageBox } from 'element-plus';
import { 
  Document, 
  Delete, 
  Search, 
  RefreshRight, 
  View, 
  Monitor, 
  Clock, 
  User 
} from '@element-plus/icons-vue';
import { request } from '@/http/index';

// 表格数据
const tableData = ref([]);
const loading = ref(false);

// 分页配置
const pagination = reactive({
  current: 1,
  size: 10,
  total: 0
});

// 搜索表单
const searchForm = reactive({
  logstitle: '',
  loglevel: '',
  logip: ''
});

// 对话框控制
const detailDialogVisible = ref(false);

// 当前查看的日志
const currentLog = ref(null);

// 执行搜索
const handleSearch = async () => {
  await fetchData();
};

const handleDelete = async (row) => {
  try {
    await ElMessageBox.confirm(
      '确定要删除该系统日志吗？此操作不可恢复！',
      '警告',
      {
        confirmButtonText: '确定删除',
        cancelButtonText: '取消',
        type: 'warning',
        confirmButtonClass: 'el-button--danger'
      }
    );
    
    const res = await request('/syslog/destroy', {id: row.id}, 'delete');
    
    if (res) {
      ElMessage.success('删除成功');
      await fetchData();
    } else {
      ElMessage.error(res.msg || '删除失败');
    }
  } catch (error) {
    if (error !== 'cancel') {
      ElMessage.error('删除失败');
    }
  }
};

const doClear = async () => {
  try {
    await ElMessageBox.confirm(
      '确定要清空所有系统日志吗？此操作不可恢复！',
      '警告',
      {
        confirmButtonText: '确定清空',
        cancelButtonText: '取消',
        type: 'warning',
        confirmButtonClass: 'el-button--danger'
      }
    );
    
    const res = await request('/syslog/clear', {}, 'delete');
    
    if (res) {
      ElMessage.success('清空成功');
      await fetchData();
    } else {
      ElMessage.error(res.msg || '清空失败');
    }
  } catch (error) {
    if (error !== 'cancel') {
      ElMessage.error('清空失败');
    }
  }
};

// 重置搜索条件
const resetSearch = () => {
  Object.assign(searchForm, {
    logstitle: '',
    loglevel: '',
    logip: ''
  });
  pagination.current = 1;
  fetchData();
};

// 处理每页条数变化
const handleSizeChange = (val) => {
  pagination.size = val;
  pagination.current = 1;
  fetchData();
};

// 处理当前页码变化
const handleCurrentChange = (val) => {
  pagination.current = val;
  fetchData();
};

// 获取日志级别标签文本
const getLevelLabel = (level) => {
  const levelMap = {
    'info': '普通',
    'error': '错误',
    'warn': '警告',
    'debug': '调试'
  };
  return levelMap[level] || level;
};

// 获取日志级别 tag 类型
const getLevelType = (level) => {
  const typeMap = {
    'info': '',
    'error': 'danger',
    'warn': 'warning',
    'debug': 'info'
  };
  return typeMap[level] || '';
};

// 查看日志详情
const handleView = (row) => {
  currentLog.value = row;
  detailDialogVisible.value = true;
};

// 格式化日志内容
const formatLogContent = (content) => {
  if (!content) return '';
  
  try {
    const parsed = JSON.parse(content);
    return JSON.stringify(parsed, null, 2);
  } catch (e) {
    return content;
  }
};

// 加载数据
const fetchData = async () => {
  loading.value = true;

  try {
    const res = await request('/syslog/index', {
      limit: pagination.size,
      pg: pagination.current,
      logstitle: searchForm.logstitle,
      loglevel: searchForm.loglevel,
      logip: searchForm.logip
    }, 'get');

    tableData.value = res.data;
    pagination.total = res.total;
  } catch (error) {
    ElMessage.error('获取数据失败');
  } finally {
    loading.value = false;
  }
};

// 页面初始化加载数据
onMounted(() => {
  fetchData();
});
</script>

<style scoped lang="scss">
.log-container {
  padding: 24px;
  background: linear-gradient(135deg, #f5f7fa 0%, #e4efe9 100%);
  min-height: 100vh;
}

.log-header {
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
      
      &.danger-btn {
        background: linear-gradient(135deg, #f56c6c, #e64c4c);
        border: none;
        
        &:hover {
          background: linear-gradient(135deg, #e64c4c, #d63030);
        }
      }
    }
  }
}

.log-content {
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
    
    .log-table {
      :deep(.el-table__header) {
        .table-header-text {
          font-weight: 600;
          color: #2c3e50;
        }
      }
      
      :deep(.el-table__body) {
        .title-cell {
          display: flex;
          align-items: center;
          gap: 8px;
          
          .title-icon {
            color: #409eff;
          }
          
          .title-text {
            font-weight: 500;
          }
        }
        
        .level-tag {
          font-weight: 500;
        }
        
        .ip-cell,
        .time-cell,
        .user-cell {
          display: flex;
          align-items: center;
          gap: 8px;
          
          .ip-icon,
          .time-icon,
          .user-icon {
            color: #909399;
            font-size: 14px;
          }
          
          .ip-text,
          .time-text,
          .user-text {
            font-size: 13px;
          }
        }
        
        .action-buttons {
          display: flex;
          gap: 8px;
          justify-content: center;
          
          .view-btn,
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
.log-detail-dialog {
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
  
  .detail-content {
    .detail-item {
      display: flex;
      align-items: center;
      gap: 8px;
    }
    
    .log-content-panel {
      border: 1px solid #e4e7ed;
      border-radius: 8px;
      overflow: hidden;
      
      .content-header {
        padding: 12px 16px;
        background: #f8f9fa;
        border-bottom: 1px solid #e4e7ed;
        display: flex;
        align-items: center;
        gap: 8px;
        font-weight: 600;
        color: #2c3e50;
      }
      
      .content-body {
        padding: 16px;
        background: #fafbfc;
        max-height: 300px;
        overflow-y: auto;
        
        pre {
          margin: 0;
          white-space: pre-wrap;
          word-break: break-word;
          font-family: 'Monaco', 'Menlo', 'Ubuntu Mono', monospace;
          font-size: 12px;
          line-height: 1.5;
          color: #606266;
        }
      }
    }
  }
  
  .dialog-footer {
    display: flex;
    justify-content: flex-end;
    
    .close-btn {
      border-radius: 8px;
      padding: 10px 20px;
    }
  }
}

// 响应式设计
@media (max-width: 768px) {
  .log-container {
    padding: 16px;
  }
  
  .log-header {
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