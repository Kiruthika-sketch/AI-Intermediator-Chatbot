// ============================
// API URL
// ============================

const API = "http://127.0.0.1:8000";

// ============================
// Load Chat History
// ============================

async function loadHistory(){

    const chatBox = document.getElementById("chat-box");

    chatBox.innerHTML = "";

    try{

        const response = await fetch(`${API}/history`);

        const data = await response.json();

        data.history.forEach(chat=>{

            addUserMessage(chat[0],chat[2]);

            addBotMessage(chat[1],chat[2]);

        });

        scrollBottom();

    }

    catch(err){

        console.log(err);

    }

}

// ============================
// Upload PDF
// ============================

async function uploadPDF(){

    const fileInput=document.getElementById("pdfFile");

    if(fileInput.files.length===0){

        alert("Select a PDF first.");

        return;

    }

    const formData=new FormData();

    formData.append("file",fileInput.files[0]);

    try{

        const response=await fetch(`${API}/upload`,{

            method:"POST",

            body:formData

        });

        const data=await response.json();

        alert(data.message);

        fileInput.value="";

        loadPDFs();

    }

    catch(err){

        console.log(err);

        alert("Upload failed.");

    }

}

// ============================
// Load Uploaded PDFs
// ============================

async function loadPDFs(){

    try{

        const response=await fetch(`${API}/pdfs`);

        const data=await response.json();

        const list=document.getElementById("pdf-list");

        list.innerHTML="";

        data.pdfs.forEach(pdf=>{

            list.innerHTML+=`

            <div class="pdf-item">

                <span>📄 ${pdf}</span>

                <button onclick="deletePDF('${pdf}')">

                    🗑

                </button>

            </div>

            `;

        });

    }

    catch(err){

        console.log(err);

    }

}

// ============================
// Delete PDF
// ============================

async function deletePDF(filename){

    const ok=confirm(`Delete ${filename}?`);

    if(!ok) return;

    try{

        await fetch(

            `${API}/delete-pdf/${filename}`,

            {

                method:"DELETE"

            }

        );

        loadPDFs();

    }

    catch(err){

        console.log(err);

    }

}

// ============================
// Clear Chat
// ============================

function clearChat(){

    document.getElementById("chat-box").innerHTML="";

}

// ============================
// Send Message
// ============================

async function sendMessage(){

    const input=document.getElementById("message");

    const message=input.value.trim();

    if(message==="") return;

    const mode=document.querySelector(

        'input[name="mode"]:checked'

    ).value;

    let endpoint="/chat";

    if(mode==="pdf"){

        endpoint="/ask-pdf";

    }

    const now=new Date().toLocaleTimeString();

    addUserMessage(message,now);

    input.value="";

    showTyping();

    try{

    const response = await fetch(

        API + endpoint,

        {

            method:"POST",

            headers:{

                "Content-Type":"application/json"

            },

            body:JSON.stringify({

                message:message

            })

        }

    );

    const data = await response.json();

    hideTyping();

    if(data.reply){

        addBotMessage(

            data.reply,

            new Date().toLocaleTimeString()

        );

    }

    else if(data.error){

        addBotMessage(

            data.error,

            new Date().toLocaleTimeString()

        );

    }

    else{

        addBotMessage(

            "Unknown server response.",

            new Date().toLocaleTimeString()

        );

    }

}
catch(err){

    hideTyping();

    console.error(err);

    addBotMessage(

        "Unable to connect to the server.",

        new Date().toLocaleTimeString()

    );

}

}

// ============================
// Add User Message
// ============================

function addUserMessage(message,time){

    const chat=document.getElementById("chat-box");

    chat.innerHTML+=`

    <div class="message">

        <div class="avatar">👤</div>

        <div>

            <div class="user-message">

                ${message}

            </div>

            <div class="time">

                ${time}

            </div>

        </div>

    </div>

    `;

}

// ============================
// Add Bot Message
// ============================

function addBotMessage(message,time){

    const chat=document.getElementById("chat-box");

    chat.innerHTML+=`

    <div class="message">

        <div class="avatar">🤖</div>

        <div>

            <div class="bot-message">

                ${message}

            </div>

            <div class="time">

                ${time}

            </div>

        </div>

    </div>

    `;



}

// ============================
// Typing Indicator
// ============================

function showTyping(){

    document.getElementById("typing").style.display="block";

}

function hideTyping(){

    document.getElementById("typing").style.display="none";

}

// ============================
// Auto Scroll
// ============================

function scrollBottom(){

    const chat=document.getElementById("chat-box");

    chat.scrollTop=chat.scrollHeight;

}

// ============================
// Enter Key
// ============================

document.addEventListener("DOMContentLoaded",()=>{

    const input=document.getElementById("message");

    input.addEventListener("keypress",function(e){

        if(e.key==="Enter"){

            e.preventDefault();

            sendMessage();

        }

    });

});

// ============================
// Startup
// ============================

window.onload=()=>{

    loadHistory();

    loadPDFs();

};

// ==========================
// Voice Recognition
// ==========================

const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;

let recognition;

if (SpeechRecognition) {

    recognition = new SpeechRecognition();

    recognition.lang = "en-US";
    recognition.continuous = false;
    recognition.interimResults = false;
    recognition.maxAlternatives = 1;

    recognition.onstart = function () {
        console.log("🎤 Listening...");
        document.getElementById("micBtn").innerHTML = "🎙️";
    };

    recognition.onresult = function (event) {

        console.log(event);

        const transcript = event.results[0][0].transcript;

        console.log("Recognized:", transcript);

        document.getElementById("message").value = transcript;

    };

    recognition.onerror = function (event) {

        console.log("Speech Error:", event.error);

        alert("Speech Error: " + event.error);

    };

    recognition.onend = function () {

        console.log("Recognition Ended");

        document.getElementById("micBtn").innerHTML = "🎤";

    };

}

function startListening() {

    if (!recognition) {

        alert("Speech Recognition not supported.");

        return;

    }

    recognition.start();

}