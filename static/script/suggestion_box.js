document.addEventListener("DOMContentLoaded", function () {
    const searchInput = document.getElementById("search_string");
    const dataList = document.getElementById("list-clients");

    searchInput.addEventListener("input", async function () {
        const query = searchInput.value;
        var $checkbox_client = $("#client_filter");
        var $checkbox_station = $("#station_filter");
        let response, suggestions;

        if (query.length > 0) {
            try {
                if ($checkbox_client.is(':checked') && $checkbox_station.is(':checked')) {
                    let clientResponse = await fetch(`/list_client?query=${query}`);
                    let stationResponse = await fetch(`/list_station?query=${query}`);
                    let clientSuggestions = await clientResponse.json();
                    let stationSuggestions = await stationResponse.json();
                    suggestions = clientSuggestions.concat(stationSuggestions);
                } else if ($checkbox_client.is(':checked')) {
                    response = await fetch(`/list_client?query=${query}`);
                    suggestions = await response.json();
                } else if ($checkbox_station.is(':checked')) {
                    response = await fetch(`/list_station?query=${query}`);
                    suggestions = await response.json();
                }
                updateDataList(suggestions);
            } catch (error) {
                console.error('Error fetching suggestions:', error);
            }
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