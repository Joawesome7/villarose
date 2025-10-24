function setActiveTab(button) {
  // Remove active class from all buttons
  document.querySelectorAll(".tab-button").forEach((btn) => {
    btn.className =
      "tab-button px-8 py-4 rounded-xl font-semibold transition-all duration-300 bg-white text-emerald-800 hover:bg-emerald-50 hover:shadow-md";
  });

  // Add active class to clicked button
  button.className =
    "tab-button px-8 py-4 rounded-xl font-semibold transition-all duration-300 bg-emerald-800 text-white shadow-lg transform -translate-y-1";
}

const faqData = {
  rooms: {
    question: "View Room Types & Prices",
    answer: `We offer 4 types of accommodations:

          🏨 TAKLONG VILLAS:
          • Executive Villa - ₱12,700 (2 pax, King bed, Ocean view)
          • Family Villa - ₱12,700 (2 pax, King + Bunk beds)
          • Junior Villa - ₱10,500 (2 pax, 2 Double beds)

          🏨 GUIWANON SUITES:
          • Premier Deluxe Room - ₱7,900 (2 pax, 2 Queen beds)

          All include breakfast and access to amenities! 🍳`,
    nextQuestions: ["amenities", "booking", "discount"],
  },
  amenities: {
    question: "What amenities do you offer?",
    answer: `We have amazing amenities for you! ✨

            INCLUDED:
            🏊 Swimming Pool
            🛝 Playground
            🍽️ Bar and Restaurant
            💆 Hunay Wellness & Spa

            AVAILABLE FOR BOOKING:
            🚤 Jetski
            🛶 Kayak
            🔥 Bonfire
            🤿 Snorkeling
            ⛵ Island Hopping
            🍌 Banana Boating

            And much more!`,
    nextQuestions: ["rooms", "booking", "location"],
  },
  location: {
    question: "Where are you located?",
    answer: `📍 ADDRESS:
            Tando, Dolores, Nueva Valencia, Guimaras

            We're located in the beautiful island of Guimaras! 🏝️

            CONTACT US:
            📞 09688731838 (SMS/Viber)
            📧 Info.villarosesortandspa@gmail.com`,
    nextQuestions: ["rooms", "booking", "amenities"],
  },
  booking: {
    question: "How to book?",
    answer: `Booking is easy! 📞

            3 WAYS TO BOOK:
            1️⃣ Call/Text: 09688731838 (SMS/Viber)
            2️⃣ Email: Info.villaroseresortandspa@gmail.com
            3️⃣ Click "BOOK NOW" button on our website

            We'll get back to you right away! ⚡`,
    nextQuestions: ["rooms", "discount", "amenities"],
  },
  discount: {
    question: "Tell me about the discount",
    answer: `🎉 LIMITED TIME OFFER!

            Save up to 40% OFF on accommodations!

            📅 VALID: Until Dec 31, 2025
            📆 APPLICABLE: Monday to Thursday only
            ⚠️ NOTE: Not applicable on holidays and special events

              Don't miss this amazing deal! 🌟`,
    nextQuestions: ["rooms", "booking", "amenities"],
  },
};

// Toggle chat window
function toggleChat() {
  const chatWindow = document.getElementById("chat-window");
  const chatIcon = document.getElementById("chat-icon");
  const closeIcon = document.getElementById("close-icon");

  if (chatWindow.classList.contains("hidden")) {
    chatWindow.classList.remove("hidden");
    chatWindow.classList.add("animate-slide-up");
    chatIcon.classList.add("hidden");
    closeIcon.classList.remove("hidden");
  } else {
    chatWindow.classList.add("hidden");
    chatIcon.classList.remove("hidden");
    closeIcon.classList.add("hidden");
  }
}

// Add user message to chat
function addUserMessage(text) {
  const messagesDiv = document.getElementById("chat-messages");
  const messageHTML = `
        <div class="flex items-start space-x-2 justify-end">
            <div class="bg-emerald-800 text-white rounded-lg rounded-tr-none p-3 shadow-sm max-w-xs">
                <p class="text-sm">${text}</p>
            </div>
        </div>
    `;
  messagesDiv.insertAdjacentHTML("beforeend", messageHTML);
  messagesDiv.scrollTop = messagesDiv.scrollHeight;
}

