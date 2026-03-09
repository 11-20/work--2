

from django.urls import path
from work.controller import RoleController
from work.controller import UserController
from work.controller import AuthorityController
from work.controller import SteamController

from django.conf import settings
from django.conf.urls.static import static

from work.controller import CarouselController
from work.controller import HealthnewsController
from work.controller import PredictionrecordController
from work.controller import HealthdataController
from work.controller import NoticeController
from work.controller import PredictionmodelController
from work.controller import HealthsummaryController
from work.controller import VisualizationconfigController
from work.controller import ReporttemplateController
from work.controller import AnalysisresultController
from work.controller import SysmsgController
from work.controller import BackupController
from work.controller import SysargController
from work.controller import SyslogController

urlpatterns = [

    
    path('basic/getwebsiteinfo', SteamController.getWebsiteInfo),
    path('basic/uploadsinglefile', SteamController.uploadSingleFile),

    path('user/index', UserController.getUser),
    path('user/store', UserController.createUser),
    path('user/show', UserController.getUserById),
    path('user/update', UserController.updateUserById),
    path('user/updatepassword', UserController.reset_password),
    path('user/destroy', UserController.removeUserById),
    path('signin', UserController.login),
    path('register', UserController.register),

    path('role/index', RoleController.getRole),
    path('role/store', RoleController.createRole),
    path('role/show', RoleController.getRoleById),
    path('role/update', RoleController.updateRoleById),
    path('role/destroy', RoleController.removeRoleById),
    path('role/getrolepermission', RoleController.getRoleAuthoritymission),
    path('role/insertrolepermission', RoleController.insertRoleAuthoritymission),
    path('role/deleterolepermission', RoleController.deleteRoleAuthoritymission),

    path('authority/index', AuthorityController.getAuthority),
    path('authority/store', AuthorityController.createAuthority),
    path('authority/update', AuthorityController.updateAuthorityById),
    path('authority/delete', AuthorityController.removeAuthorityById),

    
    path('carousel/store',CarouselController.createCarousel),

    path('carousel/destroy',CarouselController.removeCarouselById),

    
    path('carousel/update',CarouselController.updateCarouselById),

    
    path('carousel/index',CarouselController.getCarousel),

    path('carousel/show',CarouselController.getCarouselById),

    path('healthnews/store',HealthnewsController.createHealthnews),

    path('healthnews/destroy',HealthnewsController.removeHealthnewsById),

    
    path('healthnews/update',HealthnewsController.updateHealthnewsById),

    
    path('healthnews/index',HealthnewsController.getHealthnews),

    path('healthnews/show',HealthnewsController.getHealthnewsById),

    path('predictionrecord/store',PredictionrecordController.createPredictionrecord),

    path('predictionrecord/destroy',PredictionrecordController.removePredictionrecordById),

    
    path('predictionrecord/update',PredictionrecordController.updatePredictionrecordById),

    
    path('predictionrecord/index',PredictionrecordController.getPredictionrecord),

    path('predictionrecord/show',PredictionrecordController.getPredictionrecordById),

    path('healthdata/store',HealthdataController.createHealthdata),

    path('healthdata/destroy',HealthdataController.removeHealthdataById),

    
    path('healthdata/update',HealthdataController.updateHealthdataById),

    
    path('healthdata/index',HealthdataController.getHealthdata),

    path('healthdata/show',HealthdataController.getHealthdataById),

    path('notice/store',NoticeController.createNotice),

    path('notice/destroy',NoticeController.removeNoticeById),

    
    path('notice/update',NoticeController.updateNoticeById),

    
    path('notice/index',NoticeController.getNotice),

    path('notice/show',NoticeController.getNoticeById),

    path('predictionmodel/store',PredictionmodelController.createPredictionmodel),

    path('predictionmodel/destroy',PredictionmodelController.removePredictionmodelById),

    
    path('predictionmodel/update',PredictionmodelController.updatePredictionmodelById),

    
    path('predictionmodel/index',PredictionmodelController.getPredictionmodel),

    path('predictionmodel/show',PredictionmodelController.getPredictionmodelById),

    path('healthsummary/store',HealthsummaryController.createHealthsummary),

    path('healthsummary/destroy',HealthsummaryController.removeHealthsummaryById),

    
    path('healthsummary/update',HealthsummaryController.updateHealthsummaryById),

    
    path('healthsummary/index',HealthsummaryController.getHealthsummary),

    path('healthsummary/show',HealthsummaryController.getHealthsummaryById),

    path('visualizationconfig/store',VisualizationconfigController.createVisualizationconfig),

    path('visualizationconfig/destroy',VisualizationconfigController.removeVisualizationconfigById),

    
    path('visualizationconfig/update',VisualizationconfigController.updateVisualizationconfigById),

    
    path('visualizationconfig/index',VisualizationconfigController.getVisualizationconfig),

    path('visualizationconfig/show',VisualizationconfigController.getVisualizationconfigById),

    path('reporttemplate/store',ReporttemplateController.createReporttemplate),

    path('reporttemplate/destroy',ReporttemplateController.removeReporttemplateById),

    
    path('reporttemplate/update',ReporttemplateController.updateReporttemplateById),

    
    path('reporttemplate/index',ReporttemplateController.getReporttemplate),

    path('reporttemplate/show',ReporttemplateController.getReporttemplateById),

    path('analysisresult/store',AnalysisresultController.createAnalysisresult),

    path('analysisresult/destroy',AnalysisresultController.removeAnalysisresultById),

    
    path('analysisresult/update',AnalysisresultController.updateAnalysisresultById),

    
    path('analysisresult/index',AnalysisresultController.getAnalysisresult),

    path('analysisresult/show',AnalysisresultController.getAnalysisresultById),

    path('sysmsg/store',SysmsgController.createSysmsg),

    path('sysmsg/destroy',SysmsgController.removeSysmsgById),

    
    path('sysmsg/update',SysmsgController.updateSysmsgById),

    
    path('sysmsg/index',SysmsgController.getSysmsg),

    path('sysmsg/show',SysmsgController.getSysmsgById),

    path('backup/store',BackupController.createBackup),

    path('backup/destroy',BackupController.removeBackupById),

    
    path('backup/update',BackupController.updateBackupById),

    
    path('backup/index',BackupController.getBackup),

    path('backup/show',BackupController.getBackupById),

    path('sysarg/store',SysargController.createSysarg),

    path('sysarg/destroy',SysargController.removeSysargById),

    
    path('sysarg/update',SysargController.updateSysargById),

    
    path('sysarg/index',SysargController.getSysarg),

    path('sysarg/show',SysargController.getSysargById),

    path('syslog/store',SyslogController.createSyslog),

    path('syslog/destroy',SyslogController.removeSyslogById),

    
    path('syslog/update',SyslogController.updateSyslogById),

    
    path('syslog/index',SyslogController.getSyslog),

    path('syslog/show',SyslogController.getSyslogById),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)  
