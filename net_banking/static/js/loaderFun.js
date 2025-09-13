// utils.js
/* function dvloader(action) {
    const loader = document.getElementById('dvloader');
    if (!loader) return;

    if (action === 'show') {
        loader.style.display = 'flex';  // or 'block' based on your CSS
    } else if (action === 'hide') {
        loader.style.display = 'none';
    }
}
*/
function dvloader(action, bankName = 'Mini Bank') {
  const loader  = document.getElementById('dvloader');
  const content = document.getElementById('dvloader-content');
  const label   = document.getElementById('bank-name');
  if (!loader || !content || !label) return;

  if (action === 'show') {
    label.textContent     = `Processing with ${bankName}`;
    loader.style.display  = 'flex';   // show the overlay
    content.style.display = 'flex';   // show the inner flex box
  } else {
    loader.style.display  = 'none';   // hide overlay
    content.style.display = 'none';   // hide inner box
  }
}