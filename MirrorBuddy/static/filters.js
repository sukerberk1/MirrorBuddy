const filterlist = document.getElementById('filter-choices');
const filterbox = document.getElementById('filterbox');
function filter(filternumber){
    filterlist.style.opacity = "0";
    filterbox.style.backgroundImage = `url('../static/filters/filter${filternumber}.png')`;
}