from fastapi import APIRouter, Depends
from services import UserService, PostService
import schemas

router = APIRouter()


'''  '''''''''''''  '''
'''  user router    '''
''''''''''''''''''' '''


@router.get('/users', tags=['USERS'])
async def get_users(service: UserService = Depends()):
    return await service.getAllUsers()


@router.get('/users/{user_id}', tags=['USERS'])
async def get_user(user_id: int, service: UserService = Depends()):
    return await service.findUserById(user_id)


@router.post('/users', tags=['USERS'])
async def create_user(payload: schemas.User, service: UserService = Depends()):
    return await service.createUser(payload)


'''  '''''''''''''  '''
'''  post router    '''
''''''''''''''''''' '''


@router.get('/posts', tags=['Posts'])
async def get_posts(service: PostService = Depends()):
    return await service.getAllPosts()


@router.get('/posts/{post_id}', tags=['Posts'])
async def get_post(post_id: int, service: PostService = Depends()):
    return await service.findPostById(post_id)


@router.post('/posts', tags=['Posts'])
async def create_post(payload: schemas.Post, service: PostService = Depends()):
    return await service.createPost(payload)


@router.put('/posts/{post_id}', tags=['Posts'])
async def update_post(post_id: int, payload: schemas.Post, service: PostService = Depends()):
    return await service.updatePost(post_id, payload)


@router.delete('/posts/{post_id}', tags=['Posts'])
async def remove_post(post_id: int, service: PostService = Depends()):
    return await service.removePost(post_id)
