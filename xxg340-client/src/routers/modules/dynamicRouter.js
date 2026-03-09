
    export default  [
  {
    "name": "首页",
    "isNav": true,
    "path": "/index/index",
    "component": () => import('@/views/index/index/index.vue')
  },
  {
    "name": "健康资讯列表",
    "isNav": true,
    "path": "/healthnews/index",
    "component": () => import('@/views/healthnews/index/index.vue')
  },
  {
    "name": "健康资讯详情",
    "path": "/healthnews/detail",
    "component": () => import('@/views/healthnews/detail/detail.vue')
  },
  {
    "name": "单次预测",
    "isNav": true,
    "path": "/prediction/single",
    "component": () => import('@/views/prediction/single/single.vue')
  },
  {
    "name": "批量预测",
    "isNav": true,
    "path": "/prediction/batch",
    "component": () => import('@/views/prediction/batch/batch.vue')
  },
  {
    "name": "预测历史",
    "isNav": true,
    "path": "/prediction/history",
    "component": () => import('@/views/prediction/history/history.vue')
  },
  {
    "name": "报告详情",
    "path": "/prediction/report",
    "component": () => import('@/views/prediction/report/report.vue')
  },
  {
    "name": "数据录入",
    "isNav": true,
    "path": "/healthdata/input",
    "component": () => import('@/views/healthdata/input/input.vue')
  },
  {
    "name": "数据信息",
    "isNav": true,
    "path": "/healthdata/list",
    "component": () => import('@/views/healthdata/list/list.vue')
  },
  {
    "name": "健康数据编辑",
    "path": "/healthdata/edit",
    "component": () => import('@/views/healthdata/edit/edit.vue')
  },
  {
    "name": "疾病风险趋势分析",
    "isNav": true,
    "path": "/visualization/risktrend",
    "component": () => import('@/views/visualization/risktrend/risktrend.vue')
  },
  {
    "name": "健康指标分布图",
    "isNav": true,
    "path": "/visualization/healthdist",
    "component": () => import('@/views/visualization/healthdist/healthdist.vue')
  },
  {
    "name": "预测结果统计图",
    "isNav": true,
    "path": "/visualization/predstats",
    "component": () => import('@/views/visualization/predstats/predstats.vue')
  },
  {
    "name": "我的预测",
    "isNav": true,
    "isUserMenu": true,
    "path": "/user/mypredictions",
    "component": () => import('@/views/user/mypredictions/mypredictions.vue')
  },
  {
    "name": "健康数据详情",
    "isNav": false,
    "path": "/healthdata/detail",
    "component": () => import('@/views/healthdata/detail/detail.vue')
  }
]