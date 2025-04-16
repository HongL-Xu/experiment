import random
from datetime import datetime, timedelta
from database import Database

# Sample donor names
donor_names = [
    "John Smith", "Jane Doe", "Robert Johnson", "Emily Davis", "Michael Wilson",
    "Sarah Brown", "David Miller", "Jennifer Taylor", "James Anderson", "Patricia Thomas",
    "Thomas Jackson", "Linda White", "Charles Harris", "Barbara Martin", "Daniel Thompson",
    "Susan Garcia", "Joseph Martinez", "Margaret Robinson", "Paul Clark", "Nancy Rodriguez",
    "Mark Lewis", "Karen Lee", "Donald Walker", "Betty Hall", "Steven Young",
    "Dorothy Allen", "Richard King", "Lisa Wright", "Kenneth Scott", "Sandra Green",
    "Andrew Baker", "Ashley Adams", "Edward Nelson", "Kimberly Hill", "Brian Carter",
    "Michelle Mitchell", "George Turner", "Carol Phillips", "Christopher Campbell", "Ruth Parker",
    "Steven Evans", "Sharon Edwards", "Kevin Collins", "Deborah Stewart", "Ronald Morris",
    "Shirley Rogers", "Timothy Reed", "Cynthia Cook", "Larry Morgan", "Kathleen Bell"
]

# Sample notes
notes = [
    "Thank you for your support!", "In memory of our beloved horse", "For the new barn project",
    "Monthly donation", "Annual contribution", "Special fundraiser", "Holiday donation",
    "Emergency fund", "Equipment upgrade", "Feed storage improvement", "Veterinary care fund",
    "Training facility", "Pasture maintenance", "Water system upgrade", "Fencing repair",
    "Transportation costs", "Staff training", "Educational programs", "Community outreach",
    "Research initiative"
]

def generate_random_date(start_year=2020, end_year=2024):
    """Generate a random date between start_year and end_year"""
    start_date = datetime(start_year, 1, 1)
    end_date = datetime(end_year, 12, 31)
    days_between = (end_date - start_date).days
    random_days = random.randint(0, days_between)
    return (start_date + timedelta(days=random_days)).strftime('%Y-%m-%d')

def insert_sample_data(num_records=50):
    """Insert sample donation records into the database"""
    db = Database()
    
    for _ in range(num_records):
        donor_name = random.choice(donor_names)
        amount = round(random.uniform(10, 1000), 2)
        date = generate_random_date()
        note = random.choice(notes)
        
        db.add_donation(donor_name, amount, date, note)
    
    print(f"Successfully inserted {num_records} sample donation records.")

if __name__ == "__main__":
    insert_sample_data() 