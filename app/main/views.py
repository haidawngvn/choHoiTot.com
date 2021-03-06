from datetime import datetime
import os
from flask import render_template, redirect, url_for, flash, request

from ..models import Bill, Favourite, Product, User
from .forms import AddForm, SearchForm, UpdateForm
from .. import db
from flask_login import login_required, current_user
from . import main
from ..email import send_email
from werkzeug.utils import secure_filename



@main.route('/')
@main.route('/home')
def home_page():
    return render_template("home.html")

@main.route('/chotot/<category>', methods=['GET', 'POST'])
#@login_required             #yêu cầu user phải đăng nhập mới được vô trang market ==> file init phải có thêm dòng 13,14
def chotot_page(category):
    addForm = AddForm()
    searchForm = SearchForm()
    if current_user.is_authenticated:
        user = current_user
    else:
        user = User()

    if request.method == 'POST':
        select = request.form.get('sort')
        if category == "all" or category == 'Tất cả':
            category = 'Tất cả'
            if select == 'date':
                products = Product.query.filter(Product.status =='SELLING', 
                                                Product.owner_id != user.id
                                                ).order_by(Product.date.desc()).all() 
            elif select == 'price_az':
                products = Product.query.filter(Product.status =='SELLING', 
                                                Product.owner_id != user.id
                                                ).order_by(Product.price).all() 
            elif select == 'price_za':
                products = Product.query.filter(Product.status =='SELLING', 
                                                Product.owner_id != user.id
                                                ).order_by(Product.price.desc()).all() 
            elif select == 'name_az':
                products = Product.query.filter(Product.status =='SELLING', 
                                                Product.owner_id != user.id
                                                ).order_by(Product.name).all() 
            elif select == 'name_za':
                products = Product.query.filter(Product.status =='SELLING', 
                                                Product.owner_id != user.id
                                                ).order_by(Product.name.desc()).all() 
            else:
                products = Product.query.filter(Product.status =='SELLING', 
                                                Product.owner_id != user.id
                                                ).order_by(Product.date.desc()).all()
            # products = Product.query.filter(Product.status =='SELLING', 
            #                             Product.owner_id != user.id
            #                             ).order_by(Product.date.desc()).all() 
        else:    
            if select == 'date':
                products = Product.query.filter(Product.status =='SELLING', 
                                                Product.owner_id != user.id,
                                                Product.category == category,
                                                ).order_by(Product.date.desc()).all() 
            elif select == 'price_az':
                products = Product.query.filter(Product.status =='SELLING', 
                                                Product.owner_id != user.id,
                                                Product.category == category,
                                                ).order_by(Product.price).all() 
            elif select == 'price_za':
                products = Product.query.filter(Product.status =='SELLING', 
                                                Product.owner_id != user.id,
                                                Product.category == category,
                                                ).order_by(Product.price.desc()).all() 
            elif select == 'name_az':
                products = Product.query.filter(Product.status =='SELLING', 
                                                Product.owner_id != user.id,
                                                Product.category == category,
                                                ).order_by(Product.name).all() 
            elif select == 'name_za':
                products = Product.query.filter(Product.status =='SELLING', 
                                                Product.owner_id != user.id,
                                                Product.category == category,
                                                ).order_by(Product.name.desc()).all() 
            else:
                products = Product.query.filter(Product.status =='SELLING', 
                                                Product.owner_id != user.id,
                                                Product.category == category,
                                                ).order_by(Product.date.desc()).all()
            # products = Product.query.filter(Product.status =='SELLING', 
            #                             Product.owner_id != user.id,
            #                             Product.category == category).order_by(Product.date.desc()).all()    
        return render_template('market/chotot.html', 
                                products = products, 
                                category = category,
                                addForm= addForm, 
                                searchForm=searchForm)
    
    if request.method == 'GET':
        if category == "all" or category == 'Tất cả':
            category = 'Tất cả'
            products = Product.query.filter(Product.status =='SELLING', 
                                        Product.owner_id != user.id
                                        ).order_by(Product.date.desc()).all() 
        else:    
            products = Product.query.filter(Product.status =='SELLING', 
                                        Product.owner_id != user.id,
                                        Product.category == category).order_by(Product.date.desc()).all()    #return all the items in the db MÀ CHƯA CÓ OWNER
        return render_template('market/chotot.html', 
                                products = products, 
                                category = category,
                                addForm= addForm, 
                                searchForm=searchForm)


