const form = document.getElementById("itemForm");
const message = document.getElementById("message_confirm");

function showMessage(text) {
    message.textContent = text;
    message.style.display = "block";
}

async function loadCarousel() {
    try {
        const response = await fetch("/login/cards_show", { method: "POST" });
        const { image_url: imageUrls, image_story: stories } = await response.json();
        document.querySelectorAll(".image_card_div").forEach((slot, index) => {
            const image = new Image();
            image.src = `/get-images/${imageUrls[index]}`;
            image.alt = stories[index] || "Magic card";
            image.className = "image_card";
            const story = document.createElement("p");
            story.textContent = stories[index];
            story.className = "text--center";
            slot.replaceChildren(image, story);
        });
    } catch {
        showMessage("Card images could not be loaded.");
    }
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

loadCarousel();
