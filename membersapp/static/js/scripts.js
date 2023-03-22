function shuffle(array) {
  for (let i = array.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1));
    [array[i], array[j]] = [array[j], array[i]];
  }
  return array;
}

  
const cardImages = [];
  const suits = ["C", "D", "H", "S"];
  const values = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "A"];

  for (let suit of suits) {
    for (let value of values) {
      const cardName = `${value}-${suit}.jpg`;
      const cardImagePath = `/static/card_images/${cardName}`;
      cardImages.push(cardImagePath);
    }
  }
  let players = document.querySelectorAll(".card-label");

function Dealers() {
  // Get the dealer and player elements
  const dealer = document.getElementById("dealer-label");
  const dealer2 = document.getElementById("dealer-label2");
  const players = document.querySelectorAll(".card-label");

  // Shuffle the deck
  const deck = [...Array(52).keys()];
  shuffle(deck);

  // Deal two cards to each player and one card to the dealer (all face up)
  for (let i = 0; i < 2; i++) {
    for (let j = 0; j < players.length; j++) {
      const cardIndex = deck.pop();
      const card = cardImages[cardIndex];
      if (i == 0) {
        // First card is face up for players
        players[j].innerHTML += `<img src="${card}" alt="Card">`;
      } else {
        // Second card is face up for players
        const cardIndex = deck.pop();
        const card = cardImages[cardIndex];
        players[j].innerHTML += `<img src="${card}" alt="Card">`;
      }
    }
    const cardIndex = deck.pop();
    const card = cardImages[cardIndex];
    if (i == 0) {
      // First card is face up for dealer
      dealer.innerHTML += `<img src="${card}" alt="Card">`;
    } else {
      // Only deal the second card to the dealer after players have finished their turns
      if (getTotal(dealer) < 17) {
        const cardIndex = deck.pop();
        const card = cardImages[cardIndex];
        dealer2.innerHTML += `<img src="${card}" alt="Card">`;
      }
    }
  }
}

document.addEventListener("DOMContentLoaded", () => {
  function Deal() {
    // Get the dealer and player elements
    const dealer = document.getElementById("dealer-label");
    const dealer2 = document.getElementById("dealer-label2");
    const players = document.querySelectorAll(".card-label");

    // Shuffle the deck
    const deck = [...Array(52).keys()];
    shuffle(deck);

    // Deal two cards to each player and one card to the dealer (all face up)
    for (let i = 0; i < 2; i++) {
      for (let j = 0; j < players.length; j++) {
        const cardIndex = deck.pop();
        const card = cardImages[cardIndex];
        if (i == 0) {
          // First card is face up for players
          players[j].innerHTML += `<img src="${card}" alt="Card">`;
        } else {
          // Second card is face up for players
          const cardIndex = deck.pop();
          const card = cardImages[cardIndex];
          players[j].innerHTML += `<img src="${card}" alt="Card">`;
        }
      }
      const cardIndex = deck.pop();
      const card = cardImages[cardIndex];
      
      if (i == 0) {
        // First card is face up for dealer
        dealer.innerHTML += `<img src="${card}" alt="Card">`;
      } else {
        // Only deal the second card to the dealer after players have finished their turns
        if (getTotal(dealer) < 17) {
          const cardIndex = deck.pop();
          const card = cardImages[cardIndex];
          dealer2.innerHTML += `<img src="${card}" alt="Card">`;
        }
      }
    }

    // Flag variable to keep track of the number of players who have played their turn
    let numPlayersPlayed = 0;

    // Create player objects and add event listeners for stand buttons
    const playersArr = [];
    for (let i = 0; i < players.length; i++) {
      const player = new Player(i, `player${i + 1}-label`);
      playersArr.push(player);

      const standButton = document.getElementById(`player${i + 1}-stand-button`);
      standButton.addEventListener("click", () => {
        player.stand();
        numPlayersPlayed++;
        if (numPlayersPlayed === players.length) {
          stand_card();
        }
      });
    }
  }

  // Add event listener for the deal button
  const dealButton = document.getElementById("deal-button");
  dealButton.addEventListener("click", Deal);
});



const deck = [
  0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51
];

class Player {
  constructor(id, label) {
    this.id = id;
    this.label = label;
    this.cards = [];
    this.hasPlayed = false; // initialize hasPlayed to false
  }

  hit() {
    const cardIndex = deck.pop();
    const card = cardImages[cardIndex];
    this.cards.push(card);
    const playerLabel = document.getElementById(this.label);
    playerLabel.innerHTML += `<img src="${card}" alt="Card">`;
    if (getTotal(playerLabel) > 21) {
      bust(this);
    }
  }

  stand() {
    this.hasPlayed = true; // set hasPlayed to true when player stands
    endPlayerTurn();
  }

  bust() {
    this.hasPlayed = true; // set hasPlayed to true when player busts
    endPlayerTurn();
  }
}

//deck = shuffle([...Array(52).keys()]);
let numPlayers = 5;
let playerHands = [];

