const urlPrefix = 'http://localhost:5000';

function showLoading(document) {
    document.getElementById('loadingIndicator').style.display = 'flex';
}

function hideLoading(document) {
    document.getElementById('loadingIndicator').style.display = 'none';
}