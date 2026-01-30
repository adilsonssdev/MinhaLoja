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
        image_filename = "placeholder.png"

        # Priority: uploaded file > URL > placeholder
        if form.image_file.data:
            image = form.image_file.data
            print(f"DEBUG: Arquivo recebido: {image.filename}")
            
            if image and image.filename:
                # Verificar extensão
                filename = secure_filename(image.filename)
                file_ext = filename.rsplit(".", 1)[1].lower() if "." in filename else ""
                
                print(f"DEBUG: Filename seguro: {filename}, Extensão: {file_ext}")
                
                if file_ext in ALLOWED_EXTENSIONS:
                    # Criar pasta se não existir
                    if not os.path.exists(UPLOAD_FOLDER):
                        os.makedirs(UPLOAD_FOLDER)
                        print(f"DEBUG: Pasta criada: {UPLOAD_FOLDER}")
                    
                    # Salvar arquivo
                    filepath = os.path.join(UPLOAD_FOLDER, filename)
                    image.save(filepath)
                    print(f"DEBUG: Arquivo salvo em: {filepath}")
                    
                    if os.path.exists(filepath):
                        image_filename = filename
                        print(f"DEBUG: Arquivo confirmado no disco")
                    else:
                        flash("Erro ao salvar arquivo.", "error")
                        return render_template("admin/add.html", form=form, title="Add Item")
                else:
                    flash(f"Extensão não permitida. Use: {', '.join(ALLOWED_EXTENSIONS)}", "error")
                    return render_template("admin/add.html", form=form, title="Add Item")
        elif form.image_url.data:
            image_filename = form.image_url.data
            print(f"DEBUG: URL de imagem: {image_filename}")

        new_item = Item(
            name=form.name.data,
            price=form.price.data,
            category=form.category.data,
            image=image_filename,
            details=form.details.data,
            price_id=form.price_id.data or "",
        )
        db.session.add(new_item)
        db.session.commit()
        flash("Item added successfully.", "success")
        return redirect(url_for("admin.dashboard"))
    return render_template("admin/add.html", form=form, title="Add Item")


@admin.route("/edit-item/<int:item_id>", methods=["GET", "POST"])
def edit_item(item_id):
    item = Item.query.get_or_404(item_id)
    form = ItemForm()
    if form.validate_on_submit():
        item.name = form.name.data
        item.price = form.price.data
        item.category = form.category.data
        item.details = form.details.data
        item.price_id = form.price_id.data or ""

        # Handle image update if provided
        if form.image_file.data:
            image = form.image_file.data
            print(f"DEBUG: Arquivo recebido para edição: {image.filename}")
            
            if image and image.filename:
                filename = secure_filename(image.filename)
                file_ext = filename.rsplit(".", 1)[1].lower() if "." in filename else ""
                
                print(f"DEBUG: Filename seguro: {filename}, Extensão: {file_ext}")
                
                if file_ext in ALLOWED_EXTENSIONS:
                    if not os.path.exists(UPLOAD_FOLDER):
                        os.makedirs(UPLOAD_FOLDER)
                        print(f"DEBUG: Pasta criada: {UPLOAD_FOLDER}")
                    
                    filepath = os.path.join(UPLOAD_FOLDER, filename)
                    image.save(filepath)
                    print(f"DEBUG: Arquivo salvo em: {filepath}")
                    
                    if os.path.exists(filepath):
                        item.image = filename
                        print(f"DEBUG: Arquivo confirmado no disco")
                    else:
                        flash("Erro ao salvar arquivo.", "error")
                        return render_template("admin/add.html", form=form, title="Edit Item")
                else:
                    flash(f"Extensão não permitida. Use: {', '.join(ALLOWED_EXTENSIONS)}", "error")
                    return render_template("admin/add.html", form=form, title="Edit Item")
        elif form.image_url.data:
            item.image = form.image_url.data
            print(f"DEBUG: URL de imagem para edição: {item.image}")

        db.session.commit()
        flash("Item updated successfully.", "success")
        return redirect(url_for("admin.dashboard"))

    # Pre-populate form with current data
    if request.method == "GET":
        form.name.data = item.name
        form.price.data = item.price
        form.category.data = item.category
        form.details.data = item.details
        form.price_id.data = item.price_id
        # If image is a URL, show it in image_url
        if item.image and (
            item.image.startswith("http://") or item.image.startswith("https://")
        ):
            form.image_url.data = item.image
