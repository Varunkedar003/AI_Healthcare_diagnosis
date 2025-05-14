// Wait for the DOM to be fully loaded before executing any code
document.addEventListener('DOMContentLoaded', () => {
    const bookList = document.getElementById('bookList');
    const bookContent = document.getElementById('bookContent');
    const bookTitle = document.getElementById('bookTitle');
    const bookAuthor = document.getElementById('bookAuthor');
    const bookFullContent = document.getElementById('bookFullContent');

    // Check if all required elements are present
    if (!bookList || !bookContent || !bookTitle || !bookAuthor || !bookFullContent) {
        console.error('One or more required DOM elements are missing');
        return;
    }

    async function fetchBooks() {
        try {
            const response = await fetch('http://127.0.0.1:5000/books');
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            const books = await response.json();
            displayBooks(books);
        } catch (error) {
            console.error('Error fetching books:', error.message);
            if (bookList) {
                bookList.innerHTML = '<li>Error loading books. Please try again later.</li>';
            }
        }
    }

    function displayBooks(books) {
        bookList.innerHTML = '';
        books.forEach(book => {
            const li = document.createElement('li');
            li.className = 'book-item';
            li.innerHTML = `
                <div class="book-info">
                    <h3 class="book-title">${book.title}</h3>
                    <p class="book-author">by ${book.author}</p>
                </div>
                <button class="download-btn" data-id="${book.id}">Download</button>
            `;
            bookList.appendChild(li);
        });

        // Add event listeners
        document.querySelectorAll('.download-btn').forEach(btn => {
            btn.addEventListener('click', (e) => downloadBook(e.target.dataset.id));
        });
    }

    async function downloadBook(bookId) {
        try {
            const response = await fetch(`http://127.0.0.1:5000/books/${bookId}/download`);
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            const blob = await response.blob();
            const url = window.URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.style.display = 'none';
            a.href = url;
            a.download = `book_${bookId}.txt`;
            document.body.appendChild(a);
            a.click();
            window.URL.revokeObjectURL(url);
            alert('Download started. The book will be saved to your downloads folder.');
        } catch (error) {
            console.error('Error downloading book:', error.message);
            alert('Failed to download the book. Please try again.');
        }
    }

    // Call fetchBooks only after ensuring all elements are loaded
    fetchBooks();
});

