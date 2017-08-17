# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.test import TestCase
from django.urls import reverse
from .models import PollUser
# Create your tests here.

def createuser(username, password):

    return PollUser.objects.create(username=username, password=password)

class LoginTest(TestCase):

    def test_no_user(self):

        response = self.client.post(reverse("usermanager:login"), data={'username': 'user1', 'password': '123'})
        self.assertContains(response, "User Does not exist")
        session = self.client.session
        self.assertIs(session.has_key('username'), False)


    def test_wrong_password(self):

        createuser('user1' , '1234')
        response = self.client.post(reverse("usermanager:login"), data={'username': 'user1', 'password': '123'})
        self.assertContains(response, "username and password do not match")
        session = self.client.session
        self.assertIs(session.has_key('username'), False)

    def test_successful_login(self):

        createuser('user2' , '1234')
        response = self.client.post(reverse("usermanager:login"), data={'username': 'user2', 'password': '1234'})
        self.assertRedirects(response, expected_url=reverse('usermanager:home'), status_code=302, target_status_code=200)
        session = self.client.session
        self.assertIs(session.has_key('username'), True)

class SignupTest(TestCase):

    def test_user_already_exist(self):

        createuser('user3', '123')
        response = self.client.post(reverse("usermanager:create_user"), data={'username': 'user3', 'password':'1234', 'confirm-password':'1234'})
        self.assertContains(response, "username already exists")

    def test_password_not_match(self):

        response = self.client.post(reverse("usermanager:create_user"), data={'username': 'user4', 'password':'1234', 'confirm-password':'123'})
        self.assertContains(response, "password does not match")

    def test_successful_signup(self):

        response = self.client.post(reverse("usermanager:create_user"), data={'username': 'user4', 'password':'1234', 'confirm-password':'1234'})
        self.assertRedirects(response, expected_url=reverse('usermanager:login_page'), status_code=302,
                             target_status_code=200)
