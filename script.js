function updateUI() {
    fetch("/data")
        .then(response => response.json())
        .then(data => {
            document.getElementById("prediction").textContent = data.prediction;
            document.getElementById("confidence-fill").style.width = `${data.confidence}%`;
            document.getElementById("accuracy").textContent = data.confidence.toFixed(1);
            document.getElementById("streak").textContent = data.history.filter((x, i, arr) => x === arr[i-1]).length;
            document.getElementById("last10").textContent = data.history.slice(-10).join(", ");
        });

    setTimeout(updateUI, 2000);  // Update every 2 seconds
}

updateUI();