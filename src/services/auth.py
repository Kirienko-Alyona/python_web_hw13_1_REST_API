from typing import Optional
import pickle

from jose import JWTError, jwt
from fastapi import HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
from datetime import datetime, timedelta
import redis
from sqlalchemy.orm import Session
from src.database.models import User
from src.conf.config import settings

from src.database.db import get_db
from src.repository import users as repository_users


class Auth:
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    SECRET_KEY = settings.secret_key
    ALGORITHM = settings.algorithm
    oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")
    client_redis = redis.Redis(host=settings.redis_host, port=settings.redis_port, db=0)
    credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )


    def verify_password(self, plain_password, hashed_password):
        """
        The verify_password function takes a plain-text password and the hashed version of that password,
            and returns True if they match, False otherwise. This is used to verify that the user's login
            credentials are correct.
        
        :param self: Make the method belong to the class
        :param plain_password: Pass in the password that is entered by the user
        :param hashed_password: Compare the hashed password in the database with a plain text password
        :return: A boolean value, true or false
        :doc-author: Trelent
        """
        return self.pwd_context.verify(plain_password, hashed_password)

    def get_password_hash(self, password: str):
        """
        The get_password_hash function takes a password as input and returns the hash of that password.
            The function uses the pwd_context object to generate a hash from the given password.
        
        :param self: Represent the instance of the class
        :param password: str: Pass the password to be hashed
        :return: A hash of the password
        :doc-author: Trelent
        """
        return self.pwd_context.hash(password)

    # define a function to generate a new access token
    async def create_access_token(self, data: dict, expires_delta: Optional[float] = None):
        """
        The create_access_token function creates a new access token for the user.
            
        
        :param self: Represent the instance of the class
        :param data: dict: Pass in the data that will be encoded into the token
        :param expires_delta: Optional[float]: Set the expiration time of the token
        :return: A string that is the encoded access token
        :doc-author: Trelent
        """
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.utcnow() + timedelta(seconds=expires_delta)
        else:
            expire = datetime.utcnow() + timedelta(minutes=15)
        to_encode.update({"iat": datetime.utcnow(), "exp": expire, "scope": "access_token"})
        encoded_access_token = jwt.encode(to_encode, self.SECRET_KEY, algorithm=self.ALGORITHM)
        return encoded_access_token

    # define a function to generate a new refresh token
    async def create_refresh_token(self, data: dict, expires_delta: Optional[float] = None):
        """
        The create_refresh_token function creates a refresh token for the user.
            Args:
                data (dict): A dictionary containing the user's id and username.
                expires_delta (Optional[float]): The number of seconds until the refresh token expires. Defaults to None, which sets it to 7 days from now.
        
        :param self: Represent the instance of a class
        :param data: dict: Pass in the data that will be encoded into the token
        :param expires_delta: Optional[float]: Set the expiration time of the refresh token
        :return: A refresh token that is encoded with the user's id, email and username
        :doc-author: Trelent
        """
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.utcnow() + timedelta(seconds=expires_delta)
        else:
            expire = datetime.utcnow() + timedelta(days=7)
        to_encode.update({"iat": datetime.utcnow(), "exp": expire, "scope": "refresh_token"})
        encoded_refresh_token = jwt.encode(to_encode, self.SECRET_KEY, algorithm=self.ALGORITHM)
        return encoded_refresh_token
    

    async def decode_refresh_token(self, refresh_token: str):
        """
        The decode_refresh_token function takes a refresh token and decodes it.
            If the scope is 'refresh_token', then we return the email address of the user.
            Otherwise, we raise an HTTPException with status code 401 (UNAUTHORIZED) and detail message 'Invalid scope for token'.
        
        
        :param self: Represent the instance of the class
        :param refresh_token: str: Pass the refresh token to the function
        :return: The email of the user who requested a refresh token
        :doc-author: Trelent
        """
        try:
            payload = jwt.decode(refresh_token, self.SECRET_KEY, algorithms=[self.ALGORITHM])
            if payload['scope'] == 'refresh_token':
                email = payload['sub']
                return email
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Invalid scope for token')
        except JWTError:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Could not validate credentials')
        
    def verify_jwt_token(self, token: str = Depends(oauth2_scheme)):    
        """
        The verify_jwt_token function is a dependency for the protected endpoints.
        It will be called in the background to check if the user has access rights.
        If there is no valid token, it will raise an HTTPException with the error text.
        
        :param self: Represent the instance of a class
        :param token: str: Get the token from the authorization header
        :return: The email of the user
        :doc-author: Trelent
        """
        try:
            # Decode JWT
            payload = jwt.decode(token, self.SECRET_KEY, algorithms=[self.ALGORITHM])
            if payload['scope'] == 'access_token':
                email = payload["sub"]
                if email is None:
                    raise self.credentials_exception
            else:
                raise self.credentials_exception
        except JWTError as e:
            raise self.credentials_exception 
        return email   
        
        
    async def set_current_user(self, user: User):
        """
        The set_current_user function is used to set the current user in redis.
            Args:
                user (User): The User object that will be stored in redis.
        
        :param self: Represent the instance of the class
        :param user: User: Store the user object in redis
        :return: A user object
        :doc-author: Trelent
        """
        #email = self.verify_jwt_token(token)
        self.client_redis.set(f"user:{user.email}", pickle.dumps(user))


    async def get_current_user(self, token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
        """
        The get_current_user function is a dependency that will be called by FastAPI to get the current user.
        It uses the token in the Authorization header, decodes it and returns an object with all of its claims.
        
        :param self: Access the class attributes
        :param token: str: Get the token from the header of the request
        :param db: Session: Pass the database session to the function
        :return: A user object with the following fields:
        :doc-author: Trelent
        """
        #user = await repository_users.get_user_by_email(email, db)
        email = self.verify_jwt_token(token)
        user = self.client_redis.get(f"user:{email}")
        if user is None:
            user = await repository_users.get_user_by_email(email, db)
            if user is None:
                raise self.credentials_exception
            self.client_redis.set(f"user:{email}", pickle.dumps(user))
            self.client_redis.expire(f"user:{email}", 900)
        else:
            user = pickle.loads(user)
        #if user is None:
        #    raise credentials_exception
        return user
    
    
    def create_email_token(self, data: dict):
        """
        The create_email_token function creates a token that is used to verify the user's email address.
            The token contains the following data:
                - iat (issued at): The time when the token was created.
                - exp (expiration): When this token expires, 7 days from now.
                - scope: What this JWT can be used for, in this case it is an email_token which means it can only be used to verify an email address.
        
        :param self: Represent the instance of the class
        :param data: dict: Pass in the data that will be encoded into a token
        :return: A token
        :doc-author: Trelent
        """
        to_encode = data.copy()
        expire = datetime.utcnow() + timedelta(days=7)
        to_encode.update({"iat": datetime.utcnow(), "exp": expire, "scope": "email_token"})
        token = jwt.encode(to_encode, self.SECRET_KEY, algorithm=self.ALGORITHM)
        return token
    
    
    def get_email_from_token(self, token: str):
        """
        The get_email_from_token function takes a token as an argument and returns the email address associated with that token.
        If the scope of the token is not 'email_token', then it raises an HTTPException. If there is a JWTError, then it also raises
        an HTTPException.
        
        :param self: Represent the instance of the class
        :param token: str: Pass the token to the function
        :return: The email associated with the token
        :doc-author: Trelent
        """
        try:
            payload = jwt.decode(token, self.SECRET_KEY, algorithms=[self.ALGORITHM])
            if payload['scope'] == 'email_token':
                email = payload['sub']
                return email
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Invalid scope for token')
        except JWTError as e:
            print(e)
            raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                                detail="Invalid token for email verification")


auth_service = Auth()