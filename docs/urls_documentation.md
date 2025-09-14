# URL Configuration Changes and Available Template URLs

This document outlines the recent changes to the URL configuration and lists the URLs that serve HTML templates.

## URL Changes

The following changes have been made to the URL structure:

- The `/web/inventory/` prefix for inventory-related URLs has been removed. Inventory URLs are now directly accessible under `/inventory/`.
- The `/catalog/` URL, which was previously accessible under `/web/inventory/catalog/`, is now directly accessible at the root level as `/catalog/`.

## Available Template URLs

The following URLs serve HTML templates:

- **`/inventory/`**: Displays the product list (from `apps/inventory/views.py` `product_list` view, using `templates/inventory/product_list.html`).
- **`/inventory/add/`**: (Assuming this is part of inventory.urls) For adding new products (likely using `templates/inventory/product_add.html`).
- **`/inventory/edit/<int:pk>/`**: (Assuming this is part of inventory.urls) For editing existing products (likely using `templates/inventory/product_edit.html`).
- **`/inventory/delete/<int:pk>/`**: (Assuming this is part of inventory.urls) For deleting products (likely using `templates/inventory/product_confirm_delete.html`).
- **`/catalog/`**: Displays the product catalog (from `apps/inventory/views.py` `catalog` view, using `adap/catalogo.html`).
- **`/`**: (Assuming this is the main index page) Likely serves `adap/index.html`.
- **`/login/`**: (Assuming this is the login page) Likely serves `adap/login.html`.
- **`/clientes/`**: (Assuming this is the clients page) Likely serves `adap/clientes.html`.
- **`/compras/`**: (Assuming this is the purchases page) Likely serves `adap/compras.html`.
- **`/proveedores/`**: (Assuming this is the suppliers page) Likely serves `adap/proveedores.html`.
- **`/ventas/`**: (Assuming this is the sales page) Likely serves `adap/ventas.html`.
