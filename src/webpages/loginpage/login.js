const form = document.getElementById("itemForm");
const message = document.getElementById("message_confirm");

function showMessage(text) {
    message.textContent = text;
    message.style.display = "block";
}

form.addEventListener("submit", async (event) => {
    event.preventDefault();
    const submit = form.querySelector('[type="submit"]');
    submit.disabled = true;
    submit.value = "Signing in...";

    try {
        const response = await fetch("/login", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(Object.fromEntries(new FormData(form))),
        });
        const { message: result } = await response.json();
        if (result === "Login successful") {
            window.location.href = "/";
            return;
        }
        showMessage(result === "username error" ? "No account matches that username." : "Incorrect password. Please try again.");
    } catch {
        showMessage("Could not sign in. Please try again.");
    } finally {
        submit.disabled = false;
        submit.value = "Sign In";
    }
});
