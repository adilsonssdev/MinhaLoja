# MiniLoja-shop

A modern E-Commerce application built with Python Flask, featuring a premium responsive UI and robust functionality.

![MiniLoja](https://via.placeholder.com/800x400?text=MiniLoja+Preview)

## Features

- **Modern UI/UX**: Responsive design using Bootstrap 5 and custom CSS.
- **Shopping Cart**: Full-fledged cart system with quantity adjustment.
- **User System**: Secure authentication (Login/Register) with email confirmation support.
- **Order Management**: Users can view their order history and status.
- **Admin Panel**: For managing products and orders.
- **Payment Integration**: Stripe checkout integration.
- **Search**: Real-time product search functionality.

## Prerequisites

- Python 3.8+
- [Stripe Account](https://stripe.com) (for payment testing)

## Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/diwash007/Flask-O-shop.git 
   cd MiniLoja-shop
   ```

2. **Create a Virtual Environment (Recommended):**
   ```bash
   # Windows
   python -m venv venv
   venv\Scripts\activate

   # Linux/Mac
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Environment Setup:**
   Create a `.env` file in the root directory (copy from `env-example.txt` if available) and add your configuration:
   ```env
   SECRET_KEY=your_secret_key
   DB_URI="sqlite:///shop.db"
   EMAIL=your_email@gmail.com
   PASSWORD=your_app_password
   STRIPE_PUBLIC=pk_test_...
   STRIPE_PRIVATE=sk_test_...
   ENDPOINT_SECRET=whsec_...
   ```
   > **Note:** For development, you can use dummy values for email and stripe if you are just testing the UI.

5. **Initialize Database:**
   The application automatically creates the database tables on first run (in `app.py`).

## Running the Application

```bash
python app.py
```
Open your browser and visit `http://127.0.0.1:5000`.

## License

MIT