// Add bot message to chat
function addBotMessage(text, showButtons = true, nextQuestions = []) {
  const messagesDiv = document.getElementById("chat-messages");

  // Add typing indicator
  const typingHTML = `
        <div class="flex items-start space-x-2" id="typing-indicator">
            <div class="w-8 h-8 bg-emerald-800 rounded-full flex items-center justify-center flex-shrink-0">
                <span class="text-white text-sm">🏨</span>
            </div>
            <div class="bg-white rounded-lg rounded-tl-none p-3 shadow-sm">
                <div class="flex space-x-1">
                    <div class="w-2 h-2 bg-gray-400 rounded-full animate-bounce"></div>
                    <div class="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style="animation-delay: 0.1s"></div>
                    <div class="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style="animation-delay: 0.2s"></div>
                </div>
            </div>
        </div>
    `;
  messagesDiv.insertAdjacentHTML("beforeend", typingHTML);
  messagesDiv.scrollTop = messagesDiv.scrollHeight;

  // Remove typing indicator and show message after delay
  setTimeout(() => {
    document.getElementById("typing-indicator").remove();

    const messageHTML = `
            <div class="flex items-start space-x-2">
                <div class="w-8 h-8 bg-emerald-800 rounded-full flex items-center justify-center flex-shrink-0">
                    <span class="text-white text-sm">🏨</span>
                </div>
                <div class="bg-white rounded-lg rounded-tl-none p-3 shadow-sm max-w-xs">
                    <p class="text-sm text-gray-800">${text}</p>
                </div>
            </div>
        `;
    messagesDiv.insertAdjacentHTML("beforeend", messageHTML);

    // Add follow-up buttons if needed
    if (showButtons && nextQuestions.length > 0) {
      let buttonsHTML = '<div class="flex flex-col space-y-2 pl-10 mt-3">';
      buttonsHTML +=
        '<p class="text-xs text-gray-500 mb-1">You might also want to know:</p>';
      nextQuestions.forEach((q) => {
        const data = faqData[q];
        buttonsHTML += `<button onclick="askQuestion('${q}')" class="bg-emerald-50 hover:bg-emerald-100 text-emerald-800 text-sm px-4 py-2 rounded-lg text-left transition-colors">${data.question}</button>`;
      });
      buttonsHTML += "</div>";
      messagesDiv.insertAdjacentHTML("beforeend", buttonsHTML);
    }

    messagesDiv.scrollTop = messagesDiv.scrollHeight;
  }, 1000);
}

// Handle FAQ question
function askQuestion(questionKey) {
  const data = faqData[questionKey];
  addUserMessage(data.question);

  // Hide quick replies after first interaction
  const quickReplies = document.getElementById("quick-replies");
  if (quickReplies) {
    quickReplies.style.display = "none";
  }

  addBotMessage(data.answer, true, data.nextQuestions);
}

// Handle custom message
function sendMessage() {
  const input = document.getElementById("chat-input");
  const message = input.value.trim();

  if (message === "") return;

  addUserMessage(message);
  input.value = "";

  // Hide quick replies
  const quickReplies = document.getElementById("quick-replies");
  if (quickReplies) {
    quickReplies.style.display = "none";
  }

  // Simple keyword matching
  const lowerMessage = message.toLowerCase();

  if (
    lowerMessage.includes("room") ||
    lowerMessage.includes("price") ||
    lowerMessage.includes("cost")
  ) {
    askQuestion("rooms");
  } else if (
    lowerMessage.includes("amenity") ||
    lowerMessage.includes("amenities") ||
    lowerMessage.includes("facilities")
  ) {
    askQuestion("amenities");
  } else if (
    lowerMessage.includes("location") ||
    lowerMessage.includes("address") ||
    lowerMessage.includes("where")
  ) {
    askQuestion("location");
  } else if (
    lowerMessage.includes("book") ||
    lowerMessage.includes("reservation") ||
    lowerMessage.includes("reserve")
  ) {
    askQuestion("booking");
  } else if (
    lowerMessage.includes("discount") ||
    lowerMessage.includes("promo") ||
    lowerMessage.includes("offer")
  ) {
    askQuestion("discount");
  } else {
    // Default response
    addBotMessage(
      `Thanks for your message! 😊 

              I can help you with:
              • Room types and prices
              • Amenities and facilities
              • Location and contact info
              • Booking process
              • Current promotions

              What would you like to know?`,
      true,
      ["rooms", "amenities", "booking"]
    );
  }
}

// Add animation styles
const style = document.createElement("style");
style.textContent = `
          @keyframes slide-up {
              from {
                  opacity: 0;
                  transform: translateY(20px);
              }
              to {
                  opacity: 1;
                  transform: translateY(0);
              }
          }
          .animate-slide-up {
              animation: slide-up 0.3s ease-out;
          }
          `;
document.head.appendChild(style);
