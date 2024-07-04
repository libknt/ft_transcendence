from django.views.decorators.csrf import csrf_exempt
from django.http.response import JsonResponse, HttpResponseRedirect
from django.conf import settings
from django.urls import reverse
from pong.middleware.auth import jwt_exempt
from pong.models import User
from pong.utils.create_response import create_token_response
from datetime import datetime, timedelta
import requests
import base64
import json
import jwt
import os


@jwt_exempt
@csrf_exempt
def oauth_42(request):
	if request.method != 'GET':
		return JsonResponse({
			'message': 'Method is not allowed',
			'status': 'invalidParams'
		}, status=400)
	return HttpResponseRedirect(redirect_to='https://api.intra.42.fr/oauth/authorize?client_id=u-s4t2ud-dedfffaaa0594b5e902763f811b333c2585ba79265f1371aa1272306f3007626&redirect_uri=http%3A%2F%2Flocalhost%3A8080%2Fpong%2Foauth%2Fcallback%2F42&response_type=code')

@jwt_exempt
@csrf_exempt
def callback_42(request):
	if request.method != 'GET':
		return HttpResponseRedirect(redirect_to='/signup#methodNotAllowed')
	code = request.GET.get('code', None)
	if not code:
		return HttpResponseRedirect(redirect_to='/signup#failedToGetCode')
	params = {
		'grant_type': 'authorization_code',
		'client_id': settings.CLIENT_ID_42API,
		'client_secret': settings.CLIENT_SECRET_42API,
		'code': code,
		'redirect_uri': 'http://localhost:8080/pong/oauth/callback/42',
	}
	response_token = requests.post('https://api.intra.42.fr/oauth/token', params=params)
	if response_token.status_code != 200:
		return HttpResponseRedirect(redirect_to='/signup#failedToGetToken')
	access_token = response_token.json()['access_token']
	headers = {
		'Authorization': 'Bearer ' + access_token,
	}
	response_user_info = requests.get('https://api.intra.42.fr/v2/me', headers=headers)
	if response_user_info.status_code != 200:
			return HttpResponseRedirect(redirect_to='/signup#failedToGetUserInfo')
	data_user_info = response_user_info.json()
	login = data_user_info['login']
	email = data_user_info['email']
	random_password = base64.urlsafe_b64encode(os.urandom(16)).decode('utf-8')
	if User.objects.filter(name=login, email=email).first():
		return HttpResponseRedirect(redirect_to='/signup#userAlreadyExists')
	user = User.objects.create_user(name=login, email=email, password=random_password)
	return create_token_response(user.uuid, HttpResponseRedirect(redirect_to='/home'))
