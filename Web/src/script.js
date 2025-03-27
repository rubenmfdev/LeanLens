function analyze() {
  const photo = document.getElementById("photo").files[0];
  const goal = document.getElementById("goal").value;
  const type = document.getElementById("type").value;
  const button = document.querySelector("button");
  const planText = document.getElementById("plan-text");

  if (!photo || !goal || !type) {
    alert("Please complete all fields.");
    return;
  }

  button.disabled = true;
  button.innerHTML = 'Generating plan <div class="spinner"></div>';
  planText.classList.add("typing");
  planText.textContent = "🤖 LeanLens is analyzing your photo and crafting your plan...";
  document.getElementById("result").style.display = "block";

  const formData = new FormData();
  formData.append("photo", photo);
  formData.append("goal_fat", goal);
  formData.append("goal_type", type);

  fetch("http://localhost:5050/generate-plan", {
    method: "POST",
    body: formData
  })
    .then(res => res.json())
    .then(data => {
      document.getElementById("fat-pct").textContent = data.estimated_fat;
      document.getElementById("goal-text").textContent = `${goal}% - ${type}`;
      planText.innerHTML = data.plan;
    })
    .catch(err => {
      console.error("❌ Fetch failed:", err);
      planText.textContent = "❌ Something went wrong. Please try again.";
    })
    .finally(() => {
      button.disabled = false;
      button.innerHTML = "Analyze & Generate Plan";
      planText.classList.remove("typing");
    });
}
