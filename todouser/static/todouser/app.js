// // Update todo 
//     // Fetch CSRF token from cookies
//     function getCookie(name) {
//       let cookieValue = null;
//       if (document.cookie && document.cookie !== '') {
//           const cookies = document.cookie.split(';');
//           for (let i = 0; i < cookies.length; i++) {
//               const cookie = cookies[i].trim();
//               if (cookie.substring(0, name.length + 1) === (name + '=')) {
//                   cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
//                   break;
//               }
//           }
//       }
//       return cookieValue;
//   }
//   // Function to handle the form submission and update the data
//   function updateTodo() {
//       const taskName = document.getElementById('update-task-name');
//       const description = document.getElementById('update-task-desc');
//       const task_sts = document.getElementById('update-task-status');
//       const task_prty = document.getElementById('update-task-priority');
//       const completion_dat = document.getElementById('task-cmplt-date');
//       const pk = "{{ todos.pk }}";
//       // const userId = "{{ user.id }}";

//       const formData = new FormData();
//       formData.append('tname', taskName.value);
//       formData.append('desc', description.value);
//       formData.append('status', task_sts.value);
//       formData.append('priority', task_prty.value);
//       formData.append('completion_date', completion_dat.value);
//       // formData.append('user', userId);

//       const csrfToken = getCookie('csrftoken');

//       fetch(`/updateapi/${pk}/`, {
//           method: 'PATCH',
//           body: formData,
//           headers: {
//               'X-CSRFToken': csrfToken,
//           }
//       })
//           .then(response => {
//               if (response.ok) {
//                   // Data updated successfully, and redirected to the home page
//                   alert("Todo updated successfully!")
//                   window.location.href = 'http://127.0.0.1:8000/hometodo/';
//               } else {
//                   console.error('Failed to update todo!');
//               }
//           })
//           .catch(error => console.error('Update Error:', error));
//   }

//   // Add an event listener to the form's submit button
//   document.querySelector('update-task-btn').addEventListener('submit', function (event) {
//       // event.preventDefault();
//       updateTodo();
//   }); 