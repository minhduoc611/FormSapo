// Your JavaScript code here

function init() {
    const inputElement = document.getElementById("fileInput");
    inputElement.addEventListener("change", handleFiles, false);
  
    const uploadForm = document.getElementById("uploadForm");
    uploadForm.addEventListener("submit", handleSubmit, false);
  }
  
  function handleFiles() {
    const fileList = this.files;
    const previewArea = document.getElementById("filePreview");
  
    while (previewArea.firstChild) {
      previewArea.removeChild(previewArea.firstChild);
    }
  
    for (let i = 0; i < fileList.length; i++) {
      const file = fileList[i];
      const img = document.createElement("img");
      img.classList.add("file-image");
      img.file = file;
  
      const reader = new FileReader();
      reader.onload = (function(aImg) {
        return function(e) {
          aImg.src = e.target.result;
        };
      })(img);
  
      reader.readAsDataURL(file);
      previewArea.appendChild(img);
    }
  }
  
  function handleSubmit(event) {
    event.preventDefault();
  
    const formData = new FormData();
    const fileList = document.getElementById("fileInput").files;
    const csrftoken = getCookie("csrftoken");
  
    for (let i = 0; i < fileList.length; i++) {
      const file = fileList[i];
      formData.append("files", file);
    }
  
    fetch("{% url 'upload' %}", {
      method: "POST",
      headers: {
        "X-CSRFToken": csrftoken,
      },
      body: formData,
    })
      .then((response) => response.json())
      .then((data) => {
        alert("Files uploaded successfully!");
      })
      .catch((error) => {
        console.error("Error:", error);
      });
  }
  
  document.addEventListener("DOMContentLoaded", init);
  