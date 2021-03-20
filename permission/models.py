from django.db import models

# Create your models here.


class Project(models.Model):
    """项目表"""
    name = models.CharField(max_length=128, blank=False)
    create_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)


class PermissionList(models.Model):
    """权限列表"""
    class Meta:
        permissions = (
            ("create_test_case", "创建测试用例"),
            ("edit_test_case", "编辑测试用例"),
            ("delete_test_case", "删除测试用例"),
            ("view_test_case", "查看测试用例"),
            ("create_env_config", "创建环境配置"),
            ("edit_env_config", "编辑环境配置"),
            ("delete_env_config", "删除环境配置"),
            ("view_env_config", "查看环境配置"),
            # 根据需要，枚举出需要进行权限控制的操作
        )

