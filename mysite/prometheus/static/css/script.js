function fetchLabelValues(labelName) {
    const metricName = document.getElementById('saved_metric_name').value.trim();
    fetch(`/get_label_values?label_name=${labelName}&metric_name=${metricName}`)
        .then(response => response.json())
        .then(data => {
            const resultDiv = document.getElementById('label_values');
            if (data.length === 0) {
                resultDiv.innerHTML = `没有找到标签 "${labelName}" 的值`;
            } else {
                let listItems = data.map(value => `<li>${value}</li>`).join('');
                resultDiv.innerHTML = `<h3>"${labelName}" 标签的所有值:</h3><ul>${listItems}</ul>`;
                resultDiv.style.display = 'block';
            }
        });
}