// DOM Elements
const donationsTableBody = document.getElementById('donationsTableBody');
const yearFilter = document.getElementById('yearFilter');
const addDonationBtn = document.getElementById('addDonationBtn');
const refreshBtn = document.getElementById('refreshBtn');
const addDonationModal = document.getElementById('addDonationModal');
const addDonationForm = document.getElementById('addDonationForm');

// State
let currentDonations = [];
let editingRow = null;

// API Functions
const api = {
    async getDonations(year = '') {
        const url = year ? `/api/donations?year=${year}` : '/api/donations';
        const response = await fetch(url);
        if (!response.ok) throw new Error('Failed to fetch donations');
        return response.json();
    },

    async getYears() {
        const response = await fetch('/api/years');
        if (!response.ok) throw new Error('Failed to fetch years');
        return response.json();
    },

    async addDonation(donation) {
        const response = await fetch('/api/donations', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(donation)
        });
        if (!response.ok) throw new Error('Failed to add donation');
        return response.json();
    },

    async updateDonation(id, donation) {
        const response = await fetch(`/api/donations/${id}`, {
            method: 'PUT',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(donation)
        });
        if (!response.ok) throw new Error('Failed to update donation');
        return response.json();
    },

    async deleteDonation(id) {
        const response = await fetch(`/api/donations/${id}`, {
            method: 'DELETE'
        });
        if (!response.ok) throw new Error('Failed to delete donation');
        return response.json();
    }
};

// UI Functions
function formatDate(dateString) {
    return new Date(dateString).toLocaleDateString();
}

function formatAmount(amount) {
    return new Intl.NumberFormat('en-US', {
        style: 'currency',
        currency: 'USD'
    }).format(amount);
}

function createEditableCell(value, type = 'text') {
    const cell = document.createElement('td');
    cell.className = 'editable';
    
    const display = document.createElement('span');
    display.textContent = type === 'amount' ? formatAmount(value) : value;
    
    const input = document.createElement(type === 'textarea' ? 'textarea' : 'input');
    input.type = type;
    input.value = value;
    input.style.display = 'none';
    
    if (type === 'textarea') {
        input.rows = 3;
    }
    
    cell.appendChild(display);
    cell.appendChild(input);
    
    return cell;
}

function createActionButtons(donation) {
    const cell = document.createElement('td');
    cell.className = 'table__actions';
    
    const editBtn = document.createElement('button');
    editBtn.className = 'table__action-button';
    editBtn.innerHTML = '✏️';
    editBtn.title = 'Edit';
    
    const deleteBtn = document.createElement('button');
    deleteBtn.className = 'table__action-button';
    deleteBtn.innerHTML = '🗑️';
    deleteBtn.title = 'Delete';
    
    const saveBtn = document.createElement('button');
    saveBtn.className = 'table__action-button';
    saveBtn.innerHTML = '💾';
    saveBtn.title = 'Save Changes';
    saveBtn.style.display = 'none';
    
    cell.appendChild(editBtn);
    cell.appendChild(deleteBtn);
    cell.appendChild(saveBtn);
    
    return cell;
}

function renderDonations(donations) {
    donationsTableBody.innerHTML = '';
    currentDonations = donations;
    
    donations.forEach(donation => {
        const row = document.createElement('tr');
        row.dataset.id = donation.id;
        
        row.appendChild(createEditableCell(donation.donor_name));
        row.appendChild(createEditableCell(donation.amount, 'number'));
        row.appendChild(createEditableCell(donation.date, 'date'));
        row.appendChild(createEditableCell(donation.note, 'textarea'));
        row.appendChild(createActionButtons(donation));
        
        donationsTableBody.appendChild(row);
    });
}

// Event Handlers
async function handleYearFilter() {
    try {
        const year = yearFilter.value;
        const donations = await api.getDonations(year);
        renderDonations(donations);
    } catch (error) {
        alert('Error filtering donations: ' + error.message);
    }
}

async function handleRefresh() {
    try {
        // Reset the year filter to show all donations
        yearFilter.value = '';
        const donations = await api.getDonations();
        renderDonations(donations);
        alert('Data refreshed successfully!');
    } catch (error) {
        alert('Error refreshing data: ' + error.message);
    }
}

async function handleAddDonation(event) {
    event.preventDefault();
    
    const formData = new FormData(addDonationForm);
    const donation = {
        donor_name: formData.get('donorName'),
        amount: parseFloat(formData.get('amount')),
        date: formData.get('date'),
        note: formData.get('note')
    };
    
    try {
        await api.addDonation(donation);
        closeModal();
        handleYearFilter();
        addDonationForm.reset();
    } catch (error) {
        alert('Error adding donation: ' + error.message);
    }
}

async function handleEdit(row) {
    if (editingRow) {
        // If another row is being edited, cancel its edit mode
        cancelEdit(editingRow);
    }
    
    editingRow = row;
    const cells = row.cells;
    const actionCell = cells[cells.length - 1];
    const saveButton = actionCell.querySelector('button:nth-child(3)');
    
    // Show input fields
    for (let i = 0; i < cells.length - 1; i++) {
        const cell = cells[i];
        const display = cell.querySelector('span');
        const input = cell.querySelector('input, textarea');
        
        display.style.display = 'none';
        input.style.display = 'block';
    }
    
    // Show save button
    saveButton.style.display = 'inline-block';
}

function cancelEdit(row) {
    const cells = row.cells;
    const actionCell = cells[cells.length - 1];
    const saveButton = actionCell.querySelector('button:nth-child(3)');
    
    // Hide input fields and restore display values
    for (let i = 0; i < cells.length - 1; i++) {
        const cell = cells[i];
        const display = cell.querySelector('span');
        const input = cell.querySelector('input, textarea');
        
        display.style.display = 'block';
        input.style.display = 'none';
    }
    
    // Hide save button
    saveButton.style.display = 'none';
    
    if (editingRow === row) {
        editingRow = null;
    }
}

async function handleSave(row) {
    const cells = row.cells;
    const donation = {
        donor_name: cells[0].querySelector('input').value,
        amount: parseFloat(cells[1].querySelector('input').value),
        date: cells[2].querySelector('input').value,
        note: cells[3].querySelector('textarea').value
    };
    
    try {
        await api.updateDonation(row.dataset.id, donation);
        cancelEdit(row);
        handleYearFilter();
    } catch (error) {
        alert('Error updating donation: ' + error.message);
    }
}

async function handleDelete(id) {
    if (!confirm('Are you sure you want to delete this donation?')) return;
    
    try {
        await api.deleteDonation(id);
        handleYearFilter();
    } catch (error) {
        alert('Error deleting donation: ' + error.message);
    }
}

function openModal() {
    addDonationModal.classList.add('modal--visible');
}

function closeModal() {
    addDonationModal.classList.remove('modal--visible');
}

// Event Listeners
yearFilter.addEventListener('change', handleYearFilter);
addDonationBtn.addEventListener('click', openModal);
refreshBtn.addEventListener('click', handleRefresh);
addDonationForm.addEventListener('submit', handleAddDonation);

donationsTableBody.addEventListener('click', (event) => {
    const target = event.target;
    const row = target.closest('tr');
    
    if (!row) return;
    
    if (target.classList.contains('table__action-button')) {
        if (target.title === 'Edit') {
            handleEdit(row);
        } else if (target.title === 'Delete') {
            handleDelete(row.dataset.id);
        } else if (target.title === 'Save Changes') {
            handleSave(row);
        }
    }
});

// Initialize
handleYearFilter(); 