@main.route('/go2search', methods=['POST','GET'])
def go2search():
    searchForm = SearchForm()
    if request.method == 'POST':
        if searchForm.keyword.data:
            return redirect(url_for('main.search', type = 'products', keyword = searchForm.keyword.data))

@main.route('/search/<type>/<keyword>', methods=['POST','GET'])
def search(type, keyword):
    form = SearchForm()
    addForm = AddForm()
    if current_user.is_authenticated:
        user = current_user
    else:
        user = User()
    
    products = []
    
    select = request.form.get('sort')
    if select == 'date':
        all_products = Product.query.filter(Product.status =='SELLING', 
                                        Product.owner_id != user.id
                                        ).order_by(Product.date.desc()).all() 
    elif select == 'price_az':
        all_products = Product.query.filter(Product.status =='SELLING', 
                                        Product.owner_id != user.id
                                        ).order_by(Product.price).all() 
    elif select == 'price_za':
        all_products = Product.query.filter(Product.status =='SELLING', 
                                        Product.owner_id != user.id
                                        ).order_by(Product.price.desc()).all() 
    elif select == 'name_az':
        all_products = Product.query.filter(Product.status =='SELLING', 
                                        Product.owner_id != user.id
                                        ).order_by(Product.name).all() 
    elif select == 'name_za':
        all_products = Product.query.filter(Product.status =='SELLING', 
                                        Product.owner_id != user.id
                                        ).order_by(Product.name.desc()).all() 
    else:
        all_products = Product.query.filter(Product.status =='SELLING', 
                                        Product.owner_id != user.id
                                        ).order_by(Product.date.desc()).all()

    
    # all_products = Product.query.filter(Product.status =='SELLING', 
    #                                 Product.owner_id != user.id,
    #                                 ).order_by(Product.date.desc()).all()
    for product in all_products:
        if keyword.strip() in product.name:
            products.append(product)
    
    users = []
    all_users = User.query.order_by(User.id.desc()).all()
    for user_qualified in all_users:
        if keyword.strip() in user_qualified.user_name and user_qualified.id != user.id:
            users.append(user_qualified)

    return render_template('market/search.html', 
                            user=user,
                            type = type,
                            keyword = keyword, 
                            products = products,
                            users = users,
                            form = form,
                            addForm = addForm
                            )

@main.route('/product_detail/<product_id>', methods=['GET', 'POST'])
def detail_page(product_id):
    if current_user.is_authenticated:
        user = current_user
    else:
        user = User()
    product = Product.query.filter_by(id=product_id).first()
    owner = User.query.filter_by(id=product.owner_id).first()
    favourite = Favourite.query.filter_by(product_id=product.id, user_id = user.id).first()
    others = Product.query.filter(Product.category == product.category,
                                Product.owner_id != user.id,
                                Product.status == 'SELLING',
                                Product.id != product.id).limit(5).all()
    return render_template('market/product_detail.html', 
                            product = product , 
                            owner = owner, 
                            others = others,
                            favourite = favourite
                            )

@main.route('/product_owned', methods=['POST','GET'])
@login_required
def product_owned():
    current_user.update_last_seen()
    form = UpdateForm()
    user = User.query.filter_by(id = current_user.id).first_or_404()
    products = Product.query.filter(Product.status =='OWNED', 
                                    Product.owner_id == user.id
                                    ).order_by(Product.date.desc()).all() 
    number_of_products = len(products)
    return render_template('market/product_owned.html', 
                            user=user, 
                            products = products, 
                            form = form,
                            number_of_products = number_of_products)

@main.route('/like_page', methods=['POST','GET'])
@login_required
def like_page():
    current_user.update_last_seen()
    user = current_user
    liked_products_id = Favourite.query.filter_by(user_id = user.id).order_by(Favourite.id.desc()).all() 
    products = []
    for liked_product_id in liked_products_id:
        product = Product.query.filter_by(id = liked_product_id.product_id, status = 'SELLING').first() 
        products.append(product)
    for product in products:
        if not product:
            products.remove(product)
    number_of_products = len(products)
    return render_template('market/product_liked.html', 
                            user=user, 
                            products = products, 
                            number_of_products = number_of_products)

