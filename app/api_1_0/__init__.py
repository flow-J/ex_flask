# coding: utf-8
__author__ = 'flow'
from flask import Blueprint


api = Blueprint('api', __name__)


# import了各种py文件
from . import authentication, posts, users, comments, errors
