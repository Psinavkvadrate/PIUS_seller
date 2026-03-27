from app.services.auth_service import AuthService

async def register_user(db, request):
    return await AuthService.register(db, request)

async def login_user(db, request):
    return await AuthService.login(db, request)