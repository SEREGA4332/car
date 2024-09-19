from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase
from rest_framework import status
from .models import Post, Comment
from django.urls import reverse

User = get_user_model()

class ModelTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.post = Post.objects.create(
            author=self.user,
            text='Test post',
            image='/posts/test_image.jpg'
        )

    def test_post_creation(self):
        self.assertEqual(self.post.text, 'Test post')
        self.assertEqual(self.post.author, self.user)
        self.assertEqual(self.post.likes_count, 0)
        self.assertEqual(self.post.image, '/posts/test_image.jpg')

    def test_comment_creation(self):
        comment = Comment.objects.create(post=self.post, author=self.user, text='Test comment')
        self.assertEqual(comment.text, 'Test comment')
        self.assertEqual(comment.author, self.user)
        self.assertEqual(comment.post, self.post)

class APITests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.client.force_authenticate(user=self.user)
        self.post = Post.objects.create(
            author=self.user,
            text='Test post',
            image='/posts/test_image.jpg'
        )

    def test_create_post(self):
        url = reverse('post-list')
        data = {
            'text': 'New post',
            'image': '/posts/new_image.jpg'
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Post.objects.count(), 2)
        new_post = Post.objects.latest('id')
        self.assertEqual(new_post.text, 'New post')
        self.assertEqual(new_post.image, '/posts/new_image.jpg')

    def test_like_post(self):
        url = reverse('post-like', kwargs={'pk': self.post.id})
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.post.refresh_from_db()
        self.assertEqual(self.post.likes_count, 1)

    # def test_unlike_post(self):
    #     Like.objects.create(user=self.user, post=self.post)
    #     self.post.likes_count = 1
    #     self.post.save()
    #
    #     url = reverse('post-unlike', kwargs={'pk': self.post.id})
    #     response = self.client.post(url)
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)
    #     self.post.refresh_from_db()
    #     self.assertEqual(self.post.likes_count, 0)

    def test_add_comment(self):
        url = reverse('comment-list')
        data = {'text': 'New comment','post': self.post.id}
        response = self.client.post(f'{url}', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Comment.objects.count(), 1)
        self.assertEqual(Comment.objects.first().text, 'New comment')

    def test_get_post_with_comments(self):
        # Создаем комментарий
        comment = Comment.objects.create(
            post=self.post,
            author=self.user,
            text='Круто'
        )

        # Увеличиваем количество лайков
        self.post.likes_count = 20
        self.post.save()

        url = reverse('post-detail', kwargs={'pk': self.post.id})
        response = self.client.get(url)
        print("response", response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Создаем expected_data, используя значения из ответа
        expected_data = {
            "id": self.post.id,
            "text": "Test post",
            "image": "/posts/test_image.jpg",
            "created_at": response.data['created_at'],
            "comments": [
                {
                    "author": self.user.id,
                    "text": "Круто",
                    "created_at": response.data['comments'][0]['created_at']
                }
            ],
            "likes_count": 20
        }

        # Проверяем полное соответствие структуры ответа
        self.assertEqual(response.data, expected_data)