<template>
  <div class="backup-container">
    <!-- 顶部操作栏 -->
    <div class="backup-header">
      <div class="header-content">
        <h1 class="page-title">
          <el-icon class="title-icon"><Download /></el-icon>
          数据备份管理
        </h1>
        <p class="page-desc">管理系统数据备份，确保数据安全</p>
      </div>
      <div class="header-actions">
        <el-button 
          type="primary" 
          @click="handleBackup" 
          :loading="backupLoading"
          class="action-btn primary-btn"
        >
          <el-icon><Download /></el-icon>
          备份当前数据
        </el-button>
        <el-button 
          @click="handleRefresh" 
          :loading="loading"
          class="action-btn secondary-btn"
        >
          <el-icon><Refresh /></el-icon>
          刷新列表
        </el-button>
      </div>
    </div>

    <!-- 主要内容区 -->
    <div class="backup-content">
      <!-- 数据卡片区域 -->
      <div class="data-cards">
        <el-card class="backup-card" shadow="hover">
          <div class="card-content">
            <div class="card-icon primary">
              <el-icon><Files /></el-icon>
            </div>
            <div class="card-info">
              <div class="card-value">{{ pagination.total }}</div>
              <div class="card-label">总备份数量</div>
            </div>
          </div>
        </el-card>
        
        <el-card class="backup-card" shadow="hover">
          <div class="card-content">
            <div class="card-icon success">
              <el-icon><Timer /></el-icon>
            </div>
            <div class="card-info">
              <div class="card-value">{{ latestBackupTime }}</div>
              <div class="card-label">最近备份</div>
            </div>
          </div>
        </el-card>
      </div>

      <!-- 表格区域 -->
      <el-card class="table-card" shadow="never">
        <template #header>
          <div class="table-header">
            <span class="table-title">备份记录列表</span>
            <div class="table-actions">
              <el-input
                v-model="searchKeyword"
                placeholder="搜索备份记录..."
                clearable
                style="width: 200px; margin-right: 12px;"
                @clear="handleSearch"
                @keyup.enter="handleSearch"
              >
                <template #prefix>
                  <el-icon><Search /></el-icon>
                </template>
              </el-input>
            </div>
          </div>
        </template>

        <el-table
          :data="tableData"
          v-loading="loading"
          style="width: 100%"
          class="backup-table"
        >
          <el-table-column prop="id" label="ID" width="80" align="center">
            <template #header>
              <span class="table-header-text">ID</span>
            </template>
          </el-table-column>
          
          <el-table-column prop="cd" label="备份时间" width="180">
            <template #header>
              <span class="table-header-text">备份时间</span>
            </template>
            <template #default="{ row }">
              <div class="time-cell">
                <el-icon class="time-icon"><Clock /></el-icon>
                <span>{{ formatTime(row.cd) }}</span>
              </div>
            </template>
          </el-table-column>
          
          <el-table-column prop="backdata" label="备份数据摘要" min-width="200">
            <template #header>
              <span class="table-header-text">备份数据摘要</span>
            </template>
            <template #default="{ row }">
              <div class="data-preview">
                <el-tooltip
                  :content="getDataPreview(row.backdata)"
                  placement="top"
                  effect="light"
                >
                  <span>{{ getDataPreview(row.backdata) }}</span>
                </el-tooltip>
              </div>
            </template>
          </el-table-column>
          
          <el-table-column prop="data_size" label="数据大小" width="120" align="center">
            <template #header>
              <span class="table-header-text">数据大小</span>
            </template>
            <template #default="{ row }">
              <el-tag :type="getSizeTagType(row.backdata)" effect="plain">
                {{ calculateDataSize(row.backdata) }}
              </el-tag>
            </template>
          </el-table-column>
          
          <el-table-column label="操作" width="200" align="center" fixed="right">
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
                  type="success" 
                  @click="handleRestore(row)"
                  class="restore-btn"
                >
                  <el-icon><RefreshLeft /></el-icon>
                  恢复
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
            :page-sizes="[5, 10, 20, 50]"
            layout="total, sizes, prev, pager, next, jumper"
            background
            @size-change="handleSizeChange"
            @current-change="handleCurrentChange"
          />
        </div>
      </el-card>
    </div>

    <!-- 备份数据查看 Dialog -->
    <el-dialog
      title="备份数据详情"
      v-model="viewDialogVisible"
      width="900px"
      class="data-dialog"
    >
      <div class="dialog-content">
        <div class="dialog-header">
          <el-icon class="dialog-icon"><Document /></el-icon>
          <span>备份数据内容</span>
        </div>
        <div class="data-viewer">
          <el-input
            v-model="viewData"
            type="textarea"
            :rows="18"
            readonly
            placeholder="暂无数据"
            class="data-textarea"
          />
        </div>
      </div>
      <template #footer>
        <div class="dialog-footer">
          <el-button @click="viewDialogVisible = false" class="cancel-btn">关闭</el-button>
          <el-button type="primary" @click="handleCopyData" class="copy-btn">
            <el-icon><DocumentCopy /></el-icon>
            复制数据
          </el-button>
        </div>
      </template>
    </el-dialog>

    <!-- 备份确认 Dialog -->
    <el-dialog
      title="数据备份确认"
      v-model="backupDialogVisible"
      width="500px"
      class="confirm-dialog"
    >
      <div class="confirm-content">
        <div class="confirm-icon">
          <el-icon><Warning /></el-icon>
        </div>
        <div class="confirm-text">
          <h3>即将执行数据备份操作</h3>
          <p>此操作会将当前系统的所有关键数据备份到数据库中，建议在系统空闲时执行。</p>
        </div>
        <div class="confirm-info">
          <div class="info-item">
            <el-icon><Clock /></el-icon>
            <span>备份时间：</span>
            <strong>{{ currentTime }}</strong>
          </div>
          <div class="info-item">
            <el-icon><User /></el-icon>
            <span>操作人：</span>
            <strong>{{ userInfo?.user_name || '当前用户' }}</strong>
          </div>
        </div>
      </div>
      <template #footer>
        <div class="dialog-footer">
          <el-button @click="backupDialogVisible = false" class="cancel-btn">取消</el-button>
          <el-button 
            type="primary" 
            @click="confirmBackup" 
            :loading="backupLoading"
            class="confirm-btn"
          >
            <el-icon><Check /></el-icon>
            开始备份
          </el-button>
        </div>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted, computed } from 'vue';
