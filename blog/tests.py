from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from accounts.models import User
from rest_framework.authtoken.models import Token
from .models import Post

class PostTests(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='test_user', password='password123')
        self.token = Token.objects.create(user=self.user)

        self.user2 = User.objects.create_user(username='test_user2', password='password123')
        self.token2 = Token.objects.create(user=self.user2)

        self.post_data = {
            'title': 'Test Post',
            'content': 'This is a test post content.',
        }

    def test_publish_post(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        url = reverse('blog:publish-post')
        response = self.client.post(url, self.post_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_list_posts(self):
        url = reverse('blog:list-posts')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_retrieve_post(self):
        post = Post.objects.create(title='Test Post', content='This is a test post content.', author=self.user)
        url = reverse('blog:retrieve-update-delete-post', kwargs={'pk': post.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_post_no_credentials(self):
        """ Update Post with no credentials provided """
        post = Post.objects.create(title='Test Post', content='This is a test post content.', author=self.user)
        updated_data = {'title': 'Updated Test Post', 'content': 'Updated content.'}
        url = reverse('blog:retrieve-update-delete-post', kwargs={'pk': post.id})
        response = self.client.put(url, updated_data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_update_post_not_author(self):
        """
        Update Post but I'm not its author
        Post auhtor is self.user
        But Passed token is for self.user2
        """
        post = Post.objects.create(title='Test Post', content='This is a test post content.', author=self.user)
        updated_data = {'title': 'Updated Test Post', 'content': 'Updated content.'}
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token2.key)
        url = reverse('blog:retrieve-update-delete-post', kwargs={'pk': post.id})
        response = self.client.put(url, updated_data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_post(self):
        """
        Update Post with the post author token
        """
        post = Post.objects.create(title='Test Post', content='This is a test post content.', author=self.user)
        updated_data = {'title': 'Updated Test Post', 'content': 'Updated content.'}
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        url = reverse('blog:retrieve-update-delete-post', kwargs={'pk': post.id})
        response = self.client.put(url, updated_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Check if the data has been updated correctly in the database
        updated_post = Post.objects.get(id=post.id)
        self.assertEqual(updated_post.title, updated_data['title'])
        self.assertEqual(updated_post.content, updated_data['content'])

    def test_delete_post_no_credentials(self):
        """ Delete Post with no credentials provided """
        post = Post.objects.create(title='Test Post', content='This is a test post content.', author=self.user)
        url = reverse('blog:retrieve-update-delete-post', kwargs={'pk': post.id})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_delete_post_not_author(self):
        """
        Delete Post but I'm not its author
        Post auhtor is self.user
        But passed token is for self.user2
        """
        post = Post.objects.create(title='Test Post', content='This is a test post content.', author=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token2.key)
        url = reverse('blog:retrieve-update-delete-post', kwargs={'pk': post.id})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_post(self):
        post = Post.objects.create(title='Test Post', content='This is a test post content.', author=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        url = reverse('blog:retrieve-update-delete-post', kwargs={'pk': post.id})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        # Check if the post has been deleted from the database
        with self.assertRaises(Post.DoesNotExist):
            Post.objects.get(id=post.id)