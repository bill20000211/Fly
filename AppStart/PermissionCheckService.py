from Repository.PermissionDao import PermissionDao

class PermissionCheckService:

    @staticmethod
    def setSession(session, user_id):
        """
        設定Session內容，包括使用者資訊、角色權限、節點
        :param session: Flask session
        :param user_id: 使用者ID
        """
        user_dto = PermissionDao.get_user_rolecode(user_id)
        if not user_dto:
            return False

        role_dto = PermissionDao.get_role_permission(user_dto.RoleCode)
        if not role_dto or not role_dto.RolePermission:
            return False

        # 存入Session
        session['user_id'] = user_id
        session['username'] = getattr(user_dto, 'UserName', None)
        session['role_code'] = user_dto.RoleCode
        session['role_permission'] = role_dto.RolePermission  # 逗號分隔字串
        session['node_list'] = role_dto.RolePermission.split(',')  # 節點清單

        return True

    @staticmethod
    def has_permission(user_id, node_id=None, function_name=None):
        user_dto = PermissionDao.get_user_rolecode(user_id)

        if not user_dto:
            return False
        
        role_dto = PermissionDao.get_role_permission(user_dto.RoleCode)

        if not role_dto or not role_dto.RolePermission:
            return False
        
        permissions = role_dto.RolePermission  # 逗號分隔字串

        if node_id and str(node_id) not in permissions:
            return False
        
        if function_name and function_name not in permissions:
            return False
        
        return True