// function dealCards(playerIndex, numCards, playerHands) {
//   const playerHand = playerHands[playerIndex];
//   for (let i = 0; i < numCards; i++) {
//     if (deck.length === 0) {
//       console.log("No cards left in deck!");
//       return;
//     }
//     const cardIndex = deck.pop();
//     playerHand.push(cardIndex);
//   }
// }


function add_card(event, member_id) {
  event.preventDefault();
  console.log('Adding card to member', member_id);
  const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
  fetch(`/add_card/${member_id}/`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'X-CSRFToken': csrftoken,
    },
  })
  .then(response => {
    console.log(response);
    if (!response.ok) {
      throw new Error('Failed to add card.');
    }
    return response.text(); // parse the response data as text
  })
  .then(data => {
    console.log(data); // access the response data here
    const parsedData = JSON.parse(data); // parse the response data as JSON
    const player = document.querySelector(`.card-label.player-${member_id}`);
    console.log(player);
    if (player) {
      // let cardIndex = 0; // set the cardIndex to the index of the card image you want to display
      let cardIndex = parsedData.card_index;

      //player.innerHTML += `<img src="/static/card_images/load.jpg" alt="Loading...">`; // display a loading image while the card image is fetched
      
      fetch(`/show_card_image/${cardIndex}/`)
        .then(response => {
          console.log('card_index:', cardIndex);

          if (!response.ok) {
            throw new Error('Failed to load card image.');
          }
          return response.blob();
        })
        .then(blob => {
          const url = URL.createObjectURL(blob);
          
          player.innerHTML += `<img src="${url}" alt="Card">`; // display the fetched card image
        })
        .catch(error => {
          console.error(error);
        });
    } else {
      console.error('Player element not found');
    }
    
    console.log(player);
    if ('deck_json' in parsedData) {
      const deck = JSON.parse(parsedData.deck_json);
      const cardIndex = deck.pop();
      console.log(cardIndex);
    } else {
      console.error('deck_json not found in response data');
    }
  })
  .catch(error => {
    console.error(error);
  });
}


function getTotal(element) {
  if (element) {
    const cards = element.querySelectorAll("img");
    let total = 0;
    let hasAce = false;

    for (let i = 0; i < cards.length; i++) {
      const cardValue = parseInt(cards[i].alt);
      if (cardValue === 1) {
        hasAce = true;
      }
      total += cardValue;
    }

    if (hasAce && total + 10 <= 21) {
      total += 10;
    }

    return total;
  } else {
    return 0;
  }
}


function determineWinner(playerElement) {
  const playerTotal = getTotal(playerElement);
  const dealerTotal = getTotal(document.getElementById("dealer-label"));

  if (playerTotal > 21) {
    return "dealer";
  } else if (dealerTotal > 21) {
    return "player";
  } else if ( playerTotal > dealerTotal) {
    return "player";
  } else if (dealerTotal > playerTotal) {
    return "dealer";
  } else {
    return "tie";
  }
}

function stand_card() {
  // Get the dealer element
  const dealer = document.getElementById("dealer-label");
  const dealer2 = document.getElementById("dealer-label2");
  //deal
  // dealer.innerHTML = '';
  // dealer2.innerHTML = '';
  // Deal one card to the dealer and update the total
  const cardIndex = deck.pop();
  const card = cardImages[cardIndex];
  dealer2.innerText += `<img src="${card}" alt="">`;
  document.querySelector(".msgdealer2").textContent = `Dealer Total: ${getTotal(dealer)}`;
  
  // Determine the winner
  const winner = determineWinner();
  if (winner === "dealer") {
    document.querySelector(".msgdealer").textContent = "Dealer wins!";
  } else if (winner === "player") {
    document.querySelector(".msgdealer").textContent = "You win!";
  } else {
    // If the winner is not the dealer, deal one more card to the dealer and update their total
    const newCardIndex = deck.pop();
    const newCard = cardImages[newCardIndex];
    dealer2.innerHTML += `<img src="${newCard}" alt="">`;
    document.querySelector(".msgdealer2").textContent = `Dealer Total: ${getTotal(dealer)}`;
    const newDealerTotal = getTotal(dealer);
    
    // Determine the winner
    const dealerTotal = getTotal(dealer);
    if (newDealerTotal > 21) {
      document.querySelector(".msgdealer").textContent = "Dealer busted. You win!";
    } else if (newDealerTotal > dealerTotal) {
      document.querySelector(".msgdealer").textContent = "You win!";
    } else if (newDealerTotal < dealerTotal) {
      document.querySelector(".msgdealer").textContent = "Dealer wins!";
    } else {
      document.querySelector(".msgdealer").textContent = "It's a tie!";
    }

  }
}




function checkLastPlayer() {
  if (players.length < 2) {
    return;
  }
  const secondLastPlayerIndex = players.length - 2;
  const secondLastPlayer = players[secondLastPlayerIndex];
  if (!secondLastPlayer || secondLastPlayer.hasPlayed) {
    stand_card();
  }
}

