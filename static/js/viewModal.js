function displayModal(event)
{
    event.nextElementSibling.style.display="block";
}

function closeModal(event)
{
    event.parentElement.parentElement.parentElement.style.display = "none";
}

function setMyImage(event)
{
    event.parentElement.parentElement.previousElementSibling.src = event.src;
}