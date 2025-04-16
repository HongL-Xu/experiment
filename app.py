from flask import Flask, request, jsonify, send_from_directory, render_template_string
from database import Database
from datetime import datetime

app = Flask(__name__, static_folder='static')
app.config['DATABASE'] = 'hay.db'  # Default database path

def get_db():
    """Get a database instance using the current configuration."""
    return Database(app.config['DATABASE'])

@app.route('/')
def serve_index():
    db = get_db()
    years = db.get_available_years()
    return render_template_string('''
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>HAY Donation Manager</title>
            <link rel="stylesheet" href="/static/styles.css">
            <link href="https://fonts.googleapis.com/css2?family=Encode+Sans:wght@400;500;700&display=swap" rel="stylesheet">
        </head>
        <body>
            <header class="header">
                <div class="header__logo">
                    <img src="/static/uw-logo-gold.png" alt="UW Logo" class="header__logo-image">
                </div>
                <h1 class="header__title">HAY Donation Manager</h1>
            </header>

            <main class="main">
                <div class="controls">
                    <div class="controls__filter">
                        <label for="yearFilter" class="controls__label">Filter by Year:</label>
                        <select id="yearFilter" class="controls__select">
                            <option value="">All Years</option>
                            {% for year in years %}
                            <option value="{{ year }}">{{ year }}</option>
                            {% endfor %}
                        </select>
                    </div>
                    <div class="controls__actions">
                        <button id="refreshBtn" class="button button--secondary">Refresh Data</button>
                        <button id="addDonationBtn" class="button button--primary">Add Donation</button>
                    </div>
                </div>

                <div class="table-container">
                    <table id="donationsTable" class="table">
                        <thead>
                            <tr>
                                <th>Donor Name</th>
                                <th>Amount</th>
                                <th>Date</th>
                                <th>Note</th>
                                <th>Actions</th>
                            </tr>
                        </thead>
                        <tbody id="donationsTableBody">
                            <!-- Table rows will be dynamically added here -->
                        </tbody>
                    </table>
                </div>

                <!-- Add Donation Form Modal -->
                <div id="addDonationModal" class="modal">
                    <div class="modal__content">
                        <h2 class="modal__title">Add New Donation</h2>
                        <form id="addDonationForm" class="form">
                            <div class="form__group">
                                <label for="donorName" class="form__label">Donor Name:</label>
                                <input type="text" id="donorName" name="donorName" required class="form__input">
                            </div>
                            <div class="form__group">
                                <label for="amount" class="form__label">Amount:</label>
                                <input type="number" id="amount" name="amount" step="0.01" required class="form__input">
                            </div>
                            <div class="form__group">
                                <label for="date" class="form__label">Date:</label>
                                <input type="date" id="date" name="date" required class="form__input">
                            </div>
                            <div class="form__group">
                                <label for="note" class="form__label">Note:</label>
                                <textarea id="note" name="note" class="form__input"></textarea>
                            </div>
                            <div class="form__actions">
                                <button type="submit" class="button button--primary">Save</button>
                                <button type="button" class="button button--secondary" onclick="closeModal()">Cancel</button>
                            </div>
                        </form>
                    </div>
                </div>
            </main>

            <script src="/static/app.js"></script>
        </body>
        </html>
    ''', years=years)

@app.route('/api/years')
def get_years():
    """Get all available years from the database."""
    db = get_db()
    years = db.get_available_years()
    return jsonify(years)

@app.route('/api/donations', methods=['GET'])
def get_donations():
    db = get_db()
    year = request.args.get('year', type=int)
    if year:
        donations = db.get_donations_by_year(year)
    else:
        donations = db.get_all_donations()
    return jsonify(donations)

@app.route('/api/donations', methods=['POST'])
def add_donation():
    db = get_db()
    data = request.json
    try:
        donation_id = db.add_donation(
            donor_name=data['donorName'],
            amount=float(data['amount']),
            date=data['date'],
            note=data.get('note', '')
        )
        return jsonify({'id': donation_id}), 201
    except (KeyError, ValueError) as e:
        return jsonify({'error': str(e)}), 400

@app.route('/api/donations/<int:donation_id>', methods=['PUT'])
def update_donation(donation_id):
    db = get_db()
    data = request.json
    try:
        success = db.update_donation(
            donation_id=donation_id,
            donor_name=data['donorName'],
            amount=float(data['amount']),
            date=data['date'],
            note=data.get('note', '')
        )
        if success:
            return jsonify({'message': 'Updated successfully'})
        return jsonify({'error': 'Donation not found'}), 404
    except (KeyError, ValueError) as e:
        return jsonify({'error': str(e)}), 400

@app.route('/api/donations/<int:donation_id>', methods=['DELETE'])
def delete_donation(donation_id):
    db = get_db()
    success = db.delete_donation(donation_id)
    if success:
        return jsonify({'message': 'Deleted successfully'})
    return jsonify({'error': 'Donation not found'}), 404

if __name__ == '__main__':
    app.run(debug=True) 