document.addEventListener("DOMContentLoaded", function() {
    const searchInput = document.getElementById("search_string");
    const suggestionBox = document.createElement("div");
    suggestionBox.classList.add("suggestion-box");
    document.body.appendChild(suggestionBox);

    searchInput.addEventListener("input", async function() {
        const query = searchInput.value;
        if (query.length > 0) {
            const response = await fetch(`/list_client?query=${query}`);
            const suggestions = await response.json();
            showSuggestions(suggestions, query);
        } else {
            suggestionBox.innerHTML = "";
            suggestionBox.style.display = "none";
        }
    });

    function showSuggestions(suggestions, query) {
        suggestionBox.innerHTML = "";
        suggestions.forEach(client => {
            if (client.toLowerCase().startsWith(query.toLowerCase())) {
                const suggestionItem = document.createElement("div");
                suggestionItem.classList.add("suggestion-item");
                suggestionItem.textContent = client;
                suggestionItem.addEventListener("click", function() {
                    searchInput.value = client;
                    suggestionBox.innerHTML = "";
                    suggestionBox.style.display = "none";
                });
                suggestionBox.appendChild(suggestionItem);
            }
        });
        suggestionBox.style.display = suggestions.length > 0 ? "block" : "none";
    }

    // Position the suggestion box below the input field
    const rect = searchInput.getBoundingClientRect();
    suggestionBox.style.position = "absolute";
    suggestionBox.style.top = `${rect.bottom}px`;
    suggestionBox.style.left = `${rect.left}px`;
    suggestionBox.style.width = `${rect.width}px`;
});