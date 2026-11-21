
document.addEventListener('click', function(event) {
    const button = event.target.closest('.update-btn');

    if (!button) return;

    const task = button.closest('.task-item');

    if (!task) return;

    const taskField = task.querySelector('.task-field');
    const updateField = task.querySelector('.update-field');

    if (!taskField || !updateField) return;

    taskField.classList.toggle('d-none');
    updateField.classList.toggle('d-none');
});

function validateTaskTitle(input) {
    const title = input.value.trim();
    let message = '';

    if (!title) {
        message = 'Task title cannot be empty.';
    } else if (title.length > 50) {
        message = 'Task title must be 50 characters or fewer.';
    }

    const container = input.closest('form, .task-item');
    const feedback = container.querySelector('.title-validation');
    feedback.textContent = message;
    feedback.classList.toggle('d-none', !message);
    input.setCustomValidity(message);
    input.setAttribute('aria-invalid', String(Boolean(message)));

    return !message;
}

document.addEventListener('input', function(event) {
    if (event.target.matches('.task-title-input')) {
        validateTaskTitle(event.target);
    }
});

document.addEventListener('invalid', function(event) {
    if (event.target.matches('.task-title-input')) {
        validateTaskTitle(event.target);
    }
}, true);
// update field validation
document.body.addEventListener('htmx:beforeRequest', function(event) {
    const sender = event.detail.elt;
    const titleInput = sender.matches('.task-title-input')
        ? sender
        : sender.querySelector('.task-title-input');

    if (!titleInput) return;

    titleInput.value = titleInput.value.trim();

    if (!validateTaskTitle(titleInput)) {
        event.preventDefault();
    }
});
// Update task handle
document.addEventListener('keydown', function(event) {
    const input = event.target.closest('.update-field.task-title-input');

    if (!input || event.key !== 'Enter') return;

    event.preventDefault();

    if (event.repeat || input.dataset.updatePending === 'true') return;
    if (!validateTaskTitle(input)) return;

    input.dataset.updatePending = 'true';
    htmx.trigger(input, 'task-title-enter');
});

document.body.addEventListener('htmx:afterRequest', function(event) {
    const input = event.detail.elt;

    if (input.matches('.update-field.task-title-input')) {
        delete input.dataset.updatePending;
    }
});

// Close Add Task Modal
document.addEventListener('htmx:afterRequest', function(event){
    console.log('running')
    const form = document.getElementById('addTaskForm');

    if(event.detail.elt === form && event.detail.successful){
        const modalElement =document.getElementById('exampleModal');

        const modal = bootstrap.Modal.getInstance(modalElement);

        if(modal){
            form.reset();
            modal.hide();
        }
    }
});

