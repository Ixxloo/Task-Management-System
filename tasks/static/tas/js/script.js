const expandButton = document.querySelector("#expand-gallery-btn");
const extraImages = document.querySelectorAll(".extra-gallery");
//   The expaned button block
expandButton.addEventListener("click", function() {
    extraImages.forEach(function(image) {
        image.style.display = "block";
    });
    expandButton.style.display = "none";
});
    // Makeing the submission form using JavaScript work without refreshing the page (AJAX)
const contactF=document.querySelector("#contact-form");

contactF.addEventListener("submit",function(event){
    event.preventDefault();
    const formData = new FormData(contactF);

    fetch(contactF.action, {
        method: "POST",
        body: formData,
    })
    .then(function(response) {
    return response.json();
})
    .then(function(data) {
        if (data.success) {
            showToast("Message sent successfully!", "success");
            contactF.reset();
        } else {
            showToast(data.errors.join(" "), "error");
        }
    })
    .catch(function(error) {
        showToast("Something went wrong. Please try again.", "error");
    });                    //this is CSS class
})
//   the toaset function  *********
function showToast(message, type) {
    const toastBox = document.querySelector("#toast-box");

    const toast = document.createElement("div");
    toast.textContent = message;
    toast.className = "toast-message toast-" + type;

    toastBox.appendChild(toast);

    setTimeout(function() {
        toast.classList.add("toast-show");
    }, 10);

    setTimeout(function() {
        toast.classList.remove("toast-show");
        setTimeout(function() {
            toast.remove();
        }, 300);
    }, 3000);
}   // the apparing message are both popout not one the " something went wrong " and "the form sent successfully"-> fixed!