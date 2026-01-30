from flask import Blueprint, render_template, redirect, url_for, flash, abort, request
from flask_login import login_required, current_user
from app.db_models import db, Item, Order
from .forms import ItemForm
import csv
import os
from werkzeug.utils import secure_filename

admin = Blueprint(
    "admin", __name__, template_folder="templates", static_folder="static"
)

UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), "..", "static", "uploads")
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "gif"}


@admin.before_request
@login_required
def restrict_access():
    if not current_user.admin:
        abort(403)


@admin.route("/dashboard")
def dashboard():
    items = Item.query.all()
    orders = Order.query.order_by(Order.date.desc()).all()
    return render_template("admin/dashboard.html", items=items, orders=orders)


@admin.route("/add-item", methods=["GET", "POST"])
def add_item():
    form = ItemForm()
    if form.validate_on_submit():
        image_filename = form.image.data

        # Handle image upload if provided
        if "image" in request.files:
            image = request.files["image"]
            if (
                image
                and "." in image.filename
                and image.filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS
            ):
                filename = secure_filename(image.filename)
                if not os.path.exists(UPLOAD_FOLDER):
                    os.makedirs(UPLOAD_FOLDER)
                image.save(os.path.join(UPLOAD_FOLDER, filename))
                image_filename = filename

        new_item = Item(
            name=form.name.data,
            price=form.price.data,
            category=form.category.data,
            image=image_filename,
            details=form.details.data,
            price_id=form.price_id.data,
        )
        db.session.add(new_item)
        db.session.commit()
        flash("Item added successfully.", "success")
        return redirect(url_for("admin.dashboard"))
    return render_template("admin/add.html", form=form, title="Add Item")


@admin.route("/edit-item/<int:item_id>", methods=["GET", "POST"])
def edit_item(item_id):
    item = Item.query.get_or_404(item_id)
    form = ItemForm(obj=item)
    if form.validate_on_submit():
        item.name = form.name.data
        item.price = form.price.data
        item.category = form.category.data
        item.image = form.image.data
        item.details = form.details.data
        item.price_id = form.price_id.data
        db.session.commit()
        flash("Item updated successfully.", "success")
        return redirect(url_for("admin.dashboard"))
    return render_template("admin/add.html", form=form, title="Edit Item")


@admin.route("/delete-item/<int:item_id>")
def delete_item(item_id):
    item = Item.query.get_or_404(item_id)
    db.session.delete(item)
    db.session.commit()
    flash("Item deleted.", "success")
    return redirect(url_for("admin.dashboard"))
