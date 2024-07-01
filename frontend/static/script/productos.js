let listElements = document.querySelectorAll('.list_button--click');

listElements.forEach(listElement => {
    listElement.addEventListener('click', ()=>{
        listElement.classList.toggle('arrow');

        let height = 0;
        let menu = listElement.nextElementSibling;
        if(menu.clientHeight =="0"){
            height=menu.scrollHeight;
        }

        menu.style.height = height+"px";
    })

})

const bars = document.querySelector(".bars");
const navBar = document.querySelector(".nav");

bars.onclick = function () {
    navBar.classList.toggle("active");
    bars.classList.toggle("cross");
};

