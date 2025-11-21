# 🍃 GreenShelf - Combating Food Waste

![Python](https://img.shields.io/badge/Python-3.x-blue?style=for-the-badge&logo=python)
![Flask](https://img.shields.io/badge/Flask-3.x-lightgrey?style=for-the-badge&logo=flask)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-Neon-336791?style=for-the-badge&logo=postgresql)
![Vercel](https://img.shields.io/badge/Vercel-Deploy-000000?style=for-the-badge&logo=vercel)
![JavaScript](https://img.shields.io/badge/JavaScript-ES6-yellow?style=for-the-badge&logo=javascript)

**GreenShelf** is a full-stack web application developed as a university extension project. Its main objective is to combat food waste by connecting small local businesses with consumers to sell products nearing their expiration date at reduced prices.

This project is aligned with the UN **SDG 12 (Responsible Consumption and Production)**, promoting economic and environmental sustainability in the community of Altamira, PA.

***

## 🎯 The Problem It Solves

Food waste is a global challenge that affects both the economy and the environment. Small businesses often discard products that are still fit for consumption simply because they are close to their expiration date, while consumers are looking for ways to save money.

**GreenShelf** was created to solve this exact problem by offering a centralized platform where businesses can quickly move this inventory and consumers can take advantage of deals, creating a cycle of conscious and sustainable consumption.

***

## ✨ Key Features

### For Merchants (Partners)
-   ✅ **Secure Registration & Login**: Robust authentication system to protect business data and account sovereignty.
-   ✅ **Management Dashboard**: Intuitive panel for full inventory control.
-   ✅ **Product Management**: Agile addition of items with detailed fields (name, original price, discounted price, expiration date, and quantity).
-   ✅ **Cloud Image Upload**: Integration with **Vercel Blob** to display real photos of products, increasing consumer trust.
-   ✅ **Profile Management**: Edit business details and location, with an account deletion feature (Data Sovereignty).

### For Consumers (Community)
-   ✅ **Offers Showcase**: Dynamic homepage that aggregates all active offers, strategically sorted by expiration date.
-   ✅ **Product Details**: Complete view with photo, price comparison, and the exact address of the business.
-   ✅ **Responsive Design**: Modern interface that adapts perfectly to mobile phones, tablets, and desktops.

***

## 🏛️ Architecture and Data Flow

The project was built using a modern "serverless" architecture, ideal for rapid deployment and low maintenance costs.

The data flow works as follows:

1.  **Data Entry**: The commercial partner logs in and registers a product and its image via the Dashboard.
2.  **Media Storage**: The image is sent and hosted on **Vercel Blob**, returning a public URL.
3.  **Data Persistence**: Product information and the image URL are saved in the **PostgreSQL** database (hosted on Neon).
4.  **Visualization**: The consumer accesses the showcase, where **Flask** queries the database and renders active offers via the template engine.

***

## 🛠️ Tech Stack

The choice of technologies focused on scalability, ease of deployment, and robustness.

-   **Back-end**:
    -   **Python**: Main language of the application.
    -   **Flask**: Web micro-framework for building routes, business logic, and session management.
    -   **PostgreSQL (Neon)**: Serverless relational database to securely store users and products.

-   **Front-end**:
    -   **HTML5 & CSS3**: Semantic structure and custom styling.
    -   **JavaScript (Vanilla)**: For client-side interactivity and DOM manipulation.

-   **Infrastructure and Files**:
    -   **Vercel Blob**: Object storage solution for product images.
    -   **Vercel**: Hosting and continuous deployment platform.

***

## 🚀 Installation and Local Execution

Follow the steps below to set up and run the project in your local environment.

1.  **Clone the repository:**
    ```bash
    git clone [https://github.com/MCTHIAS/GreenShelf.git](https://github.com/MCTHIAS/GreenShelf.git)
    cd GreenShelf
    ```

2.  **Create and activate a virtual environment:**
    ```bash
    # Windows
    python -m venv venv
    venv\Scripts\activate

    # macOS/Linux
    python3 -m venv venv
    source venv/bin/activate
    ```

3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Configure Environment Variables:**
    Create a `.env` file in the project root and add the following variables:

    ```env
    # Key for Flask session security
    SECRET_KEY="your_secret_key_for_flask_session"

    # Neon database connection URL
    POSTGRES_URL="url_of_your_neon_postgres_db"

    # Token for image uploads
    BLOB_READ_WRITE_TOKEN="your_vercel_blob_token"
    ```

5.  **Run the application:**
    ```bash
    flask run
    ```
    Access `http://127.0.0.1:5000` in your browser.

***

## 🤝 Contribution

This is an academic extension project. Suggestions, feedback, and contributions are very welcome! Feel free to open an "issue" or submit a "pull request".

***
