document.addEventListener("DOMContentLoaded", () => {
  const form = document.getElementById("openai-form");
  const outputContainer = document.getElementById("output-container");
  const outputText = document.getElementById("output-text");

  form.addEventListener("submit", async (event) => {
    event.preventDefault();
    const inputText = document.getElementById("input-text").value;
  
    // Call the /generate route
    const response = await fetch("/generate", {
      method: "POST",
      body: new FormData(form),
    });
    const jsonResponse = await response.json();
  
    // Display the response in the output container
    outputText.textContent = jsonResponse.output;
  });

});
