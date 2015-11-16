# coding:utf-8
__author__ = 'flow'

"""
	第一个路由处理获取文章集合的请求。这个函数使用列表推导生成所有文章的 JSON 版本。
	第二个路由返回单篇博客文章， 如果在数据库中没找到指定 id 对应的文章，则返回 404
	错误.
"""
@api.route('/posts/')
@auth.login_required
def get_posts():
	posts = Post.query.all()
	return jsonify({'posts': [posts.to_json() for post in posts] })


 # 文章资源 GET 请求的处理程序
@api.route('/posts/<int:id>')
@auth.login_required
def get_post(id):
	post = Post.query.get_or_404(id)
	return jsonify(post.to_json())


 # 文章资源 POST 请求的处理程序
@api.route('/posts/', methods=['POST'])
@permission_required(Permission.WRITE_ARTICLES)
def new_porst():
	post = Post.from_json(request.json)
	post.author = g.current_user
	db.session.add(post)
	db.session.commit()
	return jsonify(post.to_json()), 201, \
		   {'Location': url_for('api.get_post', id=post.id, _external=True)}


 # 文章资源 PUT 请求的处理程序
@api.route('/posts/<int:id>', methods=['PUT'])
@permission_required(Permission.WRITE_ARTICLES)
def edit_post(id):
	post = Post.query.get_or_404(id)
	if g.current_user != post.author and \
			not g.current_user.can(Permission.ADMINISTER):
		return forbidden('Insufficient permssions')
	post.body = request.json.get('body', post.body)
	db.session.add(post)
	return jsonify(post.to_json())


 # 分页文章资源
@api.route('/posts/')
def get_posts():
	page = request.args.get('page', 1, type=int)
	pagination = Post.query.paginate(
		page, per_page=current_app.config['FLASKY_POSTS_PER_PAGE'],
		error_out=False)
	posts = pagination.items
	prev = None
	if pagination.has_prev:
		prev = url_for('api.get_posts', page=page-1, _external=True)
	next = None
	if pagination.has_next:
		next = url_for('api.get_posts', page=page+1, _external=True)
	return jsonify({
		'posts': [post.to_json() for post in posts],
		'prev': prev,
		'next': next,
		'count': pagination.total
	})
