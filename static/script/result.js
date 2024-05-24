console.log('result js')

document.addEventListener("DOMContentLoaded", function() {
    console.log("> result.js [ok]")
    const form = document.getElementById("search-form");
    const loadingSpinner = document.getElementById("loading-spinner");

    form.addEventListener("submit", function(event) {
        event.preventDefault();
        loadingSpinner.classList.remove("d-none");

        const formData = new FormData(form);
        const searchParams = new URLSearchParams(formData).toString();

        fetch("/search_async", {
            method: "POST",
            headers: {
                "Content-Type": "application/x-www-form-urlencoded"
            },
            body: searchParams
        })
        .then(response => response.text())
        .then(data => {
            console.log("> data response [ok]");
            loadingSpinner.classList.add("d-none");
            document.getElementById("search-results").innerHTML = data;
            const links = document.querySelectorAll("#file-list a");

            links.forEach(link => {
                link.addEventListener("click", function(event) {
                    console.log("> prevent default [ok]");
                    event.preventDefault();
                    const url = link.getAttribute("href");

                    const fileExtension = url.split('.').pop().toLowerCase();
                    let viewerUrl;

                    if (fileExtension === 'pdf') {
                        viewerUrl = url; // Direct link for PDF
                    } else if (fileExtension === 'xlsx') {
                        viewerUrl = 'https://docs.google.com/viewer?url=' + encodeURIComponent(url) + '&embedded=true';
                    } else {
                        viewerUrl = ''; // Handle unsupported file types
                        console.error('Unsupported file type:', fileExtension);
                    }

                    if (viewerUrl) {
                        document.getElementById("file-preview").src = viewerUrl;
                        document.getElementById("doc-name").innerText = link.innerText;
                    }
                });
            });
        })
        .catch(error => {
            loadingSpinner.classList.add("d-none");
            console.error('Error:', error);
        });
    });
});