import { ElMessage, ElMessageBox } from 'element-plus'
import { 
  Download, 
  Refresh, 
  Files, 
  Timer, 
  Search, 
  Clock, 
  View, 
  RefreshLeft, 
  Delete, 
  Document, 
  DocumentCopy, 
  Warning, 
  User,
  Check 
} from '@element-plus/icons-vue'
import { request } from '@/http/index';
import { GlobalStore } from '@/stores';
const globalStore = GlobalStore();

const userInfo = globalStore.userInfo;

// 表格数据
const tableData = ref([]);
const loading = ref(false);
const backupLoading = ref(false);
const searchKeyword = ref('');

// 分页配置
const pagination = reactive({
  current: 1,
  size: 10,
  total: 0
});

// 对话框相关
const viewDialogVisible = ref(false);
const backupDialogVisible = ref(false);
const viewData = ref('');

// 计算属性
const currentTime = computed(() => {
  return new Date().toLocaleString('zh-CN');
});

const latestBackupTime = computed(() => {
  if (tableData.value.length === 0) return '暂无备份';
  return formatTime(tableData.value[0].cd);
});

// 获取备份列表
const getBackupList = async () => {
  loading.value = true;
  try {
    const params = {
      pg: pagination.current,
      limit: pagination.size
    };
    
    if (searchKeyword.value) {
      params.keyword = searchKeyword.value;
    }
    
    const res = await request('/backup/index', params, 'get');
    
    tableData.value = res.data;
    pagination.total = res.total;
  } catch (error) {
    ElMessage.error('获取备份列表失败');
  } finally {
    loading.value = false;
  }
};

// 处理备份数据
const handleBackup = () => {
  backupDialogVisible.value = true;
};

// 确认备份
const confirmBackup = async () => {
  backupLoading.value = true;
  try {
    await request('/basic/backup', {}, 'post');
    ElMessage.success('数据备份成功');
    backupDialogVisible.value = false;
    getBackupList();
  } catch (error) {
    ElMessage.error('数据备份失败');
  } finally {
    backupLoading.value = false;
  }
};

