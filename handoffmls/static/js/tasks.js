// Get references to the necessary elements
const tasksContainer = document.getElementById("tasks");
const addButton = document.getElementById("addButton");
const trackCount = document.getElementById("count");

// Counter to track the number of textareas
let textareaCount = 1;

// Function to add a new textarea
function addTextarea() {
  // Increment the counter
  textareaCount++;
  trackCount.value = textareaCount;

  // Create a new div to hold the textarea, button, and checkbox
  const taskDiv = document.createElement("div");
  taskDiv.classList.add("row", "mb-3");

  // Create a column for the textarea
  const textareaColumn = document.createElement("div");
  textareaColumn.classList.add("col-8");

  // Create the textarea element
  const textarea = document.createElement("textarea");
  const currentCount = textareaCount;
  textarea.id = `task-${currentCount}`;
  textarea.name = `task-${currentCount}`;
  textarea.classList.add("form-control");
  textarea.placeholder = `Task ${currentCount}`;

  // Append the textarea to the textarea column
  textareaColumn.appendChild(textarea);

  // Create a column for the button and checkbox
  const buttonColumn = document.createElement("div");
  buttonColumn.classList.add("col-4", "d-flex", "align-items-center");

  // Create the remove button
  const removeButton = document.createElement("button");
  removeButton.textContent = "Remove";
  removeButton.classList.add("btn", "btn-danger", "me-2");

  // Create the checkbox
  const checkbox = document.createElement("input");
  checkbox.type = "checkbox";
  checkbox.id = `task-status-${currentCount}`;
  checkbox.name = `task-status-${currentCount}`;
  checkbox.classList.add("form-check-input");

  // Append the button and checkbox to the button column
  buttonColumn.appendChild(removeButton);
  buttonColumn.appendChild(checkbox);

  // Add event listener to remove the textarea when the remove button is clicked
  removeButton.addEventListener("click", () => {
    taskDiv.remove();

    // Decrement the counter
    textareaCount--;
    trackCount.value = textareaCount;

    // Reassign attributes if a textarea is removed
    const remainingTextareas = tasksContainer.querySelectorAll("textarea");
    const remainingCheckboxes = tasksContainer.querySelectorAll(
      'input[type="checkbox"]'
    );

    for (let i = 1; i < remainingTextareas.length; i++) {
      remainingTextareas[i].id = `task-${i + 1}`;
      remainingTextareas[i].name = `task-${i + 1}`;
      remainingTextareas[i].placeholder = `Task ${i + 1}`;

      remainingCheckboxes[i].id = `task-status-${i + 1}`;
      remainingCheckboxes[i].name = `task-status-${i + 1}`;
    }
  });

  // Append the textarea column and button column to the task div
  taskDiv.appendChild(textareaColumn);
  taskDiv.appendChild(buttonColumn);

  // Append the task div to the tasks container
  tasksContainer.appendChild(taskDiv);
}

// Add event listener to the "Add" button
addButton.addEventListener("click", addTextarea);
