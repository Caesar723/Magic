const form = document.getElementById("itemForm");
const message = document.getElementById("message_confirm");

function showMessage(text) {
    message.textContent = text;
    message.style.display = "block";
}

form.addEventListener("submit", async (event) => {
    event.preventDefault();
    const data = Object.fromEntries(new FormData(form));
    if (data.password !== data.password_confirmation) {
        showMessage("Passwords do not match.");
        document.getElementById("login__password_repeat").focus();
        return;
    }

    const submit = form.querySelector('[type="submit"]');
    submit.disabled = true;
    submit.value = "Creating account...";
    try {
        const response = await fetch("/signup", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(data),
        });
        const { message: result } = await response.json();
        if (result === "Sign up successful") {
            showMessage("Account created. Redirecting to sign in...");
            setTimeout(() => window.location.href = "/login", 800);
            return;
        }
        showMessage("That username is already in use.");
    } catch {
        showMessage("Could not create the account. Please try again.");
    } finally {
        submit.disabled = false;
        submit.value = "Register";
    }
});
