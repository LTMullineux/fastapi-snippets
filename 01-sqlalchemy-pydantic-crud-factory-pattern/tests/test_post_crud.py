import pytest

from snippets.crud import CrudFactory, IntegrityConflictException
from snippets.models import Post, PostSchema, PostUpdateSchema

PostCrud = CrudFactory(Post)


@pytest.mark.asyncio
class TestPostCrud:
    async def test_create_post(self, session):
        post_create = PostSchema(title="my first post", content="hello world")
        post = await PostCrud.create(session, post_create)
        assert post.uuid is not None
        assert post.created_at is not None
        assert post.updated_at is not None
        assert post.title == "my first post"
        assert post.content == "hello world"

    async def test_create_many_posts(self, session):
        posts_create = [
            PostSchema(title="1: my first post", content="hello world"),
            PostSchema(title="2: my second post", content="hello world again"),
        ]
        posts = await PostCrud.create_many(session, posts_create, return_models=True)
        posts = sorted(posts, key=lambda x: x.title)

        assert posts[0].uuid is not None
        assert posts[0].created_at is not None
        assert posts[0].updated_at is not None
        assert posts[0].title == "1: my first post"
        assert posts[0].content == "hello world"

        assert posts[1].uuid is not None
        assert posts[1].created_at is not None
        assert posts[1].updated_at is not None
        assert posts[1].title == "2: my second post"
        assert posts[1].content == "hello world again"

    async def test_create_many_posts_unique_name_error(self, session):
        posts_create = [
            PostSchema(title="1: my first post", content="hello world"),
            PostSchema(title="1: my first post", content="a different hello world"),
        ]

        with pytest.raises(IntegrityConflictException):
            _ = await PostCrud.create_many(session, posts_create)

    async def test_get_one_by_id(self, session):
        posts_create = [
            PostSchema(title="1: my first post", content="hello world"),
            PostSchema(title="2: my second post", content="hello world again"),
        ]
        posts = await PostCrud.create_many(session, posts_create, return_models=True)
        posts = sorted(posts, key=lambda x: x.title)

        post = await PostCrud.get_one_by_id(session, posts[0].uuid)
        assert post.title == "1: my first post"
        assert post.content == "hello world"

    async def test_get_many_by_ids(self, session):
        posts_create = [
            PostSchema(title="1: my first post", content="hello world"),
            PostSchema(title="2: my second post", content="hello world again"),
            PostSchema(title="3: my third post", content="foo bar baz"),
        ]
        posts = await PostCrud.create_many(session, posts_create, return_models=True)
        posts = sorted(posts, key=lambda x: x.title)

        posts_selected = await PostCrud.get_many_by_ids(
            session, [posts[0].uuid, posts[2].uuid]
        )
        posts_selected = sorted(posts_selected, key=lambda x: x.title)

        assert posts_selected[0].title == "1: my first post"
        assert posts_selected[1].title == "3: my third post"

    async def test_update_by_id(self, session):
        posts_create = [
            PostSchema(title="1: my first post", content="hello world"),
            PostSchema(title="2: my second post", content="hello world again"),
        ]
        posts = await PostCrud.create_many(session, posts_create, return_models=True)
        posts = sorted(posts, key=lambda x: x.title)

        post_update = PostUpdateSchema(content="i changed my mind")
        post1 = await PostCrud.update_by_id(session, post_update, posts[0].uuid)
        assert post1.content == "i changed my mind"

    async def test_update_many_by_ids(self, session):
        posts_create = [
            PostSchema(title="1: my first post", content="hello world"),
            PostSchema(title="2: my second post", content="hello world again"),
            PostSchema(title="3: my third post", content="foo bar baz"),
        ]
        posts = await PostCrud.create_many(session, posts_create, return_models=True)
        posts = sorted(posts, key=lambda x: x.title)

        updates = {
            posts[0].uuid: PostUpdateSchema(published=True, views=1),
            posts[2].uuid: PostUpdateSchema(published=True, views=2),
        }
        posts_updated = await PostCrud.update_many_by_ids(
            session, updates, return_models=True
        )
        posts = sorted(posts, key=lambda x: x.title)

        assert posts_updated[0].uuid == posts[0].uuid
        assert posts_updated[0].published is True
        assert posts_updated[0].views == 1

        assert posts_updated[1].uuid == posts[2].uuid
        assert posts_updated[1].published is True
        assert posts_updated[1].views == 2

    async def test_remove_by_id(self, session):
        posts_create = [
            PostSchema(title="1: my first post", content="hello world"),
            PostSchema(title="2: my second post", content="hello world again"),
        ]
        posts = await PostCrud.create_many(session, posts_create, return_models=True)
        posts = sorted(posts, key=lambda x: x.title)

        row_count = await PostCrud.remove_by_id(session, posts[0].uuid)
        assert row_count == 1

        all_posts = await PostCrud.get_many_by_ids(
            session, [posts[0].uuid, posts[1].uuid]
        )
        assert len(all_posts) == 1

        row_count = await PostCrud.remove_by_id(session, posts[0].uuid)
        assert row_count == 0

    async def test_remove_many_by_ids(self, session):
        posts_create = [
            PostSchema(title="1: my first post", content="hello world"),
            PostSchema(title="2: my second post", content="hello world again"),
            PostSchema(title="3: my third post", content="foo bar baz"),
        ]
        posts = await PostCrud.create_many(session, posts_create, return_models=True)
        posts = sorted(posts, key=lambda x: x.title)

        row_count = await PostCrud.remove_many_by_ids(
            session, [posts[0].uuid, posts[1].uuid]
        )
        assert row_count == 2

        row_count = await PostCrud.remove_many_by_ids(
            session, [posts[0].uuid, posts[1].uuid, posts[2].uuid]
        )
        assert row_count == 1
