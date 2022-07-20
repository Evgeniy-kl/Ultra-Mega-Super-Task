class UserManage:
    @staticmethod
    def check_user(user, u):
        if user.email == u.email and user.password == u.password:
            return True
        return False
