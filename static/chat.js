var socket = io();

const msgBox = document.getElementById("messages");

/* Klasik chat */
const sendBtn = document.getElementById("sendBtn");
const msgInput = document.getElementById("msgInput");
const cipherSelect = document.getElementById("cipher");
const keyInput = document.getElementById("keyInput");

/* Secure chat */
const secureSendBtn = document.getElementById("secureSendBtn");
const secureAlgoSelect = document.getElementById("secureAlgo");
const secureMsgInput = document.getElementById("msgSecureInput");

let RSA_PUBLIC_KEY = null;

function writeMessage(text) {
    msgBox.innerHTML += `<div>${text}</div>`;
    msgBox.scrollTop = msgBox.scrollHeight;
}

socket.on("connect", () => {
    writeMessage("Sunucuya bağlanıldı.");
    socket.emit("rsa_key_request");
});

socket.on("server_message", (data) => {
    writeMessage("SERVER -> " + data.msg);
});

socket.on("broadcast", (data) => {
    writeMessage(
        `(${data.cipher}) Orijinal: ${data.original} -> Şifreli: ${data.processed}`
    );
});

socket.on("rsa_public_key", (key) => {
    RSA_PUBLIC_KEY = key;
    writeMessage("RSA public key alındı.");
});

socket.on("secure_response", (data) => {
    writeMessage("SERVER -> Çözülmüş Mesaj: " + data.decrypted);
});

/* Klasik gönder */
if (sendBtn) {
    sendBtn.onclick = () => {
        let msg = msgInput.value.trim();
        if (!msg) return;

        socket.emit("client_message", {
            message: msg,
            cipher: cipherSelect.value,
            key: keyInput.value
        });

        msgInput.value = "";
    };
}

/* Secure gönder */
if (secureSendBtn) {
    secureSendBtn.onclick = () => {
        let msg = secureMsgInput.value.trim();
        if (!msg) return;

        let algorithm = secureAlgoSelect.value;

        let symKey = algorithm.includes("DES")
            ? "8bytekey"
            : "thisis16bytekey";

        socket.emit("secure_message", {
            algorithm: algorithm,
            encrypted_key: symKey,
            message: msg
        });

        writeMessage(`SECURE (${algorithm}) -> Mesaj gönderildi`);
        secureMsgInput.value = "";
    };
}