// 处理恢复
const handleRestore = (row) => {
  ElMessageBox.confirm(
    `确定要使用此备份数据恢复系统吗？<br><br>
    <strong style="color: #e6a23c;">警告：</strong>此操作将覆盖当前系统的所有数据，且不可逆转！`,
    '数据恢复确认',
    {
      confirmButtonText: '确认恢复',
      cancelButtonText: '取消',
      type: 'warning',
      dangerouslyUseHTMLString: true,
      customClass: 'restore-confirm-dialog'
    }
  ).then(async () => {
    try {
      await request('/basic/restore?id='+row.id);
      ElMessage.success('数据恢复成功');
      getBackupList();
    } catch (error) {
      ElMessage.error('数据恢复失败');
    }
  }).catch(() => {
    // 取消恢复
  });
};

// 处理查看
const handleView = (row) => {
  viewData.value = formatJsonData(row.backdata);
  viewDialogVisible.value = true;
};

// 处理删除
const handleDelete = (row) => {
  ElMessageBox.confirm('确定要删除此备份数据吗？', '提示', {
    confirmButtonText: '确定',
    cancelButtonText: '取消',
    type: 'warning',
    customClass: 'delete-confirm-dialog'
  }).then(async () => {
    try {
      await request('/backup/destroy', { id: row.id }, 'delete');
      ElMessage.success('删除成功');
      getBackupList();
    } catch (error) {
      ElMessage.error('删除失败');
    }
  }).catch(() => {
    // 取消删除
  });
};

// 处理刷新
const handleRefresh = () => {
  searchKeyword.value = '';
  getBackupList();
};

// 处理搜索
const handleSearch = () => {
  pagination.current = 1;
  getBackupList();
};

// 处理分页大小变化
const handleSizeChange = (val) => {
  pagination.size = val;
  pagination.current = 1;
  getBackupList();
};

// 处理当前页变化
const handleCurrentChange = (val) => {
  pagination.current = val;
  getBackupList();
};

// 格式化时间
const formatTime = (time) => {
  if (!time) return '';
  return new Date(time).toLocaleString('zh-CN');
};

// 获取数据预览
const getDataPreview = (data) => {
  if (!data) return '无数据';
  
  try {
    const parsed = JSON.parse(data);
    if (typeof parsed === 'object') {
      const keys = Object.keys(parsed);
      return `包含 ${keys.length} 个数据表: ${keys.join(', ')}`;
    }
    return String(data).substring(0, 100) + '...';
  } catch (e) {
    return String(data).substring(0, 100) + '...';
  }
};

// 计算数据大小
const calculateDataSize = (data) => {
  if (!data) return '0 B';
  
  const bytes = new Blob([data]).size;
  if (bytes < 1024) return bytes + ' B';
  if (bytes < 1024 * 1024) return (bytes / 1024).toFixed(2) + ' KB';
  return (bytes / (1024 * 1024)).toFixed(2) + ' MB';
};

// 获取大小标签类型
const getSizeTagType = (data) => {
  if (!data) return 'info';
  
  const bytes = new Blob([data]).size;
  if (bytes < 1024 * 1024) return 'success'; // 小于1MB
  if (bytes < 5 * 1024 * 1024) return 'warning'; // 1MB-5MB
  return 'danger'; // 大于5MB
};

// 格式化JSON数据
const formatJsonData = (data) => {
  if (!data) return '';
  
  try {
    const parsed = JSON.parse(data);
    return JSON.stringify(parsed, null, 2);
  } catch (e) {
    return data;
  }
};

// 复制数据
const handleCopyData = async () => {
  try {
    await navigator.clipboard.writeText(viewData.value);
    ElMessage.success('数据已复制到剪贴板');
  } catch (err) {
    ElMessage.error('复制失败');
  }
};

// 组件挂载时获取数据
onMounted(() => {
  getBackupList();
});
</script>

