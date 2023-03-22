fetch('/members/')
  .then(response => {
    if (!response.ok) {
      throw new Error('Network response was not ok');
    }
      return response.json();

  })
  .then(data => {
    // handle the JSON data here
    const playerContainer = document.querySelector('.player-info');
    console.log(playerContainer);
    playerContainer.innerHTML = ''; // clear the container
    data.forEach(member => {
      const playerDiv = document.createElement('div');
      playerDiv.className = 'player';
      playerDiv.innerHTML = `
        <span class="chips-label">${member.amount}</span>
        <img src="${member.photo}" alt="Avatar" width="40" height="50">
        <span class="card-label">${member.name}</span>
        <span class="rotate-btn">
            <button class="button" onclick="showAlert()">+</button>
            <button class="button" onclick="showAlert()">-</button>
        </span>
      `;
      playerContainer.appendChild(playerDiv);
    });
  })
  .catch(error => console.error('Error:', error));

    
function showAlert(){
    alert("Hello! I am ready to deal!");
    }