export default {
  "admin": {
    "name": "管理员",
    "roleId": "1",
    "description": "拥有系统全部权限",
    "menus": [
      {
        "name": "用户管理",
        "children": [
          {
            "name": "用户信息",
            "path": "/sys/usermanage"
          }
        ]
      },
      {
        "name": "用户管理",
        "children": []
      },
      {
        "name": "健康资讯管理",
        "children": [
          {
            "name": "健康资讯列表",
            "path": "/healthnews/index"
          }
        ]
      },
      {
        "name": "轮播图管理",
        "children": [
          {
            "name": "轮播图列表",
            "path": "/carousel/index"
          }
        ]
      },
      {
        "name": "预测模型管理",
        "children": [
          {
            "name": "预测模型列表",
            "path": "/predictionmodel/index"
          }
        ]
      },
      {
        "name": "数据统计分析",
        "children": [
          {
            "name": "健康统计汇总",
            "path": "/healthsummary/index"
          },
          {
            "name": "分析结果管理",
            "path": "/analysisresult/index"
          },
          {
            "name": "可视化配置",
            "path": "/visualizationconfig/index"
          },
          {
            "name": "报告模板管理",
            "path": "/reporttemplate/index"
          }
        ]
      },
      {
        "name": "通知公告管理",
        "children": [
          {
            "name": "通知公告列表",
            "path": "/notice/index"
          }
        ]
      },
      {
        "name": "健康数据管理",
        "children": [
          {
            "name": "健康数据列表",
            "path": "/healthdata/index"
          }
        ]
      },
      {
        "name": "预测记录管理",
        "children": [
          {
            "name": "预测记录列表",
            "path": "/predictionrecord/index"
          }
        ]
      }
    ]
  }
}