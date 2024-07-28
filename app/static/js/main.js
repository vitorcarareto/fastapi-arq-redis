document.addEventListener('DOMContentLoaded', (event) => {
    console.log('page loaded.');

    const form = document.getElementById('tasks_form');
    const tasks = document.getElementById('tasks');

    function getTaskStatus(JobId) {
        axios.get(`/task/${JobId}`)
            .then(function (resp) {
                if (resp.data.status === 'complete' || resp.data.status == 'not_found') {
                    const tableRow = `
                    <tr>
                      <td>${resp.data.job_id}</td>
                      <td>${resp.data.status}</td>
                      <td>${resp.data.result}</td>
                    </tr>
                    `;
                    const newRow = document.getElementById('table-status').insertRow(1);
                    newRow.innerHTML = tableRow;
                    return false;
                }

                setTimeout(function () {
                    getTaskStatus(resp.data.job_id);
                }, 1000);

            });
    }

    function createTasks(count) {
        axios.post('/task', {
            count: count
        })
            .then(function (response) {
                const jobIds = response.data.task_ids;
                let results = [];

                jobIds.forEach(function (item) {
                    results.push(getTaskStatus(item));
                });

                Promise.all(results)
                    .catch(function (error) {
                        console.log(error);
                    });
            })
            .catch(function (error) {
                console.log(error);
            });
    }

    form.addEventListener('submit', (evt) => {
        evt.preventDefault();
        const count = tasks.value;
        createTasks(count);
    });
});