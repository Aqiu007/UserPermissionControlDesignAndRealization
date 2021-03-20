from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User, Group, Permission
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework import serializers, status
from rest_framework.response import Response
from permission.models import Project


class UserSerializer(serializers.ModelSerializer):
    groups = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = User
        fields = '__all__'

    def get_groups(self, obj):
        groups = []
        for item in Group.objects.filter(user=obj):
            groups.append(item.name)
        return groups


class GroupSerializer(serializers.ModelSerializer):
    permissions = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Group
        fields = '__all__'

    def get_permissions(self, obj):
        info = []
        for item in obj.permissions.all():
            info.append(item.name)
        return info


class PermissionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Permission
        fields = '__all__'


class ProjectSerializer(serializers.ModelSerializer):
    create_time = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S")
    update_time = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S")

    class Meta:
        model = Project
        fields = '__all__'


class UserView(ListCreateAPIView):
    """post 创建用户、get 查询用户列表"""
    queryset = User.objects.all().order_by('-id')
    serializer_class = UserSerializer

    def post(self, request, *args, **kwargs):
        # 密码加密存储
        request.data['password'] = make_password(request.data['password'])
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        # 创建用户和组的关联关系
        groups = request.data.get("groups")
        if groups:
            group_obj_list = []
            for group_id in groups:
                group_obj = Group.objects.get(id=group_id)
                group_obj_list.append(group_obj)
                serializer.data['groups'].append(group_obj.name)
            user = User.objects.get(pk=serializer.data['id'])
            user.groups.set(group_obj_list)

        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class UserInfo(RetrieveUpdateDestroyAPIView):
    """get 用户信息、patch 更新或创建用户、put 更新用户、delete删除用户"""
    queryset = User.objects.all().order_by('-id')
    serializer_class = UserSerializer

    def put(self, request, *args, **kwargs):
        if request.data.get("password", None):
            request.data['password'] = make_password(request.data['password'])
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        data = serializer.data
        # 更新用户和组的关联关系
        groups = request.data.get("groups")
        if groups:
            data['groups'] = []
            group_obj_list = []
            for group_id in groups:
                group_obj = Group.objects.get(id=group_id)
                group_obj_list.append(group_obj)
                data['groups'].append(group_obj.name)
            user = User.objects.get(pk=data['id'])
            # 先请空之前的关联关系
            user.groups.clear()
            # 然后设置新的关联关系
            user.groups.set(group_obj_list)
        return Response(data)


class GroupView(ListCreateAPIView):
    """post 创建组、get 查询组列表"""
    queryset = Group.objects.all().order_by('-id')
    serializer_class = GroupSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        # 创建组和权限的关联关系
        permissions = request.data.get("permissions")
        if permissions:
            permission_obj_list = []
            for permission_id in permissions:
                permission_obj = Permission.objects.get(id=permission_id)
                permission_obj_list.append(permission_obj)
                serializer.data["permissions"].append(permission_obj.name)
            group = Group.objects.get(pk=serializer.data['id'])
            group.permissions.set(permission_obj_list)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class GroupInfo(RetrieveUpdateDestroyAPIView):
    """get 组信息、patch 更新或创建组、put 更新组、delete删除组"""
    queryset = Group.objects.all().order_by('-id')
    serializer_class = GroupSerializer

    def put(self, request, *args, **kwargs):
        """put请求"""
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        data = serializer.data
        # 创建组和权限的关联关系
        permissions = request.data.get("permissions")
        if permissions:
            data["permissions"] = []
            permission_obj_list = []
            for permission_id in permissions:
                permission_obj = Permission.objects.get(id=permission_id)
                permission_obj_list.append(permission_obj)
                data["permissions"].append(permission_obj.name)
            group = Group.objects.get(pk=data['id'])
            group.permissions.clear()
            group.permissions.set(permission_obj_list)
        return Response(data)


class PermissionView(ListCreateAPIView):
    """post 创建权限、get 查询权限列表"""
    queryset = Permission.objects.filter(content_type=8).order_by('-id')
    serializer_class = PermissionSerializer


class PermissionInfo(RetrieveUpdateDestroyAPIView):
    """get 权限信息、patch 更新或创建权限、put 更新权限、delete删除权限"""
    queryset = Permission.objects.filter(content_type=8).order_by('-id')
    serializer_class = PermissionSerializer


class ProjectView(ListCreateAPIView):
    """post 创建项目、get 查询项目列表"""
    queryset = Project.objects.all().order_by('-id')
    serializer_class = ProjectSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        # 创建项目的时候，创建一个同名的组，权限控制要用到
        Group.objects.create(name=serializer.data['name'])
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class ProjectInfo(RetrieveUpdateDestroyAPIView):
    """get 项目信息、patch 更新或创建项目、put 更新项目、delete删除项目"""
    queryset = Project.objects.all().order_by('-id')
    serializer_class = ProjectSerializer





