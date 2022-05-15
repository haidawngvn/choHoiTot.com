from datetime import datetime
from unicodedata import name
from flask import render_template, redirect, url_for, flash, request, session

from ..models import Product, User
from .forms import AddForm, Go2ProductDetailForm, PurchaseForm, SearchForm
from .. import db
from flask_login import login_required, current_user
from . import main
from ..email import send_email, send_congrat_email


@main.route('/')
@main.route('/home')
def home_page():
    return render_template("home.html")

@main.route('/chotot/<category>', methods=['GET', 'POST'])
@login_required             #yêu cầu user phải đăng nhập mới được vô trang market ==> file init phải có thêm dòng 13,14
def chotot_page(category):
    purchaseForm = PurchaseForm()
    addForm = AddForm()
    go2ProductDetailForm = Go2ProductDetailForm()
    searchForm = SearchForm()
    stuId = ""
    if request.method == 'POST':
        # student_to_search = Student.query.filter_by(student_id=(searchForm.keyword.data).strip(),student_owner=None).first()
        # if student_to_search:
        #     stuId = (searchForm.keyword.data).strip()
        # else:
        #     flash(f"Student Not Found !!", category='danger')
        
        # students = Student.query.filter_by(student_owner=None, student_id=stuId)    #return all the items in the db MÀ CHƯA CÓ OWNER
        # owned_students = Student.query.filter_by(student_owner=current_user.id) 
        return render_template('market/chotot.html', 
                                # students=students, 
                                # owned_students = owned_students, 
                                purchaseForm=purchaseForm, 
                                go2ProductDetailForm = go2ProductDetailForm,
                                addForm= addForm, 
                                searchForm=searchForm)

    if request.method == 'GET':
        products = Product.query.filter_by(owner_id=None)    #return all the items in the db MÀ CHƯA CÓ OWNER
        # owned_students = Student.query.filter_by(student_owner=current_user.id) 
        return render_template('market/chotot.html', 
                                products = products, 
                                # owned_students = owned_students, 
                                purchaseForm=purchaseForm, 
                                go2ProductDetailForm = go2ProductDetailForm,
                                addForm= addForm, 
                                searchForm=searchForm)

@main.route('/product_detail/<product_id>', methods=['GET', 'POST'])
def detail_page(product_id):
    addForm = AddForm()
    if product_id:
        product = Product.query.filter_by(id=product_id).first()
    return render_template('market/product_detail.html', product = product)
    

@main.route('/purchase', methods=['POST'])
@login_required
def purchase():
    if request.method == 'POST':
        if 'last_purchase_submit' in session:
            last_submit = session['last_purchase_submit']
            timestamp = datetime.strptime(last_submit, '%d/%m/%Y %H:%M:%S')
            duration_in_second = (datetime.now() - timestamp).total_seconds()
            if (duration_in_second > 300):
                current_user.user_status = True
                db.session.commit()
        if current_user.user_status == False:
            flash("Một giao dịch khác đang được thực hiện, hãy thử lại sau !", category='info')
        else:
        # Purchase function
            purchased_item = request.form.get('purchased_item')      #này chỉ lấy tên của item được bấm mua (này là name trong purchase model)
            # student_obj = Student.query.filter_by(student_id=purchased_item).first()   #dùng tên lấy ra item obj trong db
            # if student_obj:
            #     if current_user.can_purchase(student_obj):
            #         user = current_user
            #         if user is not None :
            #             user.user_status = False
            #             session['last_purchase_submit'] = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
            #             db.session.commit()
            #             token = user.generate_confirmation_token()          
            #             send_email(user.user_email, 'mail/confirm_email', user=user, token=token, student=student_obj)
            #             flash("Please check your email to confirm your purchase. ", category='success')
            #     else:
            #         flash(f"Unfortunately, you don't have enough money to paid for {student_obj.student_id} tuition!", category='danger')
    return redirect(url_for('main.chotot_page', category='products'))

@main.route('/confirm_email/<student_id>/<token>')
@login_required
def confirm_email(student_id,token):
    if current_user.confirm(token) == 'TRUE':
        current_user.user_status = True
        db.session.commit()
        # student_obj = Student.query.filter_by(student_id=student_id).first()   #dùng tên lấy ra item obj trong db
        # if student_obj.purchase(current_user) == True:
        #     mail_body = f"Congratulations! You just paid {student_obj.student_id} tuition for {student_obj.student_tuition}$"
            # send_congrat_email(current_user.user_email, mail_body)
    elif current_user.confirm(token) == 'TOUCHED':
        flash('Link xác nhận mua hàng không hợp lệ. ', category='danger')
    elif current_user.confirm(token) == 'EXPIRED':
        current_user.user_status = True
        db.session.commit()
        flash('Link xác nhận mua hàng đã hết thời hạn. ', category='danger')
    else:
        flash('Ôi không...', category='danger')
    return redirect(url_for('main.chotot_page', category='products'))

@main.route('/add', methods=['GET', 'POST'])
@login_required
def add():
    addForm = AddForm()
    if request.method == 'POST':
        product_to_add = Product.query.filter_by(name=addForm.name.data).first()
        if product_to_add:
            flash('Tên sản phẩm này đã tồn tại !!', category='danger')
        elif (addForm.price.data.isnumeric() == False):
            flash('Hãy nhập giá tiền hợp lệ !!', category='danger')
        else:
            add_product = Product(description=addForm.description.data,
                            name=addForm.name.data,
                            price=addForm.price.data,
                            category=addForm.category.data)
            db.session.add(add_product)
            db.session.commit()
            flash(f'Sản phẩm {addForm.name.data} đã được đăng bán thành công !!' , category='success')
    return redirect(url_for('main.chotot_page', category='products'))


def prettier_budget(budget):
        if len(str(budget)) >= 4:
            return '{:,}'.format(budget)
        else:
            return f"{budget}"