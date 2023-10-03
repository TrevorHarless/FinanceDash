const scrollers = document.querySelectorAll(".scroller");

// If a user hasn't opted in for recuded motion, then we add the animation
if (!window.matchMedia("(prefers-reduced-motion: reduce)").matches) {
  addAnimation();
}

function addAnimation() {
  scrollers.forEach((scroller) => {
    // add data-animated="true" to every `.scroller` on the page
    scroller.setAttribute("data-animated", true);

    // Make an array from the elements within `.scroller-inner`
    const scrollerInner = scroller.querySelector(".scroller__inner");
    const scrollerContent = Array.from(scrollerInner.children);

    // For each item in the array, clone it
    // add aria-hidden to it
    // add it into the `.scroller-inner`
    scrollerContent.forEach((item) => {
      const duplicatedItem = item.cloneNode(true);
      duplicatedItem.setAttribute("aria-hidden", true);
      scrollerInner.appendChild(duplicatedItem);
    });
  });
}


// $(document).ready(function() {
//     const cardDeck = $(".card-deck");
//     const card = $(".card");
//     const cardWidth = card.outerWidth(true); // Including margin

//     // Calculate the number of cards to show initially
//     const cardsToShow = Math.floor(cardDeck.width() / cardWidth);

//     // Clone the initial cards for infinite scrolling
//     for (let i = 0; i < cardsToShow; i++) {
//         cardDeck.append(card.clone());
//     }

//     // Function to check if scrolling is needed
//     function checkScroll() {
//         const scrollLeft = cardDeck.scrollLeft();
//         const cardsScrolled = Math.floor(scrollLeft / cardWidth);
//         if (scrollLeft >= cardDeck.width()) {
//             // Scroll beyond the width of the container, append new cards
//             cardDeck.scrollLeft(scrollLeft - (cardWidth * cardsToShow));
//             for (let i = 0; i < cardsToShow; i++) {
//                 cardDeck.append(card.clone());
//             }
//         }
//     }

//     // Listen for scroll events
//     cardDeck.on("scroll", checkScroll);
// });
