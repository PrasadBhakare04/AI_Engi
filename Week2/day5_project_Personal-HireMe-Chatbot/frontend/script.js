const CANDIDATE_NAME = "Prasad Bhakare";
const API_URL = "http://localhost:8000"; 
const PHONE = "+91 83809 42314";
const EMAIL = "prasadwork.2004@gmail.com";

const SUGGESTIONS = [
  "Give me a short summary of your background",
  "What are your key skills?",
  "Tell me about your work experience",
  "What projects have you built?",
  "What is your education?"
];

const $ = id => document.getElementById(id);
const thread = $("thread"), form = $("form"), input = $("q"), sendBtn = $("send");

$("phone").textContent = PHONE;
$("phone").href = "tel:" + PHONE.replace(/[^+\d]/g, "");
$("email").textContent = EMAIL;
$("email").href = "mailto:" + EMAIL;
$("title").textContent = "Ask " + CANDIDATE_NAME + " anything";
document.title = CANDIDATE_NAME + " | Hire me chat";

function addMsg(text, cls){
  const el = document.createElement("div");
  el.className = "msg " + cls;
  el.textContent = text;
  thread.appendChild(el);
  thread.scrollTop = thread.scrollHeight;
  return el;
}

function addTyping(){
  const el = document.createElement("div");
  el.className = "msg bot";
  el.innerHTML = '<span class="dots" aria-label="Thinking"><i></i><i></i><i></i></span>';
  thread.appendChild(el);
  thread.scrollTop = thread.scrollHeight;
  return el;
}

async function ask(question){
  question = question.trim();
  if(!question) return;

  $("chips").hidden = true;

  addMsg(question, "user");

  input.value = "";
  sendBtn.disabled = input.disabled = true;

  const typing = addTyping();

  try{
    const res = await fetch(API_URL + "/chat", {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({question})
    });

    if(!res.ok){
      throw new Error("Server returned " + res.status);
    }

    // Remove "thinking..."
    typing.remove();

    // Create an empty bot message
    const answerElement = addMsg("", "bot");

    // Get stream reader
    const reader = res.body.getReader();

    // Decode binary chunks
    const decoder = new TextDecoder();

    while(true){

      const { value, done } = await reader.read();

      if(done) break;

      const chunk = decoder.decode(value, {
        stream: true
      });

      answerElement.textContent += chunk;

      thread.scrollTop = thread.scrollHeight;
    }

  }catch(err){

    typing.remove();

    addMsg(
      "Couldn't reach the server. Check that the backend is running at " +
      API_URL +
      " and that CORS is enabled.",
      "bot error"
    );

    console.error(err);

  }finally{

    sendBtn.disabled = input.disabled = false;
    input.focus();

  }
}

form.addEventListener("submit", e => {
  e.preventDefault();
  ask(input.value);
});

SUGGESTIONS.forEach(s => {
  const b = document.createElement("button");
  b.type = "button";
  b.className = "chip";
  b.textContent = s;
  b.onclick = () => ask(s);
  $("chips").appendChild(b);
});

addMsg(
  "Hi, I'm an assistant that answers questions about " +
  CANDIDATE_NAME +
  "'s resume. What would you like to know?",
  "bot"
);