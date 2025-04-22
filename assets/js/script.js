document.getElementById("switch1").addEventListener("click", () => {
    document.querySelector(".signup").classList.remove("hide");
    document.querySelector(".login").classList.add("hide");
  });
  
  document.getElementById("switch2").addEventListener("click", () => {
    document.querySelector(".signup").classList.add("hide");
    document.querySelector(".login").classList.remove("hide");
  });
  
  function handleLogin() {
    const role = document.getElementById("role").value;
    const email = document.querySelector('.login input[name="email"]').value;
    const password = document.querySelector('.login input[name="password"]').value;
  
    if (role === "admin") {
      if (email === "admin@example.com" && password === "admin123") {
        alert("Redirecting to Admin Panel...");
        window.location.href = "admin-panel.html"; // You create this page
      } else {
        alert("Invalid admin credentials.");
      }
    } else {
      if (email && password) {
        alert("Redirecting to Student Dashboard...");
        window.location.href = "dashboard.html"; // You create this page
      } else {
        alert("Please fill in your details.");
      }
    }
  }
  