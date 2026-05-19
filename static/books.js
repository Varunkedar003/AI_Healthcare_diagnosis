document.addEventListener('DOMContentLoaded', async () => {

    const bookList = document.getElementById('bookList');

    try {
        const response = await fetch('/books');
        const books = await response.json();

        bookList.innerHTML = "";

        books.forEach(book => {
            const li = document.createElement('li');

            li.innerHTML = `
                <strong>${book.title}</strong> by ${book.author}
                <button onclick="downloadBook(${book.id})">Download</button>
            `;

            bookList.appendChild(li);
        });

    } catch (error) {
        console.error("Error fetching books:", error);
        bookList.innerHTML = "<li>Error loading books</li>";
    }

});

// Download function
async function downloadBook(id) {
    try {
        const response = await fetch(`/books/${id}/download`);
        const blob = await response.blob();

        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = `book_${id}.txt`;
        a.click();

    } catch (error) {
        console.error("Download error:", error);
    }
}