@main.route('/bills', methods=['POST','GET'])
@login_required
def bills():
    current_user.update_last_seen()
    user = User.query.filter_by(id = current_user.id).first_or_404()
    bills = Bill.query.filter_by(user_id = user.id).order_by(Bill.id.desc()).all() 
    number_of_bills = len(bills)
    others = []
    for bill in bills:
        other = User.query.filter_by(id = bill.other_id).first_or_404()
        others.append(other)
    return render_template('market/bills.html', 
                            user=user, 
                            bills = bills, 
                            others = others,
                            number_of_bills = number_of_bills)

@main.route('/purchase/<product_id>', methods=['POST','GET'])
@login_required
def purchase(product_id):
    # Purchase function
    if request.method == 'POST':
        product = Product.query.filter_by(id = product_id, status= 'SELLING').first()
        if product:
            if current_user.can_purchase(product):
                user = current_user
                token = user.generate_confirmation_token()      
                send_email(user.user_email, 'mail/confirm_purchase', user=user, token=token, product=product)
                flash("Email xác thực cho giao dịch này đã được gửi đến hộp thư của bạn! ", category='success')    
            else:
                flash(f"Số dư trong tài khoản của bản không đủ để mua {product.name}!", category='danger')
        else:
            flash('Không thể mua sản phẩm này! Xin thử lại sau! ', category='danger')
    return redirect(url_for('main.detail_page', product_id=product_id))

@main.route('/confirm_email/<product_id>/<token>')
@login_required
def confirm_purchase(product_id,token):
    if current_user.confirm(token) == 'TRUE':
        product = Product.query.filter_by(id = product_id).first()
        old_owner = User.query.filter_by(id=product.owner_id).first()
        if product.purchase(current_user) == True:
            buyer_bill = Bill(type = 'Hóa Đơn Mua Hàng',
                            date = datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
                            product_name = product.name,
                            total = prettier_budget(product.price) + " đồng",
                            other_id = old_owner.id,
                            user_id = current_user.id)
            seller_bill = Bill(type = 'Hóa Đơn Bán Hàng',
                            date = datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
                            product_name = product.name,
                            total = prettier_budget(product.price) + " đồng",
                            other_id = current_user.id,
                            user_id = old_owner.id)
            db.session.add(buyer_bill)
            db.session.add(seller_bill)
            db.session.commit()
            send_email(current_user.user_email, 'mail/purchase_success_buyer', user=current_user, product=product, owner = old_owner, bill = buyer_bill)
            send_email(old_owner.user_email, 'mail/purchase_success_seller', user=current_user, product=product, owner = old_owner, bill = seller_bill)
    elif current_user.confirm(token) == 'TOUCHED':
        flash('Link xác nhận mua hàng không hợp lệ. ', category='danger')
    elif current_user.confirm(token) == 'EXPIRED':
        flash('Link xác nhận mua hàng đã hết thời hạn. ', category='danger')
    else:
        flash('Đã xảy ra lỗi khi xác thực giao dịch.', category='danger')
    return redirect(url_for('main.chotot_page', category='all'))

@main.route('/like/<product_id>', methods=['POST','GET'])
@login_required
def like(product_id):
    current_user.update_last_seen()
    user = current_user
    favourite = Favourite.query.filter_by(product_id=product_id, user_id = user.id).first()
    if favourite:
        db.session.delete(favourite)
    else:
        new_favourite = Favourite(product_id = product_id, user_id = user.id)
        db.session.add(new_favourite)
    db.session.commit()
    return redirect(url_for('main.detail_page', product_id=product_id))


ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])

def allowed_file(filename):
	return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@main.route('/add', methods=['GET', 'POST'])
