document.addEventListener("DOMContentLoaded", function() {
    const searchInput = document.getElementById("search_string");
    const dataList = document.getElementById("list-clients");
    

    searchInput.addEventListener("input", async function() {
        const query = searchInput.value;
        var $checkbox_client = $("#client_filter")

        if (query.length > 0 &&  $checkbox_client.is(':checked')) {
            const response = await fetch(`/list_client?query=${query}`);
            const suggestions = await response.json();
            updateDataList(suggestions);
        } else {
            dataList.innerHTML = "";
        }
    });

    function updateDataList(suggestions) {
        dataList.innerHTML = "";
        suggestions.forEach(client => {
            const option = document.createElement("option");
            option.value = client;
            dataList.appendChild(option);
        });
    }
});