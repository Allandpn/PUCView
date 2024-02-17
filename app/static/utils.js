
document.addEventListener('DOMContentLoaded', function () { 
  const state_page = document.getElementById('route-state')
  setColorNavItem(state_page)
})




const setColorNavItem = function(page){
if(page.textContent){
  const link = document.getElementById(`state-page-${page.textContent}`)
  link.classList.add('nav-menu-link-selected')
}

const menuLinks = document.querySelectorAll('.nav-menu-link  li a');
menuLinks.forEach(link => {
  link.addEventListener('click', function(event) {
    const target = this.getAttribute('data-target');
    const targetLi = document.querySelector(`[data-target="${target}"]`);
    
    document.querySelectorAll('.nav-menu-link .nav-item a').forEach( li => {
        console.log(li);
        console.log(targetLi)
        li.classList.remove('nav-menu-link-selected')
        });
    if (targetLi) {
      targetLi.classList.add('nav-menu-link-selected');
    }
  });
});


}