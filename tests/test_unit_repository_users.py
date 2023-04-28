from datetime import date, timedelta
import unittest
from unittest.mock import MagicMock

from sqlalchemy.orm import Session

from src.database.models import User
from src.schemas.users import UserModel, UserDb, UserResponse, TokenModel
from src.repository.users import ( 
    get_user_by_email,
    create_user,
    update_avatar,
    update_token,
    confirmed_email
)


class TestUsers(unittest.IsolatedAsyncioTestCase):
    
    def setUp(self):
        self.session = MagicMock(spec=Session)
        self.user_id = 1, 
        self.email = 'example@mail.com'
        self.url = 'https://'
        self.token = '123'
        self.confirmed = True


    async def test_get_user_by_email(self):
        user = User(email = 'example@mail.com')
        self.session.query(User).filter(email=self.email).first.return_value = user
        result = await get_user_by_email(email=self.email, db=self.session)
        self.assertEqual(result, user)
        
        
    async def test_create_user(self):
        body = UserModel(username='James', email='user@example.com', password='Mqt-4567')
        #result_new_user = User(**body.dict(), avatar=None)
        result = await create_user(body=body, db=self.session)
        self.assertEqual(result.username, body.username)
        self.assertEqual(result.email, body.email)
        self.assertEqual(result.password, body.password)
        self.assertTrue(hasattr(result, "id"))    
    
    
    async def test_update_avatar(self):
        user_old_avatar = User(email='user@example.com', avatar='https://123')
        user_new_avatar = User(avatar='https://')
        self.session.query(User).filter(email=self.email).first.return_value = user_old_avatar
        response_user = await get_user_by_email(email=self.email, db=self.session)
        self.assertEqual(response_user, user_old_avatar)
        result = await update_avatar(email=self.email, url=self.url, db=self.session)
        self.assertEqual(result.avatar, user_new_avatar.avatar)
        self.assertEqual(result.avatar, response_user.avatar)
        self.assertTrue(hasattr(result, "id"))    

    
    async def test_update_token(self):
        user_old_token = User(id='1', refresh_token='')
        user_new_token = User(refresh_token='123')
        self.session.query(User).filter(id=self.user_id).first.return_value = user_old_token
        await update_token(user=user_old_token, token=self.token, db=self.session)
        self.assertEqual(user_new_token.refresh_token, self.token)
    
    
    async def test_confirmed_email(self):
        user_old_conf = User(email='user@example.com', confirmed=False)
        user_new_conf = User(confirmed=True)
        self.session.query(User).filter(email=self.email).first.return_value = user_old_conf
        response_user = await get_user_by_email(email=self.email, db=self.session)
        self.assertEqual(response_user, user_old_conf)
        self.session.query(User).filter(confirmed=self.confirmed).first.return_value = user_new_conf
        await confirmed_email(email=self.email, db=self.session)
        self.assertEqual(user_new_conf.confirmed, self.confirmed)
        