from model.UserModel import User
from model.RoleModel import Role
from model.sql import DB

class PermissionDao:
    @staticmethod
    def get_user_rolecode(user_id):
        sql = """
            SELECT UserId, RoleCode
            FROM [User]
            WHERE UserId = :user_id
        """
        session = DB.get_session()
        result = DB.execute(session, sql, {'user_id': user_id})
        row = DB.fetchone(result)
        if row:
            user = User()
            user.UserId = row[0]
            user.RoleCode = row[1]
            return user
        return None

    @staticmethod
    def get_role_permission(role_code):
        sql = """
            SELECT RoleId, RoleName, RoleCode, RoleScope, RolePermission
            FROM [Role]
            WHERE RoleCode = :role_code
        """
        session = DB.get_session()
        result = DB.execute(session, sql, {'role_code': role_code})
        row = DB.fetchone(result)
        if row:
            role = Role()
            role.RoleId = row[0]
            role.RoleName = row[1]
            role.RoleCode = row[2]
            role.RoleScope = row[3]
            role.RolePermission = row[4]
            return role
        return None
