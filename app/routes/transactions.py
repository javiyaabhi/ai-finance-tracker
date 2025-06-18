from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from app import db
from app.forms import AddTransactionForm
from app.models import Transaction

transactions = Blueprint('transactions', __name__)

@transactions.route('/transactions', methods=['GET', 'POST'])
@login_required
def manage_transactions():
    form = AddTransactionForm()
    if form.validate_on_submit():
        txn = Transaction(
            description=form.description.data,
            amount=form.amount.data,
            category=form.category.data,
            user_id=current_user.id
        )
        db.session.add(txn)
        db.session.commit()
        flash('Transaction added!', 'success')
        return redirect(url_for('transactions.manage_transactions'))

    user_txns = Transaction.query.filter_by(user_id=current_user.id).order_by(Transaction.date.desc()).all()
    return render_template('transactions.html', form=form, transactions=user_txns)
