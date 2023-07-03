from django.contrib.auth.models import User
from .models import Post
from rest_framework import status
from rest_framework.test import APITestCase

"""
For each test a temporary DB is created and destroyed before the next test is run.
This allows us to count the number of posts in the DB in each test because we are not using the real DB.

* All test methods must start with 'test_'
"""


class PostListViewsTestCase(APITestCase):
    def setUp(self):
        User.objects.create_user(username='test', password='test')

    def test_can_list_posts(self):
        test = User.objects.get(username='test')
        Post.objects.create(owner=test, title='test title')
        response = self.client.get('/posts/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        print(f"List Posts: {response.status_code}")

    def test_logged_in_user_can_create_post(self):
        self.client.login(username='test', password='test')
        response = self.client.post('/posts/', {'title': 'test title'})
        count = Post.objects.count()
        self.assertEqual(count, 1)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        print(f"Logged in user can POST: {response.status_code}")

    def test_logged_out_user_cannot_create_post(self):
        response = self.client.post('/posts/', {'title': 'test title'})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        print(f"Logged Out User is prevented from POST: {response.status_code}")

class postDetailViewTestCase(APITestCase):
    def setUp(self):
        user_post_owner = User.objects.create_user(username='post_owner', password='test')
        user_not_post_owner = User.objects.create_user(username='not_post_owner', password='test')
        Post.objects.create(owner=user_post_owner, title='test title')
        Post.objects.create(owner=user_not_post_owner, title='test title')

    def test_can_get_post_details(self):
        response = self.client.get('/posts/1/')
        self.assertEqual(response.data['title'], 'test title')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        print(f"Can get post details: {response.status_code}")

    def test_can_not_get_invalid_post_id(self):
        response = self.client.get('/posts/abc/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        print(f"Can not get invalid post id: {response.status_code}")

    def test_user_can_update_own_post(self):
        self.client.login(username='post_owner', password='test')
        response = self.client.put('/posts/1/', {'title': 'updated title'})
        test_post = Post.objects.filter(pk=1).first()
        self.assertEqual(test_post.title, 'updated title')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        print(f"User can update own post: {response.status_code}")

    def test_user_cannot_update_other_user_post(self):
        self.client.login(username='post_owner', password='test')
        response = self.client.put('/posts/2/', {'title': 'updated title'})
        test_post = Post.objects.filter(pk=1).first()
        self.assertEqual(test_post.title, 'test title')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        print(f"User cannot update other user post: {response.status_code}")