@login_required
def add():
    addForm = AddForm()
    if request.method == 'POST':
        file =addForm.file.data#First grab the file
        if (addForm.price.data.isnumeric() == False):
            flash('Hãy nhập giá tiền hợp lệ !!', category='danger')
        elif allowed_file(file.filename) == False:
            flash(f'File ảnh không hợp lệ!', category='danger')
        else:
            add_product = Product(description=addForm.description.data,
                            date = datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
                            name=addForm.name.data,
                            price=addForm.price.data,
                            category=addForm.category.data,
                            owner_id=current_user.id)
            db.session.add(add_product)
            db.session.commit()
            file.filename = f"{add_product.id}."+ file.filename.rsplit('.', 1)[1].lower()
            file.save(os.path.join(os.path.abspath(os.path.dirname(__file__)), '../../static/product', secure_filename(file.filename)))#Then save the file
            add_product.image = f"{add_product.id}."+ file.filename.rsplit('.', 1)[1].lower()
            db.session.commit()
            flash(f'Sản phẩm {addForm.name.data} đã được đăng bán thành công !!' , category='success')
    return redirect(url_for('main.chotot_page', category='all'))

@main.route('/update/<product_id>', methods=['GET', 'POST'])
@login_required
def update(product_id):
    form = UpdateForm()
    haveChange = False
    product = Product.query.filter_by(id = product_id).first()
    if request.method == 'POST':
        if form.name.data :
            product.name = form.name.data
            haveChange = True
        if form.price.data :
            if (form.price.data.isnumeric() == False):
                flash('Hãy nhập giá tiền hợp lệ !!', category='danger')
                return redirect(url_for('profile.profile_page', id=current_user.id))
            else:
                product.price = form.price.data
                haveChange = True
        if form.description.data :
            product.description = form.description.data
            haveChange = True
        if form.file.data:
            file = form.file.data
            if allowed_file(file.filename) == False:
                flash(f'File ảnh không hợp lệ!', category='danger')
            else:
                file.filename = f"{product.id}."+ file.filename.rsplit('.', 1)[1].lower()
                file.save(os.path.join(os.path.abspath(os.path.dirname(__file__)), '../../static/product', secure_filename(file.filename)))#Then save the file
                product.image = f"{product.id}."+ file.filename.rsplit('.', 1)[1].lower()
                haveChange = True
        if form.category.data != '...':
            product.category = form.category.data
            haveChange = True
        if haveChange == True:
            db.session.commit()
            flash('Thông tin sản phẩm đã được cập nhật thành công !', category='success')
        elif haveChange == False:
            flash('Hãy điền các trường thông tin mà bạn muốn cập nhật!', category='info')
    return redirect(url_for('profile.profile_page', id=current_user.id))

@main.route('/resell/<product_id>', methods=['GET', 'POST'])
@login_required
def resell(product_id):
    form = UpdateForm()
    product = Product.query.filter_by(id = product_id).first()
    if request.method == 'POST':
        if form.name.data :
            product.name = form.name.data
        if form.price.data :
            if (form.price.data.isnumeric() == False):
                flash('Hãy nhập giá tiền hợp lệ !!', category='danger')
                return redirect(url_for('main.product_owned'))
            else:
                product.price = form.price.data
        if form.description.data :
            product.description = form.description.data
        if form.file.data:
            file = form.file.data
            if allowed_file(file.filename) == False:
                flash(f'File ảnh không hợp lệ!', category='danger')
            else:
                file.filename = f"{product.id}."+ file.filename.rsplit('.', 1)[1].lower()
                file.save(os.path.join(os.path.abspath(os.path.dirname(__file__)), '../../static/product', secure_filename(file.filename)))#Then save the file
                product.image = f"{product.id}."+ file.filename.rsplit('.', 1)[1].lower()
        if form.category.data != '...':
            product.category = form.category.data
        product.date = datetime.now().strftime("%d/%m/%Y %H:%M:%S")         #lúc đăng bán thì chuyển lại date thành ngày đăng bán
        product.status = 'SELLING'
        db.session.commit()
        flash('Sản phẩm đã được đăng bán thành công !', category='success')

    return redirect(url_for('main.product_owned'))


@main.route('/delete/<product_id>', methods=['POST','GET'])
@login_required
def delete(product_id):
    product = Product.query.filter_by(id = product_id).first()
    if request.method == 'POST':
        if product:
            db.session.delete(product)
            db.session.commit()
            flash('Sản phẩm đã xóa thành công!', category='success')
        else:
            flash('Không thể xóa sản phẩm!', category='danger')
    return redirect(url_for('profile.profile_page', id=current_user.id))
    

def prettier_budget(budget):
        if len(str(budget)) >= 4:
            return '{:,}'.format(budget)
        else:
            return f"{budget}"