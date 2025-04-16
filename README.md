# HAY Donation Manager

A single-page application for managing hay donations, built with Python Flask backend and vanilla JavaScript frontend.

## Features

- Track hay donations with donor information, amount, date, and notes
- CRUD operations for donations
- Filter donations by year
- Clean, responsive UI following UW Brand guidelines
- Inline editing for quick updates
- SQLite database for data persistence

## Prerequisites

- Python 3.8 or higher
- Modern web browser

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd donations_app
```

2. Create a virtual environment and activate it:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Running the Application

1. Start the Flask server:
```bash
python app.py
```

2. Open your web browser and navigate to:
```
http://localhost:5000
```

## Usage

- **View Donations**: All donations are displayed in a table format
- **Add Donation**: Click the "Add Donation" button and fill in the form
- **Edit Donation**: Click the edit (✏️) icon on any row to edit inline
- **Delete Donation**: Click the delete (🗑️) icon to remove a donation
- **Filter by Year**: Use the dropdown to filter donations by year

## Project Structure

```
donations_app/
├── app.py              # Flask application
├── database.py         # Database operations
├── requirements.txt    # Python dependencies
├── static/
│   ├── index.html     # Main HTML file
│   ├── styles.css     # CSS styles
│   ├── app.js         # Frontend JavaScript
│   └── uw-logo.png    # UW logo
└── hay.db             # SQLite database
```

## Error Handling

- Frontend errors are displayed using browser alerts
- Backend errors return appropriate HTTP status codes
- Database operations are wrapped in try-catch blocks

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details. 