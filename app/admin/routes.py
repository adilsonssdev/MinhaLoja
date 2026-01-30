from flask import Blueprint, render_template, redirect, url_for, flash, abort, request
from flask_login import login_required, current_user
from app.db_models import db, Item, Order
from .forms import ItemForm
import csv

admin = Blueprint(
    "admin", __name__, template_folder="templates", static_folder="static"
)


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
        new_item = Item(
            name=form.name.data,
            price=form.price.data,
            category=form.category.data,
            image=form.image.data,
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


@admin.route("/admin/add_product", methods=["GET", "POST"])
@login_required
def add_product():
    if not current_user.is_admin:
        flash(
            "Acesso negado: apenas administradores podem acessar esta página.", "danger"
        )
        return redirect(url_for("home"))

    if request.method == "POST":
        product_name = request.form.get("product_name")
        product_value = request.form.get("product_value")

        # Aqui você pode adicionar lógica para salvar o produto no banco de dados
        flash(f"Produto {product_name} adicionado com sucesso!", "success")
        return redirect(url_for("admin_dashboard"))

    return render_template("admin/add_product.html")


@admin.route("/admin/import_admins", methods=["GET", "POST"])
@login_required
def import_admins():
    if not current_user.is_admin:
        flash(
            "Acesso negado: apenas administradores podem acessar esta página.", "danger"
        )
        return redirect(url_for("home"))

    if request.method == "POST":
        file = request.files.get("file")
        if not file:
            flash("Nenhum arquivo foi enviado.", "danger")
            return redirect(url_for("import_admins"))

        try:
            csv_reader = csv.DictReader(file.stream)
            for row in csv_reader:
                # Aqui você pode adicionar lógica para salvar o administrador no banco de dados
                # Exemplo: User.create_admin(row['email'], row['name'])
                flash(
                    f"Administrador {row['name']} ({row['email']}) adicionado com sucesso!",
                    "success",
                )
        except Exception as e:
            flash(f"Erro ao processar o arquivo: {str(e)}", "danger")

        return redirect(url_for("admin_dashboard"))

    return render_template("admin/import_admins.html")