<style scoped lang="scss">
.backup-container {
  padding: 24px;
  background: linear-gradient(135deg, #f5f7fa 0%, #e4efe9 100%);
  min-height: 100vh;
}

.backup-header {
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

.backup-content {
  .data-cards {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
    gap: 16px;
    margin-bottom: 24px;
    
    .backup-card {
      border-radius: 12px;
      border: none;
      transition: all 0.3s ease;
      
      &:hover {
        transform: translateY(-4px);
        box-shadow: 0 8px 25px rgba(0, 0, 0, 0.1);
      }
      
      .card-content {
        display: flex;
        align-items: center;
        padding: 8px;
        
        .card-icon {
          width: 60px;
          height: 60px;
          border-radius: 12px;
          display: flex;
          align-items: center;
          justify-content: center;
          margin-right: 16px;
          font-size: 24px;
          
          &.primary {
            background: linear-gradient(135deg, #409eff, #79bbff);
            color: white;
          }
          
          &.success {
            background: linear-gradient(135deg, #67c23a, #95d475);
            color: white;
          }
        }
        
        .card-info {
          .card-value {
            font-size: 28px;
            font-weight: 700;
            color: #2c3e50;
            line-height: 1.2;
          }
          
          .card-label {
            font-size: 14px;
            color: #7f8c8d;
            margin-top: 4px;
          }
        }
      }
    }
  }
  
  .table-card {
    border-radius: 12px;
    border: none;
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
    }
    
    .backup-table {
      :deep(.el-table__header) {
        .table-header-text {
          font-weight: 600;
          color: #2c3e50;
        }
      }
      
      :deep(.el-table__body) {
        .time-cell {
          display: flex;
          align-items: center;
          gap: 8px;
          
          .time-icon {
            color: #909399;
          }
        }
        
        .data-preview {
          font-family: 'Monaco', 'Menlo', 'Ubuntu Mono', monospace;
          font-size: 12px;
          color: #606266;
          line-height: 1.4;
        }
        
        .action-buttons {
          display: flex;
          gap: 8px;
          justify-content: center;
          
          .view-btn,
          .restore-btn,
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
.data-dialog,
.confirm-dialog {
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
}

.dialog-content {
  .dialog-header {
    display: flex;
    align-items: center;
    gap: 8px;
    margin-bottom: 16px;
    font-weight: 600;
    color: #2c3e50;
    
    .dialog-icon {
      color: #409eff;
    }
  }
  
  .data-viewer {
    .data-textarea {
      :deep(.el-textarea__inner) {
        font-family: 'Monaco', 'Menlo', 'Ubuntu Mono', monospace;
        font-size: 13px;
        line-height: 1.5;
        border-radius: 8px;
        background: #f8f9fa;
        border: 1px solid #e4e7ed;
      }
    }
  }
}

.confirm-content {
  text-align: center;
  
  .confirm-icon {
    width: 64px;
    height: 64px;
    background: linear-gradient(135deg, #e6a23c, #f0c78a);
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    margin: 0 auto 16px;
    font-size: 28px;
    color: white;
  }
  
  .confirm-text {
    margin-bottom: 20px;
    
    h3 {
      margin: 0 0 8px 0;
      color: #2c3e50;
    }
    
    p {
      margin: 0;
      color: #7f8c8d;
      line-height: 1.5;
    }
  }
  
  .confirm-info {
    background: #f8f9fa;
    border-radius: 8px;
    padding: 16px;
    
    .info-item {
      display: flex;
      align-items: center;
      gap: 8px;
      margin-bottom: 8px;
      color: #606266;
      
      &:last-child {
        margin-bottom: 0;
      }
      
      strong {
        color: #2c3e50;
      }
    }
  }
}

.dialog-footer {
  display: flex;
  justify-content: flex-end;
  gap: 12px;
  
  .cancel-btn,
  .copy-btn,
  .confirm-btn {
    border-radius: 8px;
    padding: 10px 20px;
  }
}

// 响应式设计
@media (max-width: 768px) {
  .backup-container {
    padding: 16px;
  }
  
  .backup-header {
    flex-direction: column;
    gap: 16px;
    
    .header-actions {
      width: 100%;
      
      .action-btn {
        flex: 1;
      }
    }
  }
  
  .data-cards {
    grid-template-columns: 1fr !important;
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

<style>
/* 全局对话框样式 */
.restore-confirm-dialog .el-message-box__message {
  line-height: 1.6;
}

.delete-confirm-dialog .el-message-box__status {
  color: #f56c6c;
}
</style>