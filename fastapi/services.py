from models import Post, User
from typing import List
from fastapi import HTTPException
import schemas


class UserService():

    async def getAllUsers(self) -> List[User]:
        users = await User.all()
        return users

    async def createUser(self, payload: schemas.User) -> User:
        user = await User.create(**payload.dict())
        return user

    async def findUserById(self, user_id: int) -> User:
        user = await User.filter(id=user_id).first()
        if user is None:
            raise HTTPException(status_code=404, detail={
                                "error": f"User[{user_id}] not found"})
        return user


class PostService():

    async def getAllPosts(self) -> List[Post]:
        posts = await Post.all()
        return posts

    async def createPost(self, payload: schemas.Post) -> Post:
        post = await Post.create(**payload.dict())
        return post

    async def findPostById(self, post_id: int) -> Post:
        post = await Post.filter(id=post_id).first()
        if post is None:
            raise HTTPException(status_code=404, detail={
                                "error": f"Post[{post_id}] not found"})
        return post

    async def updatePost(self, post_id: int, payload: schemas.Post) -> Post:
        post = await self.findPostById(post_id)
        post = await post.update_from_dict(payload.dict())
        return post

    async def removePost(self, post_id: int):
        post = await self.findPostById(post_id)
        await post.delete()
