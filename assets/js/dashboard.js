document.addEventListener("DOMContentLoaded", () => {
    const form = document.getElementById("studentForm");
    const statusDisplay = document.getElementById("card-status");
  
    // Load status from localStorage
    const savedStudentNumber = localStorage.getItem("studentNumber");
    if (savedStudentNumber) {
      const status = localStorage.getItem(`status_${savedStudentNumber}`) || "Starting";
      statusDisplay.innerHTML = `Status: <strong>${status}</strong>`;
    }
  
    // Handle form submission
    form.addEventListener("submit", function (e) {
      e.preventDefault();
  
      const name = document.getElementById("fullName").value;
      const number = document.getElementById("studentNumber").value;
      const email = document.getElementById("email").value;
      const photoInput = document.getElementById("photo");
  
      localStorage.setItem("studentName", name);
      localStorage.setItem("studentNumber", number);
      localStorage.setItem("studentEmail", email);
  
      const reader = new FileReader();
      reader.onload = function () {
        localStorage.setItem("studentPhoto", reader.result);
        // Optionally, set status to "Processing" after submission
        localStorage.setItem(`status_${number}`, "Processing");
        window.location.href = "virtual-card.html";
      };
  
      reader.readAsDataURL(photoInput.files[0]);
  
      alert("Your details have been submitted. Please wait while we process your card.");
    });
  });
  