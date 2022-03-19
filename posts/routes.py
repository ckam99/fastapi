from fastapi import APIRouter, HTTPException
from producers import PostProducer
from schemas import Post as PostSchema
from models import Post
from tortoise.contrib.pydantic import pydantic_model_creator

router = APIRouter(prefix='/posts')

serializer = pydantic_model_creator(Post)


@router.get('/', response_model=list[PostSchema])
async def get_posts():
    return await serializer.from_queryset(Post.all())


@router.get('/{post_id}')
async def get_post(post_id: int):
    obj = await Post.get(id=post_id)
    if obj:
        return await serializer.from_queryset_single(obj)
    raise HTTPException(
        404, detail={'error': f'Model not found with id ({post_id})'})


@router.post('/', response_model=PostSchema)
async def create_post(post: PostSchema):
    obj = await Post.create(**post.dict(exclude={'id'}))
    obj = serializer.from_orm(obj)
    PostProducer().post_created(obj.dict())
    return obj


@router.put('/{post_id}', response_model=PostSchema)
async def update_post(post_id: int, post: PostSchema):
    obj = await Post.get(id=post_id)
    if obj:
        obj = await obj.update_from_dict(**post.dict())
        obj = await serializer.from_queryset_single(obj)
        PostProducer().post_updated(obj.dict())
        return obj
    raise HTTPException(
        404, detail={'error': f'Model not found with id ({post_id})'})


@router.delete('/{post_id}')
async def delete_post(post_id: int):
    obj = await Post.get(id=post_id)
    if obj:
        await obj.delete()
        obj = await serializer.from_queryset_single(obj)
        PostProducer().post_removed(obj.dict())
    raise HTTPException(
        404, detail={'error': f'Model not found with id ({post_id})'})
