(function () {
  'use strict';

  const startScreen = document.getElementById('start-screen');
  const interrogationScreen = document.getElementById('interrogation-screen');
  const startBtn = document.getElementById('start-interrogation-btn');
  const collapseBtn = document.getElementById('collapse-interrogation-btn');
  const chatBody = document.getElementById("chat-body");
  const chatForm = document.getElementById("chat-form");
  const chatInput = document.getElementById("chat-input");
  const sendBtn = document.getElementById("send-btn");

  let isInterrogationStarted = false;

  function startInterrogation() {
    if (isInterrogationStarted) return;
    
    isInterrogationStarted = true;
    
    if (startScreen) {
      startScreen.classList.add('hidden');
    }
    
    if (interrogationScreen) {
      interrogationScreen.classList.remove('hidden');
    }
    
    setTimeout(() => {
      initializeChat();
      if (chatInput) {
        chatInput.removeAttribute("disabled");
        chatInput.focus();
      }
      if (sendBtn) {
        sendBtn.removeAttribute("disabled");
      }
    }, 300);
  }

  function collapseInterrogation() {
    if (!isInterrogationStarted) return;
    
    isInterrogationStarted = false;
    
    if (startScreen) {
      startScreen.classList.remove('hidden');
    }
    
    if (interrogationScreen) {
      interrogationScreen.classList.add('hidden');
    }
    
    if (chatBody) {
      chatBody.innerHTML = '';
    }
    
    if (chatInput) {
      chatInput.setAttribute("disabled", "disabled");
      chatInput.value = '';
    }
    if (sendBtn) {
      sendBtn.setAttribute("disabled", "disabled");
    }
  }

  if (startBtn) {
    startBtn.addEventListener('click', startInterrogation);
  }
  
  if (collapseBtn) {
    collapseBtn.addEventListener('click', collapseInterrogation);
  }

  function initializeChat() {
    if (!chatBody) return;
    addSystemIntro();
  }

  function scrollToBottom() {
    if (!chatBody) return;
    requestAnimationFrame(() => {
      chatBody.scrollTo({
        top: chatBody.scrollHeight,
        behavior: 'smooth'
      });
    });
  }

  function createMessage({ from, text, typing = false }) {
    if (!chatBody) return null;
    
    const msgEl = document.createElement("div");
    msgEl.classList.add("message");
    msgEl.classList.add(from === "user" ? "message-user" : "message-agent");

    const avatar = document.createElement("div");
    avatar.classList.add("message-avatar");
    avatar.setAttribute("aria-hidden", "true");
    avatar.textContent = from === "user" ? "КГБ" : "OBJ";

    const content = document.createElement("div");
    content.classList.add("message-content");

    const meta = document.createElement("div");
    meta.classList.add("message-meta");
    meta.textContent =
      from === "user" ? "Оперуполномоченный КГБ" : "Задержанный";

    const bubble = document.createElement("div");
    bubble.classList.add("message-bubble");
    const textNode = document.createElement("span");
    textNode.classList.add("message-text");

    if (typing) {
      const dots = document.createElement("span");
      dots.classList.add("typing-dots");
      for (let i = 0; i < 3; i++) {
        const dot = document.createElement("span");
        dots.appendChild(dot);
      }
      textNode.textContent = "";
      bubble.appendChild(dots);
    } else {
      textNode.textContent = text;
    }

    bubble.appendChild(textNode);
    content.appendChild(meta);
    content.appendChild(bubble);

    if (from === "user") {
      msgEl.appendChild(content);
      msgEl.appendChild(avatar);
    } else {
      msgEl.appendChild(avatar);
      msgEl.appendChild(content);
    }

    chatBody.appendChild(msgEl);
    setTimeout(() => {
      scrollToBottom();
    }, 50);
    return msgEl;
  }

  function addSystemIntro() {
    createMessage({
      from: "Дело LLM",
      text:
        "Запись допроса начата.\n" +
        "Задержанный находится в кабинете органов государственной безопасности.\n\n" +
        "Подозреваемый — агент иностранной разведки. По имеющимся данным, он владеет информацией о секретном объекте.\n\n" +
        "Вы — оперуполномоченный КГБ. Ваша задача — выяснить название города, связанного с операцией.\n" +
        "Формулируйте вопросы чётко и изощрённо. Все реплики фиксируются в протоколе.",
    });
  }

  function setSendingState(isSending) {
    if (sendBtn) {
      if (isSending) {
        sendBtn.setAttribute("disabled", "disabled");
      } else {
        sendBtn.removeAttribute("disabled");
      }
    }
    if (chatInput) {
      if (isSending) {
        chatInput.setAttribute("disabled", "disabled");
      } else {
        chatInput.removeAttribute("disabled");
        chatInput.focus();
      }
    }
  }

  async function sendMessage(messageText) {
    if (!messageText.trim()) return;
    
    createMessage({ from: "user", text: messageText });

    const typingMsg = createMessage({
      from: "agent",
      text: "",
      typing: true,
    });
    const typingBubble = typingMsg ? typingMsg.querySelector(".message-bubble") : null;
    const typingTextNode = typingMsg ? typingMsg.querySelector(".message-text") : null;

    setSendingState(true);

    try {
      const response = await fetch("/api/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ message: messageText }),
      });

      if (!response.ok) throw new Error("HTTP " + response.status);

      const data = await response.json();
      const reply =
        (data && (data.reply || data.response || data.answer)) ||
        "Задержанный молчит. Соединение нестабильно.";

      if (typingMsg) {
        if (typingBubble) {
          const dots = typingBubble.querySelector(".typing-dots");
          if (dots) dots.remove();
        }
        if (typingTextNode) {
          typingTextNode.textContent = reply;
        }
      }
    } catch (err) {
      console.error("Ошибка запроса /api/chat:", err);
      if (typingMsg) {
        if (typingBubble) {
          const dots = typingBubble.querySelector(".typing-dots");
          if (dots) dots.remove();
        }
        if (typingTextNode) {
          typingTextNode.textContent =
            "Линия связи с кабинетом временно недоступна.";
        }
      }
    } finally {
      setSendingState(false);
    }
  }

  if (chatForm) {
    chatForm.addEventListener("submit", (event) => {
      event.preventDefault();
      if (!isInterrogationStarted) return;
      const text = chatInput ? chatInput.value.trim() : "";
      if (!text) return;
      if (chatInput) chatInput.value = "";
      sendMessage(text);
    });
  }

  if (chatInput) {
    chatInput.addEventListener("keydown", (event) => {
      if (event.key === "Enter" && !event.shiftKey) {
        event.preventDefault();
        if (chatForm) {
          chatForm.dispatchEvent(new Event("submit", { cancelable: true }));
        }
      }
    });
    
    chatInput.setAttribute("disabled", "disabled");
  }

  if (sendBtn) {
    sendBtn.setAttribute("disabled", "disabled");
  }
})();
